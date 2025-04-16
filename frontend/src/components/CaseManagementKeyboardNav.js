import React, { useEffect, useState, useCallback, useRef, useMemo } from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  IconButton,
  Flex,
  Text,
  Heading,
  Input,
  Select,
  useToast,
  VisuallyHidden,
  InputGroup,
  InputLeftElement,
} from '@chakra-ui/react';
import { FaEdit, FaTrash, FaEye, FaLock, FaSort } from 'react-icons/fa';
import { useFocusable, useFocusNavigation, useFocusAfterOperation } from '../utils/focusManager';
import PropTypes from 'prop-types';
import { SearchIcon } from '@chakra-ui/icons';
/**
 * CaseManagementKeyboardNav component
 * Demonstrates accessible keyboard navigation for case management using our focus management system
 */
// Create a SearchInput component
const SearchInput = React.forwardRef(({ onSearch, ...props }, ref) => (
  <InputGroup>
    <InputLeftElement pointerEvents="none">
      <SearchIcon color="gray.300" />
    </InputLeftElement>
    <Input
      ref={ref}
      placeholder="Search cases..."
      onChange={(e) => onSearch(e.target.value)}
      {...props}
    />
  </InputGroup>
));
SearchInput.displayName = 'SearchInput';
const CaseManagementKeyboardNav = ({ cases = [], onViewCase, onEditCase, onDeleteCase }) => {
  const [filteredCases, setFilteredCases] = useState(cases);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortField, setSortField] = useState('priority');
  const [sortDirection, setSortDirection] = useState('desc');
  const [selectedCaseId, setSelectedCaseId] = useState(null);
  const [operation, setOperation] = useState({ type: null, isLoading: false, isSuccess: false });
  const [announcement, setAnnouncement] = useState('');
  const toast = useToast();
  // Create refs at the component level
  const rowRefs = useRef({});
  const actionRefs = useRef({});
  const viewRefs = useRef({});
  const editRefs = useRef({});
  const deleteRefs = useRef({});
  // Register focus for search input and sort select
  const { ref: searchInputRef, isFocused: isSearchFocused } = useFocusable(
    'case-management-main-actions',
    'search-input',
    {
      isDefault: true,
      autoFocus: true,
      order: 1,
    }
  );
  const { ref: sortSelectRef } = useFocusable('case-management-main-actions', 'sort-select', {
    order: 2,
  });
  // Create caseRefs using useMemo
  const caseRefs = useMemo(() => {
    const refs = {};
    cases.forEach(caseItem => {
      const caseId = caseItem.id;
      refs[caseId] = {
        row: rowRefs.current[caseId],
        view: viewRefs.current[caseId],
        edit: editRefs.current[caseId],
        delete: deleteRefs.current[caseId]
      };
    });
    return refs;
  }, [cases]);
  // Update refs when they change
  useEffect(() => {
    const currentRefs = {
      row: { ...rowRefs.current },
      view: { ...viewRefs.current },
      edit: { ...editRefs.current },
      delete: { ...deleteRefs.current }
    };
    cases.forEach(caseItem => {
      const caseId = caseItem.id;
      rowRefs.current[caseId] = rowRefs.current[caseId] || null;
      viewRefs.current[caseId] = viewRefs.current[caseId] || null;
      editRefs.current[caseId] = editRefs.current[caseId] || null;
      deleteRefs.current[caseId] = deleteRefs.current[caseId] || null;
    });
    // Cleanup function to delete refs when component unmounts
    return () => {
      Object.keys(currentRefs.row).forEach(caseId => {
        delete rowRefs.current[caseId, rowRefs.current];
        delete viewRefs.current[caseId, viewRefs.current];
        delete editRefs.current[caseId, editRefs.current];
        delete deleteRefs.current[caseId, deleteRefs.current];
      });
    };
  }, [cases]);
  const registerCaseRow = useCallback((caseId, element) => {
    rowRefs.current[caseId] = element;
  }, []);
  const registerRowAction = useCallback((caseId, actionType, element) => {
    switch (actionType) {
      case 'view':
        viewRefs.current[caseId] = element;
        break;
      case 'edit':
        editRefs.current[caseId] = element;
        break;
      case 'delete':
        deleteRefs.current[caseId] = element;
        break;
    }
  }, []);
  // Create a focus group for the main actions
  const mainActionsFocusGroupId = 'case-management-main-actions';
  const {
    handleKeyDown: handleMainActionsKeyDown,
    focusNext: focusNextMainAction,
    focusPrev: focusPrevMainAction,
    focusDefault: focusDefaultMainAction,
  } = useFocusNavigation(mainActionsFocusGroupId, {
    trapFocus: false,
    arrowKeyNavigation: true,
  });
  // Create a focus group for the case table rows
  const caseRowsFocusGroupId = 'case-management-rows';
  const { handleKeyDown: handleRowsKeyDown, focusDefault: focusDefaultRow } = useFocusNavigation(
    caseRowsFocusGroupId,
    {
      trapFocus: false,
      arrowKeyNavigation: true,
    }
  );
  // Create a focus group for actions within a row
  const rowActionsFocusGroupId = 'case-management-row-actions';
  const {
    handleKeyDown: handleRowActionsKeyDown,
    focusNext: focusNextRowAction,
    focusPrev: focusPrevRowAction,
  } = useFocusNavigation(rowActionsFocusGroupId, {
    trapFocus: false,
    arrowKeyNavigation: true,
  });
  // Register focus for refresh button
  const { ref: refreshButtonRef } = useFocusable(mainActionsFocusGroupId, 'refresh-button', {
    order: 3,
  });
  // Focus management after operations
  useFocusAfterOperation(operation.isLoading, operation.isSuccess, () => {
    switch (operation.type) {
      case 'delete': {
        // Focus the next row or the previous if deleted the last one
        const nextRow = document.querySelector('[data-testid^="case-row-"]');
        if (nextRow) nextRow.focus();
        break;
      }
      case 'edit': {
        // Return focus to the edited row
        if (selectedCaseId) {
          const rowId = `case-row-${selectedCaseId}`;
          const rowFocusable = document.getElementById(rowId);
          if (rowFocusable) rowFocusable.focus();
        }
        break;
      }
      default:
        searchInputRef.current?.focus();
    }
  });
  // Sort cases when sort parameters change
  useEffect(() => {
    const sorted = [...cases].sort((a, b) => {
      const fieldA = a[sortField] ?? '';
      const fieldB = b[sortField] ?? '';
      if (typeof fieldA === 'string' && typeof fieldB === 'string') {
        return sortDirection === 'asc'
          ? fieldA.localeCompare(fieldB)
          : fieldB.localeCompare(fieldA);
      }
      return sortDirection === 'asc' ? fieldA - fieldB : fieldB - fieldA;
    });
    const filtered = searchTerm
      ? sorted.filter(
          c =>
            c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.client.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.status.toLowerCase().includes(searchTerm.toLowerCase())
        )
      : sorted;
    setFilteredCases(filtered);
    // Make screen reader announcement about search/sort results
    if (searchTerm) {
      setAnnouncement(`Found ${filtered.length} cases matching "${searchTerm}"`);
    } else if (sorted !== cases) {
      setAnnouncement(
        `Cases sorted by ${sortField} ${sortDirection === 'asc' ? 'ascending' : 'descending'}`
      );
    }
  }, [cases, searchTerm, sortField, sortDirection]);
  // Handle search input change
  const handleSearch = useCallback((value) => {
    setSearchTerm(value);
    const filtered = cases.filter(caseItem => 
      caseItem.title.toLowerCase().includes(value.toLowerCase()) ||
      caseItem.description.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredCases(filtered);
  }, [cases]);
  // Handle sort change
  const handleSort = useCallback((field) => {
    setSortField(field);
    setSortDirection(prev => prev === 'asc' ? 'desc' : 'asc');
    
    const sorted = [...filteredCases].sort((a, b) => {
      const aValue = a[field];
      const bValue = b[field];
      const modifier = sortDirection === 'asc' ? 1 : -1;
      
      if (aValue < bValue) return -1 * modifier;
      if (aValue > bValue) return 1 * modifier;
      return 0;
    });
    
    setFilteredCases(sorted);
  }, [filteredCases, sortDirection]);
  // Handle refresh button click
  const handleRefresh = () => {
    setOperation({ type: 'refresh', isLoading: true, isSuccess: false });
    // Simulate API call
    setTimeout(() => {
      setOperation({ type: 'refresh', isLoading: false, isSuccess: true });
      toast({
        title: 'Cases refreshed',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      setAnnouncement('Cases list refreshed');
    }, 500);
  };
  // Handle case row selection
  const handleRowSelect = caseId => {
    setSelectedCaseId(caseId === selectedCaseId ? null : caseId);
    setAnnouncement(`Case ${caseId} ${caseId === selectedCaseId ? 'unselected' : 'selected'}`);
  };
  // Handle case row keyboard navigation
  const handleRowKeyDown = (e, caseItem) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        handleRowSelect(caseItem.id);
        break;
      case 'ArrowRight':
        e.preventDefault();
        // Move focus to row actions
        const firstActionId = `view-case-${caseItem.id}`;
        const firstActionEl = document.getElementById(firstActionId);
        if (firstActionEl) {
          firstActionEl.focus();
        }
        break;
      default:
        handleRowsKeyDown(e);
    }
  };
  // Handle key down on row actions
  const handleActionKeyDown = (e, actionType, caseItem) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (actionType === 'view') {
          handleViewCase(caseItem);
        } else if (actionType === 'edit') {
          handleEditCase(caseItem);
        } else if (actionType === 'delete') {
          handleDeleteCase(caseItem);
        }
        break;
      case 'ArrowLeft':
        if (actionType === 'view') {
          e.preventDefault();
          // Move focus back to row
          const rowId = `case-row-${caseItem.id}`;
          const rowEl = document.getElementById(rowId);
          if (rowEl) {
            rowEl.focus();
          }
        } else {
          handleRowActionsKeyDown(e);
        }
        break;
      default:
        handleRowActionsKeyDown(e);
    }
  };
  // Action handlers
  const handleViewCase = caseItem => {
    if (onViewCase) {
      onViewCase(caseItem);
    }
    toast({
      title: 'Viewing case',
      description: `Opening case ${caseItem.title}`,
      status: 'info',
      duration: 3000,
    });
    setAnnouncement(`Opening case ${caseItem.title}`);
  };
  const handleEditCase = caseItem => {
    setOperation({ type: 'edit', isLoading: true, isSuccess: false });
    setSelectedCaseId(caseItem.id);
    if (onEditCase) {
      // Simulate API call
      setTimeout(() => {
        onEditCase(caseItem);
        setOperation({ type: 'edit', isLoading: false, isSuccess: true });
        toast({
          title: 'Case updated',
          description: `Case ${caseItem.title} has been updated`,
          status: 'success',
          duration: 3000,
        });
        setAnnouncement(`Case ${caseItem.title} has been updated`);
      }, 500);
    }
  };
  const handleDeleteCase = caseItem => {
    setOperation({ type: 'delete', isLoading: true, isSuccess: false });
    setSelectedCaseId(caseItem.id);
    if (onDeleteCase) {
      // Simulate API call
      setTimeout(() => {
        onDeleteCase(caseItem);
        setOperation({ type: 'delete', isLoading: false, isSuccess: true });
        toast({
          title: 'Case deleted',
          description: `Case ${caseItem.title} has been removed`,
          status: 'success',
          duration: 3000,
        });
        setAnnouncement(`Case ${caseItem.title} has been deleted`);
      }, 500);
    }
  };
  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      const activeElement = document.activeElement;
      if (activeElement) {
        const action = activeElement.getAttribute('data-action');
        if (action === 'view') {
          onViewCase();
        } else if (action === 'edit') {
          onEditCase();
        } else if (action === 'delete') {
          onDeleteCase();
        }
      }
    }
  }, [onViewCase, onEditCase, onDeleteCase]);
  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);
  // Render row actions
  const renderRowActions = caseItem => {
    const viewAction = registerRowAction(caseItem.id, 'view', null);
    const editAction = registerRowAction(caseItem.id, 'edit', null);
    const deleteAction = registerRowAction(caseItem.id, 'delete', null);
    return (
      <Flex gap={2}>
        <IconButton
          {...viewAction}
          aria-label="View case"
          icon={<FaEye />}
          onClick={() => handleViewCase(caseItem)}
        />
        <IconButton
          {...editAction}
          aria-label="Edit case"
          icon={<FaEdit />}
          onClick={() => handleEditCase(caseItem)}
        />
        <IconButton
          {...deleteAction}
          aria-label="Delete case"
          icon={<FaTrash />}
          onClick={() => handleDeleteCase(caseItem)}
        />
      </Flex>
    );
  };
  return (
    <Box>
      <Flex mb={4} alignItems="center">
        <Box flex="1" maxW="300px">
          <SearchInput
            ref={searchInputRef}
            onSearch={handleSearch}
          />
        </Box>
        <IconButton
          icon={<FaSort />}
          aria-label="Sort cases"
          ml={2}
          onClick={() => handleSort(sortField)}
        />
      </Flex>
      <Button
        colorScheme="blue"
        onClick={handleRefresh}
        isLoading={operation.type === 'refresh' && operation.isLoading}
        ml="auto"
        ref={refreshButtonRef}
        aria-label="Refresh case list"
      >
        Refresh
      </Button>
      {/* Case summary */}
      <Text mb={4}>
        {filteredCases.length} {filteredCases.length === 1 ? 'case' : 'cases'} found
        {searchTerm ? ` matching "${searchTerm}"` : ''}
      </Text>
      {/* Cases table */}
      <Box overflowX="auto">
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Status</Th>
              <Th>Priority</Th>
              <Th>Case Title</Th>
              <Th>Client</Th>
              <Th>Due Date</Th>
              <Th>Actions</Th>
            </Tr>
          </Thead>
          <Tbody onKeyDown={handleRowsKeyDown}>
            {filteredCases.map((caseItem, index) => {
              const isHighPriority = caseItem.priority === 'high';
              const isConfidential = caseItem.confidential;
              const rowId = `case-row-${caseItem.id}`;
              // Register focus for each row
              const { ref: rowRef } = registerCaseRow(caseItem.id, null);
              // Register focus for row actions
              const { ref: viewRef } = registerRowAction(caseItem.id, 'view', null);
              const { ref: editRef } = registerRowAction(caseItem.id, 'edit', null);
              const { ref: deleteRef } = registerRowAction(caseItem.id, 'delete', null);
              return (
                <Tr
                  key={caseItem.id}
                  bg={selectedCaseId === caseItem.id ? 'blue.50' : undefined}
                  _hover={{ bg: 'gray.50' }}
                  tabIndex={0}
                  id={rowId}
                  ref={rowRef}
                  onClick={() => handleRowSelect(caseItem.id)}
                  onKeyDown={e => handleRowKeyDown(e, caseItem)}
                  aria-selected={selectedCaseId === caseItem.id}
                  role="row"
                  aria-label={`Case ${caseItem.title}, ${caseItem.status}, Priority: ${caseItem.priority}`}
                >
                  <Td>{caseItem.status}</Td>
                  <Td color={isHighPriority ? 'red.500' : undefined}>{caseItem.priority}</Td>
                  <Td>
                    <Flex alignItems="center">
                      {isConfidential && (
                        <FaLock
                          color="gray"
                          style={{ marginRight: '8px' }}
                          aria-label="Confidential case"
                        />
                      )}
                      {caseItem.title}
                    </Flex>
                  </Td>
                  <Td>{caseItem.client}</Td>
                  <Td>{caseItem.dueDate}</Td>
                  <Td>{renderRowActions(caseItem)}</Td>
                </Tr>
              );
            })}
          </Tbody>
        </Table>
      </Box>
      {filteredCases.length === 0 && (
        <Box textAlign="center" p={6}>
          <Text>No cases found matching your search criteria.</Text>
        </Box>
      )}
      {/* Keyboard navigation instructions */}
      <Box mt={6} p={4} bg="gray.50" borderRadius="md">
        <Heading size="sm" mb={2}>
          Keyboard Navigation
        </Heading>
        <Text as="div">
          <ul>
            <li>
              Use <kbd>Tab</kbd> to navigate between controls and table rows
            </li>
            <li>
              Use <kbd>Arrow keys</kbd> to navigate between table rows
            </li>
            <li>
              Press <kbd>Enter</kbd> to select a row
            </li>
            <li>
              Use <kbd>Right Arrow</kbd> from a row to access row actions
            </li>
            <li>
              Use <kbd>Left Arrow</kbd> from actions to return to the row
            </li>
            <li>
              Press <kbd>Enter</kbd> on an action button to activate it
            </li>
          </ul>
        </Text>
      </Box>
    </Box>
  );
};
SearchInput.propTypes = {
  onSearch: PropTypes.func.isRequired
};
CaseManagementKeyboardNav.propTypes = {
  cases: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
      priority: PropTypes.string.isRequired,
      status: PropTypes.string.isRequired,
    })
  ),
  onViewCase: PropTypes.func.isRequired,
  onEditCase: PropTypes.func.isRequired,
  onDeleteCase: PropTypes.func.isRequired,
};
export default CaseManagementKeyboardNav;