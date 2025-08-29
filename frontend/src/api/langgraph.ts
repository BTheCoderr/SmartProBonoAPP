// LangGraph API integration for SmartProBono
const LANGGRAPH_URL = process.env.REACT_APP_LANGGRAPH_URL || 'http://localhost:8010';

export interface IntakeRequest {
  user_id?: string | null;
  full_text: string;
  meta?: Record<string, any>;
}

export interface IntakeResponse {
  result: {
    intake_id: string;
    user_id?: string | null;
    raw_text: string;
    summary?: string;
    status: string;
    meta?: Record<string, any>;
  };
}

export class LangGraphAPI {
  private baseUrl: string;

  constructor(baseUrl: string = LANGGRAPH_URL) {
    this.baseUrl = baseUrl;
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      const data = await response.json();
      return data.ok === true;
    } catch (error) {
      console.error('LangGraph health check failed:', error);
      return false;
    }
  }

  async runIntake(request: IntakeRequest): Promise<IntakeResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/intake/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('LangGraph intake failed:', error);
      throw error;
    }
  }
}

// Export a default instance
export const langGraphAPI = new LangGraphAPI();
