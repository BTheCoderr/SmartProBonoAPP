import ReactGA from 'react-ga4';
import { ErrorBoundary } from 'react-error-boundary';

interface EventParams {
    category?: string;
    action: string;
    label?: string;
    value?: number;
    nonInteraction?: boolean;
    [key: string]: any;
}

class AnalyticsService {
    private initialized: boolean = false;
    private measurementId: string;

    constructor(measurementId: string) {
        this.measurementId = measurementId;
    }

    initialize(): void {
        if (!this.initialized) {
            ReactGA.initialize(this.measurementId, {
                testMode: process.env.NODE_ENV !== 'production',
                gaOptions: {
                    siteSpeedSampleRate: 100,
                    enableWebVitals: true
                }
            });
            this.initialized = true;
        }
    }

    trackPageView(path: string): void {
        if (!this.initialized) return;
        ReactGA.send({ hitType: "pageview", page: path });
    }

    trackEvent(params: EventParams): void {
        if (!this.initialized) return;
        ReactGA.event({
            category: params.category || 'General',
            action: params.action,
            label: params.label,
            value: params.value,
            nonInteraction: params.nonInteraction,
            ...params
        });
    }

    trackDocumentGeneration(documentType: string, processingTime: number, success: boolean): void {
        this.trackEvent({
            category: 'Document',
            action: success ? 'Generation Success' : 'Generation Failure',
            label: documentType,
            value: processingTime,
            documentType,
            processingTime,
            success
        });
    }

    trackFormCompletion(formType: string, completionTime: number, stepCount: number): void {
        this.trackEvent({
            category: 'Form',
            action: 'Completion',
            label: formType,
            value: completionTime,
            formType,
            stepCount
        });
    }

    trackFormStep(formType: string, stepNumber: number, stepName: string): void {
        this.trackEvent({
            category: 'Form',
            action: 'Step Completion',
            label: `${formType} - Step ${stepNumber}`,
            stepName
        });
    }

    trackSearch(query: string, resultsCount: number, category?: string): void {
        this.trackEvent({
            category: 'Search',
            action: 'Query',
            label: category || 'General',
            value: resultsCount,
            query,
            resultsCount
        });
    }

    trackError(error: Error, componentStack: string): void {
        this.trackEvent({
            category: 'Error',
            action: 'JavaScript Error',
            label: error.message,
            error: {
                name: error.name,
                message: error.message,
                stack: error.stack,
                componentStack
            }
        });
    }

    trackUserEngagement(duration: number, pagesVisited: number): void {
        this.trackEvent({
            category: 'Engagement',
            action: 'Session End',
            value: duration,
            pagesVisited
        });
    }

    trackDocumentDownload(documentId: string, documentType: string): void {
        this.trackEvent({
            category: 'Document',
            action: 'Download',
            label: documentType,
            documentId
        });
    }
}

// Create analytics instance with measurement ID from config
const analytics = new AnalyticsService(process.env.REACT_APP_GA_MEASUREMENT_ID || '');

// Error Boundary component for tracking errors
export const AnalyticsErrorBoundary: React.FC = ({ children }) => (
    <ErrorBoundary
        onError={(error, componentStack) => {
            analytics.trackError(error, componentStack);
        }}
        fallback={<div>Something went wrong. Please try again.</div>}
    >
        {children}
    </ErrorBoundary>
);

export default analytics; 