import { run_pipeline } from '../../../legal_ai_backend/langgraph/main_graph';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { text, jurisdiction } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }

    // Run the LangGraph pipeline
    const result = await run_pipeline({ 
      query: text, 
      jurisdiction: jurisdiction || 'ri' 
    });
    
    res.status(200).json({ 
      success: true, 
      result: result,
      analysis: result.analysis || {},
      disclaimers: result.disclaimers || [],
      warnings: result.warnings || [],
      recommendations: result.recommendations || []
    });
  } catch (error) {
    console.error('Error in searchCase API:', error);
    res.status(500).json({ 
      success: false, 
      error: 'Internal server error',
      analysis: {},
      disclaimers: ["This analysis is for informational purposes only and does not constitute legal advice."],
      warnings: [],
      recommendations: []
    });
  }
}
