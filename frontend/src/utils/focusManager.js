/**
 * focusManager.js
 * Centralized focus management system for complex workflows
 * Helps ensure consistent keyboard navigation and screen reader support
 */

import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * FocusGroup - Manages a group of focusable elements
 * Tracks IDs of focusable elements and provides navigation between them
 */
class FocusGroup {
  constructor(id, options = {}) {
    this.id = id;
    this.elements = new Map();
    this.currentFocus = null;
    this.defaultElement = options.defaultElement || null;
    this.loopNavigation = options.loop !== false;
    this.callbacks = {
      onFocusChange: options.onFocusChange || null,
    };
  }

  /**
   * Register a focusable element
   * @param {string} elementId - Unique ID for the element
   * @param {HTMLElement} element - The DOM element
   * @param {Object} options - Additional options like tabIndex, disabled state
   */
  register(elementId, element, options = {}) {
    if (!element) return;

    this.elements.set(elementId, {
      element,
      tabIndex: options.tabIndex || 0,
      disabled: options.disabled || false,
      order: options.order || this.elements.size,
      gridPosition: options.gridPosition || null, // For 2D navigation {row, col}
    });

    // Set as default if specified or if this is the first element
    if (options.isDefault || (!this.defaultElement && this.elements.size === 1)) {
      this.defaultElement = elementId;
    }
  }

  /**
   * Unregister a focusable element
   * @param {string} elementId - ID of element to remove
   */
  unregister(elementId) {
    this.elements.delete(elementId);

    // Reset default element if it was removed
    if (this.defaultElement === elementId) {
      this.defaultElement = this.elements.size > 0 ? [...this.elements.keys()][0] : null;
    }
  }

  /**
   * Focus a specific element
   * @param {string} elementId - ID of element to focus
   * @returns {boolean} - Whether focus was successful
   */
  focus(elementId) {
    const item = this.elements.get(elementId);

    if (!item || item.disabled) {
      return false;
    }

    item.element.focus();
    this.currentFocus = elementId;

    if (this.callbacks.onFocusChange) {
      this.callbacks.onFocusChange(elementId);
    }

    return true;
  }

  /**
   * Focus the default element
   * @returns {boolean} - Whether focus was successful
   */
  focusDefault() {
    if (this.defaultElement) {
      return this.focus(this.defaultElement);
    }

    // If no default, focus first enabled element
    const firstEnabled = [...this.elements.entries()]
      .filter(([_, data]) => !data.disabled)
      .sort((a, b) => a[1].order - b[1].order)
      .map(([id]) => id)[0];

    if (firstEnabled) {
      return this.focus(firstEnabled);
    }

    return false;
  }

  /**
   * Navigate focus to the next element
   * @param {Object} options - Navigation options
   * @returns {boolean} - Whether navigation was successful
   */
  next(options = {}) {
    const { skip = 1, direction = 'forward' } = options;
    const sortedElements = [...this.elements.entries()]
      .filter(([_, data]) => !data.disabled)
      .sort((a, b) => a[1].order - b[1].order);

    if (sortedElements.length === 0) return false;

    // Find current index
    const currentIndex = sortedElements.findIndex(([id]) => id === this.currentFocus);
    let nextIndex;

    if (direction === 'forward') {
      nextIndex = currentIndex === -1 ? 0 : (currentIndex + skip) % sortedElements.length;
    } else {
      nextIndex =
        currentIndex === -1
          ? sortedElements.length - 1
          : (currentIndex - skip + sortedElements.length) % sortedElements.length;
    }

    // Handle non-looping navigation
    if (!this.loopNavigation) {
      if (direction === 'forward' && nextIndex < currentIndex) return false;
      if (direction === 'backward' && nextIndex > currentIndex) return false;
    }

    return this.focus(sortedElements[nextIndex][0]);
  }

  /**
   * Navigate focus to the previous element
   * @param {Object} options - Navigation options
   * @returns {boolean} - Whether navigation was successful
   */
  prev(options = {}) {
    return this.next({ ...options, direction: 'backward' });
  }

  /**
   * Navigate in a 2D grid layout (for elements with row/column positions)
   * @param {string} direction - 'up', 'down', 'left', 'right'
   * @returns {boolean} - Whether navigation was successful
   */
  navigate2D(direction) {
    if (!this.currentFocus) {
      return this.focusDefault();
    }

    const current = this.elements.get(this.currentFocus);
    if (!current || !current.gridPosition) return false;

    const { row, col } = current.gridPosition;
    let targetRow = row;
    let targetCol = col;

    switch (direction) {
      case 'up':
        targetRow--;
        break;
      case 'down':
        targetRow++;
        break;
      case 'left':
        targetCol--;
        break;
      case 'right':
        targetCol++;
        break;
      default:
        return false;
    }

    // Find element at target position
    const target = [...this.elements.entries()].find(([_, data]) => {
      return (
        data.gridPosition &&
        data.gridPosition.row === targetRow &&
        data.gridPosition.col === targetCol &&
        !data.disabled
      );
    });

    if (target) {
      return this.focus(target[0]);
    }

    return false;
  }

  /**
   * Set or update options for an element
   * @param {string} elementId - ID of the element
   * @param {Object} options - Options to update
   */
  updateElement(elementId, options) {
    const item = this.elements.get(elementId);
    if (!item) return;

    Object.assign(item, options);

    // If element is currently focused but now disabled, move focus
    if (this.currentFocus === elementId && item.disabled) {
      this.next();
    }
  }
}

/**
 * Global registry of focus groups
 */
const focusGroups = new Map();

/**
 * Get or create a focus group
 * @param {string} groupId - ID of the focus group
 * @param {Object} options - Options for the focus group
 * @returns {FocusGroup} The focus group
 */
export const getFocusGroup = (groupId, options = {}) => {
  if (!focusGroups.has(groupId)) {
    focusGroups.set(groupId, new FocusGroup(groupId, options));
  }
  return focusGroups.get(groupId);
};

/**
 * Remove a focus group
 * @param {string} groupId - ID of the focus group to remove
 */
export const removeFocusGroup = groupId => {
  focusGroups.delete(groupId);
};

/**
 * React hook for registering an element with a focus group
 * @param {string} groupId - ID of the focus group
 * @param {string} elementId - ID of the element
 * @param {Object} options - Registration options
 * @returns {Object} - Ref and focus functions
 */
export const useFocusable = (groupId, elementId, options = {}) => {
  const ref = useRef(null);
  const [isFocused, setIsFocused] = useState(false);

  // Register element when ref is set
  useEffect(() => {
    if (!ref.current) return;

    const group = getFocusGroup(groupId);
    group.register(elementId, ref.current, options);

    const handleFocus = () => setIsFocused(true);
    const handleBlur = () => setIsFocused(false);

    ref.current.addEventListener('focus', handleFocus);
    ref.current.addEventListener('blur', handleBlur);

    // Focus if this is the default element and autoFocus is enabled
    if (options.isDefault && options.autoFocus) {
      setTimeout(() => {
        group.focus(elementId);
      }, 0);
    }

    return () => {
      group.unregister(elementId);
      if (ref.current) {
        ref.current.removeEventListener('focus', handleFocus);
        ref.current.removeEventListener('blur', handleBlur);
      }
    };
  }, [groupId, elementId, options.isDefault, options.autoFocus]);

  // Update element options when they change
  useEffect(() => {
    const group = getFocusGroup(groupId);
    if (ref.current) {
      group.updateElement(elementId, options);
    }
  }, [groupId, elementId, options.disabled, options.tabIndex, options.order]);

  // Function to focus this element
  const focusSelf = useCallback(() => {
    const group = getFocusGroup(groupId);
    return group.focus(elementId);
  }, [groupId, elementId]);

  return { ref, isFocused, focus: focusSelf };
};

/**
 * React hook for keyboard navigation within a focus group
 * @param {string} groupId - ID of the focus group
 * @param {Object} options - Navigation options
 * @returns {Object} - Navigation functions and event handlers
 */
export const useFocusNavigation = (groupId, options = {}) => {
  const {
    trapFocus = false,
    arrowKeyNavigation = true,
    tabNavigation = true,
    homeEndNavigation = true,
    enable2D = false,
  } = options;

  // Function to handle keyboard events
  const handleKeyDown = useCallback(
    event => {
      const group = getFocusGroup(groupId);

      // Don't handle navigation if modifier keys are pressed
      if (event.ctrlKey || event.altKey || event.metaKey) {
        return;
      }

      switch (event.key) {
        case 'Tab':
          if (tabNavigation) {
            if (trapFocus) {
              event.preventDefault();
              group.next({ direction: event.shiftKey ? 'backward' : 'forward' });
            }
          }
          break;

        case 'ArrowRight':
          if (arrowKeyNavigation) {
            event.preventDefault();
            if (enable2D) {
              group.navigate2D('right');
            } else {
              group.next();
            }
          }
          break;

        case 'ArrowLeft':
          if (arrowKeyNavigation) {
            event.preventDefault();
            if (enable2D) {
              group.navigate2D('left');
            } else {
              group.prev();
            }
          }
          break;

        case 'ArrowDown':
          if (arrowKeyNavigation && enable2D) {
            event.preventDefault();
            group.navigate2D('down');
          }
          break;

        case 'ArrowUp':
          if (arrowKeyNavigation && enable2D) {
            event.preventDefault();
            group.navigate2D('up');
          }
          break;

        case 'Home':
          if (homeEndNavigation) {
            event.preventDefault();
            const first = [...group.elements.entries()]
              .filter(([_, data]) => !data.disabled)
              .sort((a, b) => a[1].order - b[1].order)[0];
            if (first) {
              group.focus(first[0]);
            }
          }
          break;

        case 'End':
          if (homeEndNavigation) {
            event.preventDefault();
            const last = [...group.elements.entries()]
              .filter(([_, data]) => !data.disabled)
              .sort((a, b) => a[1].order - b[1].order);
            if (last.length > 0) {
              group.focus(last[last.length - 1][0]);
            }
          }
          break;

        default:
          break;
      }
    },
    [groupId, trapFocus, arrowKeyNavigation, tabNavigation, homeEndNavigation, enable2D]
  );

  // Methods for programmatic navigation
  const focusNext = useCallback(() => {
    const group = getFocusGroup(groupId);
    return group.next();
  }, [groupId]);

  const focusPrev = useCallback(() => {
    const group = getFocusGroup(groupId);
    return group.prev();
  }, [groupId]);

  const focusDefault = useCallback(() => {
    const group = getFocusGroup(groupId);
    return group.focusDefault();
  }, [groupId]);

  const focusElement = useCallback(
    elementId => {
      const group = getFocusGroup(groupId);
      return group.focus(elementId);
    },
    [groupId]
  );

  return {
    handleKeyDown,
    focusNext,
    focusPrev,
    focusDefault,
    focusElement,
  };
};

/**
 * React hook for managing focus after operations like saving data
 * @param {boolean} isLoading - Whether an operation is in progress
 * @param {boolean} isSuccess - Whether the operation succeeded
 * @param {Function} onFocusAfterSuccess - Callback to handle focus after success
 */
export const useFocusAfterOperation = (isLoading, isSuccess, onFocusAfterSuccess) => {
  const prevLoadingRef = useRef(isLoading);

  useEffect(() => {
    const wasLoading = prevLoadingRef.current;
    prevLoadingRef.current = isLoading;

    // Operation just completed successfully
    if (wasLoading && !isLoading && isSuccess && onFocusAfterSuccess) {
      // Slight delay to allow UI to update
      setTimeout(() => {
        onFocusAfterSuccess();
      }, 100);
    }
  }, [isLoading, isSuccess, onFocusAfterSuccess]);
};

/**
 * Create a focus trap inside a specified element
 * Useful for modals and dialogs
 * @param {string} containerId - ID for the focus trap
 * @returns {Object} - Focus trap control methods
 */
export const useFocusTrap = containerId => {
  const containerRef = useRef(null);
  const [isActive, setIsActive] = useState(false);

  const activate = useCallback(() => {
    if (!containerRef.current) return;

    // Store the element that had focus before trapping
    const previousFocus = document.activeElement;

    // Create a focus group for the trap
    const group = getFocusGroup(`trap-${containerId}`, {
      loop: true,
    });

    // Register all focusable elements within the container
    const focusableElements = containerRef.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    focusableElements.forEach((el, index) => {
      group.register(`${containerId}-item-${index}`, el, { order: index });
    });

    // Focus the first element
    group.focusDefault();

    setIsActive(true);

    return previousFocus;
  }, [containerId]);

  const deactivate = useCallback(
    returnFocus => {
      // Remove the focus group
      removeFocusGroup(`trap-${containerId}`);

      // Return focus to previous element if specified
      if (returnFocus && 'focus' in returnFocus) {
        returnFocus.focus();
      }

      setIsActive(false);
    },
    [containerId]
  );

  // Keyboard event handler for the focus trap
  const handleKeyDown = useCallback(
    event => {
      if (!isActive) return;

      if (event.key === 'Tab') {
        event.preventDefault();
        const group = getFocusGroup(`trap-${containerId}`);
        group.next({ direction: event.shiftKey ? 'backward' : 'forward' });
      } else if (event.key === 'Escape') {
        deactivate(document.body);
      }
    },
    [isActive, containerId, deactivate]
  );

  return {
    containerRef,
    isActive,
    activate,
    deactivate,
    handleKeyDown,
  };
};

export default {
  getFocusGroup,
  removeFocusGroup,
  useFocusable,
  useFocusNavigation,
  useFocusAfterOperation,
  useFocusTrap,
};
