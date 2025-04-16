import { render, screen } from '@testing-library/react';
import DeadlineReminders from '../DeadlineReminders';

// Mock date-fns to return a consistent date
jest.mock('date-fns', () => ({
  parseISO: jest.fn(str => new Date(str)),
  formatDistance: jest.fn(() => '2 days'),
  isAfter: jest.fn(() => false),
  isBefore: jest.fn(() => true),
}));

// Mock React Icons
jest.mock('react-icons/md', () => ({
  MdAdd: () => 'Add Icon',
  MdSort: () => 'Sort Icon',
}));

describe('DeadlineReminders', () => {
  it('renders without crashing', () => {
    render(<DeadlineReminders />);
    expect(screen.getByText('Deadlines')).toBeInTheDocument();
  });
});
