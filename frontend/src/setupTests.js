// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
import '@testing-library/jest-dom/extend-expect';
import React from 'react';

// Mock window.matchMedia
window.matchMedia = jest.fn().mockImplementation(query => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: jest.fn(),
  removeListener: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  dispatchEvent: jest.fn(),
}));

// Mock IntersectionObserver
window.IntersectionObserver = class IntersectionObserver {
  constructor() {
    this.observe = jest.fn();
    this.unobserve = jest.fn();
    this.disconnect = jest.fn();
  }
};

// Mock ResizeObserver
window.ResizeObserver = class ResizeObserver {
  constructor() {
    this.observe = jest.fn();
    this.unobserve = jest.fn();
    this.disconnect = jest.fn();
  }
};

// Mock Chakra UI components
jest.mock('@chakra-ui/react', () => {
  const mockToast = jest.fn();

  const createMockComponent = displayName => {
    const component = ({ children, ...props }) => {
      const elementType = displayName.toLowerCase();
      return `<${elementType}>${children || ''}</${elementType}>`;
    };
    component.displayName = displayName;
    return component;
  };

  return {
    Box: createMockComponent('Box'),
    Heading: createMockComponent('Heading'),
    Text: createMockComponent('Text'),
    Badge: createMockComponent('Badge'),
    VStack: createMockComponent('VStack'),
    HStack: createMockComponent('HStack'),
    IconButton: createMockComponent('IconButton'),
    useColorModeValue: light => light,
    Checkbox: createMockComponent('Checkbox'),
    Divider: createMockComponent('Divider'),
    useToast: () => mockToast,
    Button: createMockComponent('Button'),
    Modal: createMockComponent('Modal'),
    ModalOverlay: createMockComponent('ModalOverlay'),
    ModalContent: createMockComponent('ModalContent'),
    ModalHeader: createMockComponent('ModalHeader'),
    ModalFooter: createMockComponent('ModalFooter'),
    ModalBody: createMockComponent('ModalBody'),
    ModalCloseButton: createMockComponent('ModalCloseButton'),
    FormControl: createMockComponent('FormControl'),
    FormLabel: createMockComponent('FormLabel'),
    Input: createMockComponent('Input'),
    Select: createMockComponent('Select'),
    Tooltip: createMockComponent('Tooltip'),
    Container: createMockComponent('Container'),
    SimpleGrid: createMockComponent('SimpleGrid'),
    Stat: createMockComponent('Stat'),
    StatLabel: createMockComponent('StatLabel'),
    StatNumber: createMockComponent('StatNumber'),
    StatHelpText: createMockComponent('StatHelpText'),
    StatArrow: createMockComponent('StatArrow'),
  };
});
