import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import DocumentGenerator from '../DocumentGenerator';
import axios from 'axios';

// Mock axios
jest.mock('axios');

// Mock the auth context
jest.mock('../../contexts/AuthContext', () => ({
  useAuth: () => ({
    user: { id: 'user123', email: 'test@example.com', name: 'Test User' },
    token: 'mock-token',
    isAuthenticated: true,
  }),
}));

describe('DocumentGenerator Component', () => {
  const mockTemplates = [
    { id: 1, name: 'Demand Letter', description: 'Template for legal demand letters' },
    { id: 2, name: 'Divorce Petition', description: 'Template for divorce petitions' },
    { id: 3, name: 'Will', description: 'Template for wills and testaments' },
    { id: 4, name: 'Power of Attorney', description: 'Template for power of attorney documents' },
    { id: 5, name: 'Eviction Notice', description: 'Template for eviction notices' },
  ];

  beforeEach(() => {
    // Mock the API responses
    axios.get.mockResolvedValueOnce({ data: mockTemplates });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders DocumentGenerator component with template list', async () => {
    render(<DocumentGenerator />);

    // Check loading state is displayed initially
    expect(screen.getByText(/loading templates/i)).toBeInTheDocument();

    // Wait for templates to load
    await waitFor(() => {
      expect(screen.getByText('Demand Letter')).toBeInTheDocument();
      expect(screen.getByText('Divorce Petition')).toBeInTheDocument();
      expect(screen.getByText('Will')).toBeInTheDocument();
    });

    // Check that all templates are rendered
    mockTemplates.forEach(template => {
      expect(screen.getByText(template.name)).toBeInTheDocument();
      expect(screen.getByText(template.description)).toBeInTheDocument();
    });
  });

  test('handles template selection and form display', async () => {
    render(<DocumentGenerator />);

    // Wait for templates to load
    await waitFor(() => {
      expect(screen.getByText('Demand Letter')).toBeInTheDocument();
    });

    // Select a template
    const demandLetterCard = screen.getByText('Demand Letter').closest('button');
    fireEvent.click(demandLetterCard);

    // Check that form is displayed after template selection
    expect(screen.getByText('Document Information')).toBeInTheDocument();

    // Check for common form fields
    expect(screen.getByLabelText(/recipient name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/address/i)).toBeInTheDocument();
  });

  test('handles form submission and document generation', async () => {
    // Mock the API response for document generation
    axios.post.mockResolvedValueOnce({
      data: {
        documentId: 'doc123',
        downloadUrl: '/api/documents/doc123/download',
        message: 'Document generated successfully',
      },
    });

    render(<DocumentGenerator />);

    // Wait for templates to load
    await waitFor(() => {
      expect(screen.getByText('Demand Letter')).toBeInTheDocument();
    });

    // Select a template
    const demandLetterCard = screen.getByText('Demand Letter').closest('button');
    fireEvent.click(demandLetterCard);

    // Fill out form
    await userEvent.type(screen.getByLabelText(/recipient name/i), 'John Doe');
    await userEvent.type(screen.getByLabelText(/address/i), '123 Main St');

    // Submit form
    const generateButton = screen.getByRole('button', { name: /generate document/i });
    fireEvent.click(generateButton);

    // Check that loading state is shown during generation
    expect(screen.getByText(/generating document/i)).toBeInTheDocument();

    // Wait for success message after generation
    await waitFor(() => {
      expect(screen.getByText(/document generated successfully/i)).toBeInTheDocument();
      expect(screen.getByText(/download document/i)).toBeInTheDocument();
    });

    // Verify API was called correctly
    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/api/document-generator/generate'),
      expect.objectContaining({
        templateId: 1,
        data: expect.objectContaining({
          recipientName: 'John Doe',
          recipientAddress: '123 Main St',
        }),
      }),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: 'Bearer mock-token',
        }),
      })
    );
  });

  test('displays error message when document generation fails', async () => {
    // Mock a failed API response
    axios.get.mockResolvedValueOnce({ data: mockTemplates });
    axios.post.mockRejectedValueOnce({
      response: {
        status: 500,
        data: { message: 'Server error while generating document' },
      },
    });

    render(<DocumentGenerator />);

    // Wait for templates to load
    await waitFor(() => {
      expect(screen.getByText('Demand Letter')).toBeInTheDocument();
    });

    // Select a template
    const demandLetterCard = screen.getByText('Demand Letter').closest('button');
    fireEvent.click(demandLetterCard);

    // Fill out form minimally
    await userEvent.type(screen.getByLabelText(/recipient name/i), 'John Doe');

    // Submit form
    const generateButton = screen.getByRole('button', { name: /generate document/i });
    fireEvent.click(generateButton);

    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(/error generating document/i)).toBeInTheDocument();
      expect(screen.getByText(/server error while generating document/i)).toBeInTheDocument();
    });
  });

  test('handles empty template list scenario', async () => {
    // Override the mock to return empty array
    axios.get.mockResolvedValueOnce({ data: [] });

    render(<DocumentGenerator />);

    // Wait for no templates message
    await waitFor(() => {
      expect(screen.getByText(/no document templates available/i)).toBeInTheDocument();
    });
  });
});
