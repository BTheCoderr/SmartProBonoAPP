import { renderHook, act } from '@testing-library/react-hooks';
import useFormRecovery from '../useFormRecovery';
import ApiService from '../../services/ApiService';

jest.mock('../../services/ApiService');

describe('useFormRecovery', () => {
    const mockFormType = 'small_claims';
    const mockInitialValues = {
        plaintiff_name: '',
        claim_amount: 0
    };
    const mockDraftData = {
        values: {
            plaintiff_name: 'John Doe',
            claim_amount: 5000
        },
        timestamp: Date.now()
    };

    beforeEach(() => {
        localStorage.clear();
        jest.clearAllMocks();
    });

    it('should load local draft if available', async () => {
        // Setup local storage draft
        localStorage.setItem(
            `${mockFormType}FormDraft`,
            JSON.stringify(mockDraftData)
        );

        const { result, waitForNextUpdate } = renderHook(() =>
            useFormRecovery(mockFormType, mockInitialValues)
        );

        await waitForNextUpdate();

        expect(result.current.recoveredData).toEqual(mockDraftData);
        expect(result.current.lastAutoSave).toEqual(mockDraftData);
        expect(result.current.isRecovering).toBe(false);
    });

    it('should load server draft if no local draft exists', async () => {
        const serverDraftData = {
            ...mockDraftData,
            timestamp: Date.now() + 1000
        };

        ApiService.get.mockResolvedValueOnce({ data: serverDraftData });

        const { result, waitForNextUpdate } = renderHook(() =>
            useFormRecovery(mockFormType, mockInitialValues)
        );

        await waitForNextUpdate();

        expect(result.current.recoveredData).toEqual(serverDraftData);
        expect(result.current.lastAutoSave).toEqual(serverDraftData);
        expect(result.current.isRecovering).toBe(false);
    });

    it('should save recovery point locally and to server', async () => {
        ApiService.post.mockResolvedValueOnce({ data: { success: true } });

        const { result } = renderHook(() =>
            useFormRecovery(mockFormType, mockInitialValues)
        );

        await act(async () => {
            await result.current.saveRecoveryPoint(mockDraftData.values);
        });

        // Check local storage
        const savedLocal = JSON.parse(
            localStorage.getItem(`${mockFormType}FormDraft`)
        );
        expect(savedLocal.values).toEqual(mockDraftData.values);

        // Check API call
        expect(ApiService.post).toHaveBeenCalledWith(
            `/api/drafts/${mockFormType}`,
            expect.objectContaining({
                values: mockDraftData.values
            })
        );
    });

    it('should clear recovery data from local storage and server', async () => {
        // Setup initial data
        localStorage.setItem(
            `${mockFormType}FormDraft`,
            JSON.stringify(mockDraftData)
        );

        ApiService.delete.mockResolvedValueOnce({ data: { success: true } });

        const { result } = renderHook(() =>
            useFormRecovery(mockFormType, mockInitialValues)
        );

        await act(async () => {
            await result.current.clearRecoveryData();
        });

        // Check local storage is cleared
        expect(localStorage.getItem(`${mockFormType}FormDraft`)).toBeNull();

        // Check API call
        expect(ApiService.delete).toHaveBeenCalledWith(
            `/api/drafts/${mockFormType}`
        );
    });

    it('should handle errors gracefully', async () => {
        const consoleError = jest.spyOn(console, 'error').mockImplementation();
        ApiService.get.mockRejectedValueOnce(new Error('API Error'));

        const { result, waitForNextUpdate } = renderHook(() =>
            useFormRecovery(mockFormType, mockInitialValues)
        );

        await waitForNextUpdate();

        expect(result.current.isRecovering).toBe(false);
        expect(consoleError).toHaveBeenCalled();

        consoleError.mockRestore();
    });
}); 