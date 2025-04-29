import ReactGA from 'react-ga4';
import { ErrorBoundary, FallbackProps } from 'react-error-boundary';
import React from 'react';

interface AnalyticsConfig {
    trackingId: string;
    debug?: boolean;
}

class AnalyticsService {
    private static instance: AnalyticsService;
    private initialized: boolean = false;

    private constructor() {}

    public static getInstance(): AnalyticsService {
        if (!AnalyticsService.instance) {
            AnalyticsService.instance = new AnalyticsService();
        }
        return AnalyticsService.instance;
    }

    public init(config: AnalyticsConfig): void {
        if (!this.initialized) {
            ReactGA.initialize(config.trackingId, { debug: config.debug });
            this.initialized = true;
        }
    }

    public trackPageView(path: string): void {
        if (this.initialized) {
            ReactGA.send({ hitType: "pageview", page: path });
        }
    }

    public trackEvent(category: string, action: string, label?: string, value?: number): void {
        if (this.initialized) {
            ReactGA.event({
                category,
                action,
                label,
                value,
            });
        }
    }

    public trackError(error: Error, componentStack?: string): void {
        if (this.initialized) {
            ReactGA.event({
                category: 'Error',
                action: 'Application Error',
                label: `${error.message} | Stack: ${componentStack || 'N/A'}`,
            });
        }
    }
}

const analytics = AnalyticsService.getInstance();

export const ErrorBoundaryWithAnalytics: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const handleError = (error: Error, info: { componentStack: string }) => {
        analytics.trackError(error, info.componentStack);
    };

    return (
        <ErrorBoundary
            FallbackComponent={({ error }: FallbackProps) => (
                <div>Something went wrong. Please try again.</div>
            )}
            onError={handleError}
        >
            {children}
        </ErrorBoundary>
    );
};

export { analytics };
export default analytics; 