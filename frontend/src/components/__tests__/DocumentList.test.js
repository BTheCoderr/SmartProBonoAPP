import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChakraProvider } from '@chakra-ui/react';
import DocumentList from '../DocumentList';
import {
  getCaseDocuments,
  uploadDocument,
  downloadDocument,
  deleteDocument,
  shareDocument,
  getDocumentVersions,
  restoreDocumentVersion,
} from '../../services/documentService';

// Mock the documentService
jest.mock('../../services/documentService');

const mockDocuments = [
  {
    id: '1',
    title: 'Test Document 1',
    type: 'PDF',
    size: 1024 * 1024, // 1MB
    uploaded_at: '2024-05-29T12:00:00Z',
  },
  {
    id: '2',
    title: 'Test Document 2',
    type: 'DOCX',
    size: 512 * 1024, // 512KB
    uploaded_at: '2024-05-28T12:00:00Z',
  },
];

const mockVersions = [
  {
    id: '1',
    version_number: 1,
    created_at: '2024-05-29T12:00:00Z',
    size: 1024 * 1024,
  },
  {
    id: '2',
    version_number: 2,
    created_at: '2024-05-29T13:00:00Z',
    size: 1024 * 1024,
  },
];

describe('DocumentList', () => {
  const caseId = '123';

  beforeEach(() => {
    getCaseDocuments.mockResolvedValue(mockDocuments);
    getDocumentVersions.mockResolvedValue(mockVersions);
    uploadDocument.mockResolvedValue({});
    downloadDocument.mockResolvedValue(new Blob());
    deleteDocument.mockResolvedValue({});
    shareDocument.mockResolvedValue({});
    restoreDocumentVersion.mockResolvedValue({});
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders the document list with documents', async () => {
    render(
      <ChakraProvider>
        <DocumentList caseId={caseId} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getCaseDocuments).toHaveBeenCalledWith(caseId);
    });

    expect(screen.getByText('Test Document 1')).toBeInTheDocument();
    expect(screen.getByText('Test Document 2')).toBeInTheDocument();
    expect(screen.getByText('PDF')).toBeInTheDocument();
    expect(screen.getByText('DOCX')).toBeInTheDocument();
  });

  it('handles document upload', async () => {
    render(
      <ChakraProvider>
        <DocumentList caseId={caseId} />
      </ChakraProvider>
    );

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const uploadButton = screen.getByText('Upload Document');
    const fileInput = screen.getByRole('button', { name: 'Upload Document' }).previousSibling;

    Object.defineProperty(fileInput, 'files', {
      value: [file],
    });

    fireEvent.click(uploadButton);
    fireEvent.change(fileInput);

    await waitFor(() => {
      expect(screen.getByText('Upload Document')).toBeInTheDocument();
    });

    const titleInput = screen.getByLabelText('Title');
    const descriptionInput = screen.getByLabelText('Description');
    fireEvent.change(titleInput, { target: { value: 'New Document' } });
    fireEvent.change(descriptionInput, { target: { value: 'Test description' } });

    const submitButton = screen.getByRole('button', { name: 'Upload' });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(uploadDocument).toHaveBeenCalledWith(
        caseId,
        file,
        expect.objectContaining({
          title: 'New Document',
          description: 'Test description',
        })
      );
    });
  });

  it('handles document download', async () => {
    render(
      <ChakraProvider>
        <DocumentList caseId={caseId} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getCaseDocuments).toHaveBeenCalled();
    });

    const menuButtons = screen.getAllByRole('button', { name: /more/i });
    fireEvent.click(menuButtons[0]);

    const downloadButton = screen.getByText('Download');
    fireEvent.click(downloadButton);

    await waitFor(() => {
      expect(downloadDocument).toHaveBeenCalledWith(caseId, '1');
    });
  });

  it('handles document sharing', async () => {
    render(
      <ChakraProvider>
        <DocumentList caseId={caseId} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getCaseDocuments).toHaveBeenCalled();
    });

    const menuButtons = screen.getAllByRole('button', { name: /more/i });
    fireEvent.click(menuButtons[0]);

    const shareButton = screen.getByText('Share');
    fireEvent.click(shareButton);

    const emailInput = screen.getByPlaceholderText("Enter recipient's email");
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });

    const submitButton = screen.getByRole('button', { name: 'Share' });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(shareDocument).toHaveBeenCalledWith(caseId, '1', {
        email: 'test@example.com',
      });
    });
  });

  it('handles document deletion', async () => {
    render(
      <ChakraProvider>
        <DocumentList caseId={caseId} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getCaseDocuments).toHaveBeenCalled();
    });

    const menuButtons = screen.getAllByRole('button', { name: /more/i });
    fireEvent.click(menuButtons[0]);

    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(deleteDocument).toHaveBeenCalledWith(caseId, '1');
      expect(getCaseDocuments).toHaveBeenCalledTimes(2);
    });
  });

  it('handles version management', async () => {
    render(
      <ChakraProvider>
        <DocumentList caseId={caseId} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(getCaseDocuments).toHaveBeenCalled();
    });

    const menuButtons = screen.getAllByRole('button', { name: /more/i });
    fireEvent.click(menuButtons[0]);

    const versionsButton = screen.getByText('Versions');
    fireEvent.click(versionsButton);

    await waitFor(() => {
      expect(getDocumentVersions).toHaveBeenCalledWith(caseId, '1');
      expect(screen.getByText('v1')).toBeInTheDocument();
      expect(screen.getByText('v2')).toBeInTheDocument();
    });

    const restoreButtons = screen.getAllByText('Restore');
    fireEvent.click(restoreButtons[0]);

    await waitFor(() => {
      expect(restoreDocumentVersion).toHaveBeenCalledWith(caseId, '1', '1');
      expect(getCaseDocuments).toHaveBeenCalledTimes(2);
    });
  });

  it('handles API errors gracefully', async () => {
    const error = new Error('Failed to fetch documents');
    getCaseDocuments.mockRejectedValue(error);

    render(
      <ChakraProvider>
        <DocumentList caseId={caseId} />
      </ChakraProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument();
      expect(screen.getByText('Failed to fetch documents')).toBeInTheDocument();
    });
  });
});
