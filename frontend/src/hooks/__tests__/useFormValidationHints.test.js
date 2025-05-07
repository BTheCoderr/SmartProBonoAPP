import { renderHook, act } from '@testing-library/react-hooks';
import useFormValidationHints from '../useFormValidationHints';
import * as Yup from 'yup';

describe('useFormValidationHints', () => {
    const mockValidationSchema = Yup.object().shape({
        name: Yup.string()
            .required('Name is required')
            .min(2, 'Name must be at least 2 characters'),
        email: Yup.string()
            .required('Email is required')
            .email('Must be a valid email'),
        amount: Yup.number()
            .required('Amount is required')
            .positive('Must be a positive number')
    });

    const mockFormik = {
        values: {
            name: '',
            email: '',
            amount: ''
        },
        touched: {},
        errors: {}
    };

    beforeEach(() => {
        document.body.innerHTML = `
            <input name="name" />
            <input name="email" />
            <input name="amount" />
        `;
    });

    it('should generate field hints based on validation schema', () => {
        const { result } = renderHook(() =>
            useFormValidationHints(mockFormik, mockValidationSchema)
        );

        const nameHints = result.current.getFieldHint('name');
        expect(nameHints).toContain('This field is required');
        expect(nameHints).toContain('Minimum 2 characters');

        const emailHints = result.current.getFieldHint('email');
        expect(emailHints).toContain('This field is required');
        expect(emailHints).toContain('Must be a valid email address');

        const amountHints = result.current.getFieldHint('amount');
        expect(amountHints).toContain('This field is required');
        expect(amountHints).toContain('Must be a positive number');
    });

    it('should track field completion times', async () => {
        const { result } = renderHook(() =>
            useFormValidationHints(mockFormik, mockValidationSchema)
        );

        const nameInput = document.querySelector('[name="name"]');

        // Simulate field focus and completion
        act(() => {
            nameInput.dispatchEvent(new Event('focus'));
        });

        // Wait for some time
        await new Promise(resolve => setTimeout(resolve, 1000));

        act(() => {
            nameInput.dispatchEvent(new Event('blur'));
        });

        const fieldTime = result.current.getEstimatedTimeForField('name');
        expect(fieldTime).toBeGreaterThan(0);
    });

    it('should calculate estimated completion time', async () => {
        const { result } = renderHook(() =>
            useFormValidationHints({
                ...mockFormik,
                values: {
                    name: 'John',
                    email: '',
                    amount: ''
                },
                touched: {
                    name: true,
                    email: true,
                    amount: true
                }
            }, mockValidationSchema)
        );

        const nameInput = document.querySelector('[name="name"]');
        const emailInput = document.querySelector('[name="email"]');

        // Simulate completing name field
        act(() => {
            nameInput.dispatchEvent(new Event('focus'));
        });
        await new Promise(resolve => setTimeout(resolve, 1000));
        act(() => {
            nameInput.dispatchEvent(new Event('blur'));
        });

        // Simulate completing email field
        act(() => {
            emailInput.dispatchEvent(new Event('focus'));
        });
        await new Promise(resolve => setTimeout(resolve, 1500));
        act(() => {
            emailInput.dispatchEvent(new Event('blur'));
        });

        const estimatedTime = result.current.getFormattedEstimatedTime();
        expect(estimatedTime).toMatch(/\d+ minutes?/);
    });

    it('should filter hints based on field state', () => {
        const { result } = renderHook(() =>
            useFormValidationHints({
                ...mockFormik,
                values: {
                    name: 'J', // Too short
                    email: 'invalid-email', // Invalid format
                    amount: '-5' // Negative number
                },
                touched: {
                    name: true,
                    email: true,
                    amount: true
                },
                errors: {
                    name: 'Name must be at least 2 characters',
                    email: 'Must be a valid email',
                    amount: 'Must be a positive number'
                }
            }, mockValidationSchema)
        );

        const nameHints = result.current.getFieldHint('name');
        expect(nameHints).toContain('Minimum 2 characters');
        expect(nameHints).not.toContain('This field is required');

        const emailHints = result.current.getFieldHint('email');
        expect(emailHints).toContain('Must be a valid email address');
        expect(emailHints).not.toContain('This field is required');

        const amountHints = result.current.getFieldHint('amount');
        expect(amountHints).toContain('Must be a positive number');
        expect(amountHints).not.toContain('This field is required');
    });
}); 