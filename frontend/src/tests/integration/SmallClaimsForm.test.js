import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { act } from 'react-dom/test-utils';
import { MemoryRouter } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';
import SmallClaimsComplaintForm from '../../pages/SmallClaimsComplaintForm';
import ApiService from '../../services/ApiService';

jest.mock('../../services/ApiService');

describe('SmallClaimsComplaintForm Integration', () => {
    const mockNavigate = jest.fn();

    beforeEach(() => {
        jest.clearAllMocks();
        localStorage.clear();

        // Mock react-router-dom's useNavigate
        jest.mock('react-router-dom', () => ({
            ...jest.requireActual('react-router-dom'),
            useNavigate: () => mockNavigate
        }));
    });

    const renderForm = () => {
        return render(
            <MemoryRouter>
                <SnackbarProvider>
                    <SmallClaimsComplaintForm />
                </SnackbarProvider>
            </MemoryRouter>
        );
    };

    const fillFormStep = async (step, values) => {
        for (const [fieldName, value] of Object.entries(values)) {
            const input = screen.getByLabelText(fieldName, { exact: false });
            await userEvent.type(input, value);
        }
    };

    it('should complete full form submission flow', async () => {
        ApiService.post.mockResolvedValueOnce({ data: { documentId: '123' } });
        
        renderForm();

        // Step 1: Court Information
        await fillFormStep(1, {
            'Court County': 'Sample County',
            'Court State': 'Sample State'
        });
        fireEvent.click(screen.getByText('Next'));

        // Step 2: Party Information
        await fillFormStep(2, {
            'Plaintiff Name': 'John Doe',
            'Plaintiff Address': '123 Main St',
            'Defendant Name': 'Jane Smith',
            'Defendant Address': '456 Oak Ave'
        });
        fireEvent.click(screen.getByText('Next'));

        // Step 3: Claim Information
        await fillFormStep(3, {
            'Claim Amount': '5000',
            'Claim Description': 'Sample claim description',
            'Incident Location': 'Sample Location'
        });
        fireEvent.click(screen.getByText('Next'));

        // Step 4: Facts and Evidence
        await fillFormStep(4, {
            'Fact 1': 'Sample fact 1',
            'Evidence List': 'Sample evidence',
            'Witness List': 'Sample witness'
        });

        // Submit form
        await act(async () => {
            fireEvent.click(screen.getByText('Submit'));
        });

        await waitFor(() => {
            expect(ApiService.post).toHaveBeenCalledWith(
                '/api/templates/generate',
                expect.objectContaining({
                    template_id: 'small_claims_complaint',
                    data: expect.objectContaining({
                        court_county: 'Sample County',
                        plaintiff_name: 'John Doe',
                        claim_amount: '5000'
                    })
                })
            );
        });

        expect(mockNavigate).toHaveBeenCalledWith(
            '/documents',
            expect.objectContaining({
                state: expect.objectContaining({
                    documentId: '123'
                })
            })
        );
    });

    it('should handle form validation errors', async () => {
        renderForm();

        // Try to proceed without filling required fields
        fireEvent.click(screen.getByText('Next'));

        await waitFor(() => {
            expect(screen.getByText('County is required')).toBeInTheDocument();
            expect(screen.getByText('State is required')).toBeInTheDocument();
        });
    });

    it('should handle API errors gracefully', async () => {
        ApiService.post.mockRejectedValueOnce(new Error('API Error'));
        
        renderForm();

        // Fill minimum required fields
        await fillFormStep(1, {
            'Court County': 'Sample County',
            'Court State': 'Sample State'
        });
        fireEvent.click(screen.getByText('Next'));

        await fillFormStep(2, {
            'Plaintiff Name': 'John Doe',
            'Plaintiff Address': '123 Main St',
            'Defendant Name': 'Jane Smith',
            'Defendant Address': '456 Oak Ave'
        });
        fireEvent.click(screen.getByText('Next'));

        await fillFormStep(3, {
            'Claim Amount': '5000',
            'Claim Description': 'Sample description'
        });
        fireEvent.click(screen.getByText('Next'));

        await fillFormStep(4, {
            'Fact 1': 'Sample fact'
        });

        // Submit form
        await act(async () => {
            fireEvent.click(screen.getByText('Submit'));
        });

        await waitFor(() => {
            expect(screen.getByText('Failed to submit form. Please try again.')).toBeInTheDocument();
        });
    });

    it('should save and recover draft', async () => {
        const mockDraft = {
            values: {
                court_county: 'Draft County',
                court_state: 'Draft State'
            },
            timestamp: Date.now()
        };

        // Setup draft in localStorage
        localStorage.setItem('small_claims_form_draft', JSON.stringify(mockDraft));

        renderForm();

        await waitFor(() => {
            expect(screen.getByLabelText('Court County')).toHaveValue('Draft County');
            expect(screen.getByLabelText('Court State')).toHaveValue('Draft State');
        });

        // Update a field
        await userEvent.type(screen.getByLabelText('Court County'), ' Updated');

        // Save draft
        fireEvent.click(screen.getByText('Save Draft'));

        await waitFor(() => {
            expect(screen.getByText('Draft saved successfully')).toBeInTheDocument();
        });

        const savedDraft = JSON.parse(localStorage.getItem('small_claims_form_draft'));
        expect(savedDraft.values.court_county).toBe('Draft County Updated');
    });

    it('should show form completion progress', async () => {
        renderForm();

        // Initially 0%
        expect(screen.getByText('Form Progress: 0%')).toBeInTheDocument();

        // Fill some fields
        await fillFormStep(1, {
            'Court County': 'Sample County',
            'Court State': 'Sample State'
        });

        // Should show increased progress
        await waitFor(() => {
            expect(screen.getByText(/Form Progress: \d+%/)).toBeInTheDocument();
        });
    });

    it('should handle document preview', async () => {
        ApiService.post.mockResolvedValueOnce({ 
            data: { previewUrl: 'mock-preview-url' } 
        });

        renderForm();

        // Fill all steps
        await fillFormStep(1, {
            'Court County': 'Sample County',
            'Court State': 'Sample State'
        });
        fireEvent.click(screen.getByText('Next'));

        await fillFormStep(2, {
            'Plaintiff Name': 'John Doe',
            'Plaintiff Address': '123 Main St',
            'Defendant Name': 'Jane Smith',
            'Defendant Address': '456 Oak Ave'
        });
        fireEvent.click(screen.getByText('Next'));

        await fillFormStep(3, {
            'Claim Amount': '5000',
            'Claim Description': 'Sample description'
        });
        fireEvent.click(screen.getByText('Next'));

        await fillFormStep(4, {
            'Fact 1': 'Sample fact'
        });

        // Click preview button
        fireEvent.click(screen.getByText('Preview'));

        await waitFor(() => {
            expect(ApiService.post).toHaveBeenCalledWith(
                '/api/templates/preview',
                expect.any(Object)
            );
            expect(screen.getByAltText('Document Preview')).toBeInTheDocument();
        });
    });
}); 