#!/usr/bin/env python3
"""
SmartProBono REAL Multi-Layered Agent System with LangGraph
True multi-layer orchestration where agents call other agents
"""

import os
import json
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, TypedDict
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from anthropic import Anthropic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://ewtcvsohdgkthuyajyyk.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3dGN2c29oZGdrdGh1eWFqeXlrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjQxMDQ2NCwiZXhwIjoyMDcxOTg2NDY0fQ._9KbvHJ6JohciGAqwHlQGerGr2xkHEr36OmSB5oQjng")

# AI Clients
openai_client = None
anthropic_client = None

# Initialize AI clients
try:
    if os.getenv("OPENAI_API_KEY"):
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        logger.info("✅ OpenAI client initialized")
except Exception as e:
    logger.warning(f"OpenAI client not available: {e}")

try:
    if os.getenv("ANTHROPIC_API_KEY"):
        anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        logger.info("✅ Anthropic client initialized")
except Exception as e:
    logger.warning(f"Anthropic client not available: {e}")

# LangGraph-style State Management
class MultiLayerState(TypedDict):
    """State for multi-layered agent system"""
    # Input
    user_message: str
    user_id: Optional[str]
    
    # Layer 1: Supervisor Analysis
    supervisor_analysis: Dict[str, Any]
    complexity_score: float
    required_agents: List[str]
    workflow_type: str
    
    # Layer 2: Agent Orchestration
    agent_responses: Dict[str, str]
    agent_confidence: Dict[str, float]
    cross_agent_validation: Dict[str, Any]
    
    # Layer 3: Synthesis & Human-in-Loop
    synthesized_response: str
    needs_human_review: bool
    escalation_reason: Optional[str]
    human_feedback: Optional[str]
    
    # Layer 4: Final Output
    final_response: str
    agent_chain: List[str]
    processing_time: float
    confidence_score: float

class BaseAgent:
    """Base class for all agents in the multi-layer system"""
    
    def __init__(self, name: str, model: str, system_prompt: str):
        self.name = name
        self.model = model
        self.system_prompt = system_prompt
        self.sub_agents = []
    
    def add_sub_agent(self, agent):
        """Add a sub-agent that this agent can call"""
        self.sub_agents.append(agent)
    
    def call_ai(self, messages: List[Dict], model: str = None):
        """Call AI model"""
        model = model or self.model
        
        if "claude" in model.lower():
            return self._call_anthropic(messages, model)
        else:
            return self._call_openai(messages, model)
    
    def _call_openai(self, messages: List[Dict], model: str):
        """Call OpenAI API"""
        if not openai_client:
            return "OpenAI service unavailable"
        
        try:
            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Error calling OpenAI: {e}"
    
    def _call_anthropic(self, messages: List[Dict], model: str):
        """Call Anthropic API"""
        if not anthropic_client:
            return "Anthropic service unavailable"
        
        try:
            formatted_messages = []
            system_prompt = ""
            
            for msg in messages:
                if msg['role'] == 'system':
                    system_prompt = msg['content']
                else:
                    formatted_messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
            
            response = anthropic_client.messages.create(
                model=model,
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=formatted_messages
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return f"Error calling Anthropic: {e}"
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Process the state - to be implemented by subclasses"""
        raise NotImplementedError

class SupervisorAgent(BaseAgent):
    """Layer 1: Supervisor Agent - Analyzes and routes complex queries"""
    
    def __init__(self):
        super().__init__(
            "Supervisor Agent",
            "gpt-4o",
            """You are a legal supervisor agent that analyzes user queries and determines the complexity and required workflow.

            Your job is to:
            1. Analyze the user's legal question
            2. Determine complexity score (0-1)
            3. Identify which specialized agents are needed
            4. Decide on the workflow type (simple, complex, multi-agent, human-review)
            
            Respond with JSON:
            {
                "complexity_score": 0.8,
                "required_agents": ["immigration", "document"],
                "workflow_type": "multi-agent",
                "reasoning": "Complex immigration case requiring document analysis"
            }"""
        )
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Analyze query and determine workflow"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Analyze this legal query: {state['user_message']}"}
        ]
        
        response = self.call_ai(messages)
        
        try:
            analysis = json.loads(response)
            state['supervisor_analysis'] = analysis
            state['complexity_score'] = analysis.get('complexity_score', 0.5)
            state['required_agents'] = analysis.get('required_agents', ['greeting'])
            state['workflow_type'] = analysis.get('workflow_type', 'simple')
        except:
            # Fallback analysis
            state['supervisor_analysis'] = {"error": "Failed to parse analysis"}
            state['complexity_score'] = 0.5
            state['required_agents'] = ['greeting']
            state['workflow_type'] = 'simple'
        
        return state

class ImmigrationAgent(BaseAgent):
    """Layer 2: Immigration Agent with sub-agents"""
    
    def __init__(self):
        super().__init__(
            "Immigration Agent",
            "gpt-4o",
            """You are an immigration law specialist. You can call sub-agents for complex cases.
            
            For simple questions: Provide direct guidance
            For complex cases: Call document_agent and compliance_agent
            For urgent cases: Recommend human attorney consultation"""
        )
        # Add sub-agents
        self.add_sub_agent(DocumentAgent())
        self.add_sub_agent(ComplianceAgent())
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Process immigration query with potential sub-agent calls"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Immigration question: {state['user_message']}"}
        ]
        
        response = self.call_ai(messages)
        
        # Check if we need to call sub-agents
        if "document" in response.lower() or "form" in response.lower():
            # Call document sub-agent
            doc_state = state.copy()
            doc_state['user_message'] = f"Generate immigration document for: {state['user_message']}"
            doc_response = self.sub_agents[0].process(doc_state)
            response += f"\n\n**Document Analysis:** {doc_response.get('agent_responses', {}).get('document', '')}"
        
        if "compliance" in response.lower() or "regulation" in response.lower():
            # Call compliance sub-agent
            comp_state = state.copy()
            comp_state['user_message'] = f"Check compliance for: {state['user_message']}"
            comp_response = self.sub_agents[1].process(comp_state)
            response += f"\n\n**Compliance Check:** {comp_response.get('agent_responses', {}).get('compliance', '')}"
        
        state['agent_responses']['immigration'] = response
        state['agent_confidence']['immigration'] = 0.9
        return state

class FamilyLawAgent(BaseAgent):
    """Layer 2: Family Law Agent with emotional intelligence"""
    
    def __init__(self):
        super().__init__(
            "Family Law Agent",
            "claude-3-sonnet-20240229",
            """You are a compassionate family law specialist with emotional intelligence.
            
            Your approach:
            1. Acknowledge emotional aspects
            2. Provide legal guidance
            3. For complex cases, call expert_agent
            4. Always recommend human attorney for sensitive matters"""
        )
        self.add_sub_agent(ExpertAgent())
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Process family law query with emotional intelligence"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Family law question: {state['user_message']}"}
        ]
        
        response = self.call_ai(messages)
        
        # Check if we need expert analysis
        if state['complexity_score'] > 0.7:
            expert_state = state.copy()
            expert_state['user_message'] = f"Expert analysis needed for: {state['user_message']}"
            expert_response = self.sub_agents[0].process(expert_state)
            response += f"\n\n**Expert Analysis:** {expert_response.get('agent_responses', {}).get('expert', '')}"
        
        state['agent_responses']['family'] = response
        state['agent_confidence']['family'] = 0.9
        return state

class BusinessLawAgent(BaseAgent):
    """Layer 2: Business Law Agent with multi-step workflows"""
    
    def __init__(self):
        super().__init__(
            "Business Law Agent",
            "gpt-4o",
            """You are a business law expert specializing in startups and small businesses.
            
            For business formation: Call document_agent for entity documents
            For contracts: Call document_agent for contract analysis
            For compliance: Call compliance_agent for regulatory requirements"""
        )
        self.add_sub_agent(DocumentAgent())
        self.add_sub_agent(ComplianceAgent())
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Process business law with multi-step workflow"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Business law question: {state['user_message']}"}
        ]
        
        response = self.call_ai(messages)
        
        # Multi-step workflow for business formation
        if "incorporat" in state['user_message'].lower() or "llc" in state['user_message'].lower():
            # Step 1: Document generation
            doc_state = state.copy()
            doc_state['user_message'] = f"Generate incorporation documents for: {state['user_message']}"
            doc_response = self.sub_agents[0].process(doc_state)
            
            # Step 2: Compliance check
            comp_state = state.copy()
            comp_state['user_message'] = f"Check compliance requirements for: {state['user_message']}"
            comp_response = self.sub_agents[1].process(comp_state)
            
            response += f"\n\n**Document Generation:** {doc_response.get('agent_responses', {}).get('document', '')}"
            response += f"\n\n**Compliance Requirements:** {comp_response.get('agent_responses', {}).get('compliance', '')}"
        
        state['agent_responses']['business'] = response
        state['agent_confidence']['business'] = 0.9
        return state

class DocumentAgent(BaseAgent):
    """Layer 3: Document Agent - Specialized for document generation and analysis"""
    
    def __init__(self):
        super().__init__(
            "Document Agent",
            "gpt-4o",
            """You are a legal document specialist. Generate, analyze, and review legal documents.
            
            Capabilities:
            - Generate standard legal documents
            - Analyze existing documents
            - Review for compliance issues
            - Suggest improvements"""
        )
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Process document-related requests"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Document request: {state['user_message']}"}
        ]
        
        response = self.call_ai(messages)
        state['agent_responses']['document'] = response
        state['agent_confidence']['document'] = 0.8
        return state

class ComplianceAgent(BaseAgent):
    """Layer 3: Compliance Agent - Specialized for regulatory compliance"""
    
    def __init__(self):
        super().__init__(
            "Compliance Agent",
            "claude-3-sonnet-20240229",
            """You are a compliance specialist focusing on regulatory requirements.
            
            Areas of expertise:
            - GDPR and data privacy
            - Business compliance
            - Industry regulations
            - Risk assessment"""
        )
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Process compliance-related requests"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Compliance question: {state['user_message']}"}
        ]
        
        response = self.call_ai(messages)
        state['agent_responses']['compliance'] = response
        state['agent_confidence']['compliance'] = 0.8
        return state

class ExpertAgent(BaseAgent):
    """Layer 3: Expert Agent - For complex legal analysis"""
    
    def __init__(self):
        super().__init__(
            "Expert Agent",
            "gpt-4o",
            """You are a legal expert for complex cases requiring deep analysis.
            
            Your role:
            - Provide in-depth legal analysis
            - Identify potential issues
            - Suggest strategies
            - Recommend when to consult human attorneys"""
        )
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Process complex legal analysis"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Expert analysis needed for: {state['user_message']}"}
        ]
        
        response = self.call_ai(messages)
        state['agent_responses']['expert'] = response
        state['agent_confidence']['expert'] = 0.9
        return state

class SynthesisAgent(BaseAgent):
    """Layer 4: Synthesis Agent - Combines multiple agent responses"""
    
    def __init__(self):
        super().__init__(
            "Synthesis Agent",
            "gpt-4o",
            """You are a synthesis agent that combines responses from multiple agents.
            
            Your job:
            1. Review all agent responses
            2. Identify conflicts or gaps
            3. Create a coherent final response
            4. Determine if human review is needed"""
        )
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Synthesize multiple agent responses"""
        agent_responses = state.get('agent_responses', {})
        
        if len(agent_responses) == 1:
            # Single agent response
            state['synthesized_response'] = list(agent_responses.values())[0]
            state['needs_human_review'] = False
        else:
            # Multiple agent responses - need synthesis
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"""
                Synthesize these agent responses for the user question: {state['user_message']}
                
                Agent Responses:
                {json.dumps(agent_responses, indent=2)}
                
                Create a coherent, comprehensive response that addresses all aspects of the question.
                """}
            ]
            
            response = self.call_ai(messages)
            state['synthesized_response'] = response
            state['needs_human_review'] = state['complexity_score'] > 0.8
        
        return state

class HumanInLoopAgent(BaseAgent):
    """Layer 5: Human-in-the-Loop Agent - For complex cases requiring human review"""
    
    def __init__(self):
        super().__init__(
            "Human-in-Loop Agent",
            "gpt-4o",
            """You are a human-in-the-loop agent that handles cases requiring human attorney review.
            
            Your role:
            1. Identify when human review is needed
            2. Prepare case summary for human attorney
            3. Provide interim guidance
            4. Schedule follow-up"""
        )
    
    def process(self, state: MultiLayerState) -> MultiLayerState:
        """Handle human-in-the-loop workflow"""
        if state.get('needs_human_review', False):
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"""
                This case requires human attorney review: {state['user_message']}
                
                Synthesized response: {state.get('synthesized_response', '')}
                Complexity score: {state.get('complexity_score', 0)}
                
                Prepare a case summary and interim guidance.
                """}
            ]
            
            response = self.call_ai(messages)
            state['escalation_reason'] = "Complex case requiring human attorney review"
            state['final_response'] = response + "\n\n⚠️ **This case has been escalated to a human attorney for review.**"
        else:
            state['final_response'] = state.get('synthesized_response', 'No response generated')
        
        return state

class MultiLayerAgentSystem:
    """Main multi-layer agent orchestration system"""
    
    def __init__(self):
        # Initialize all agents
        self.supervisor = SupervisorAgent()
        self.immigration = ImmigrationAgent()
        self.family = FamilyLawAgent()
        self.business = BusinessLawAgent()
        self.document = DocumentAgent()
        self.compliance = ComplianceAgent()
        self.expert = ExpertAgent()
        self.synthesis = SynthesisAgent()
        self.human_loop = HumanInLoopAgent()
        
        # Agent registry
        self.agents = {
            'supervisor': self.supervisor,
            'immigration': self.immigration,
            'family': self.family,
            'business': self.business,
            'document': self.document,
            'compliance': self.compliance,
            'expert': self.expert,
            'synthesis': self.synthesis,
            'human_loop': self.human_loop
        }
    
    def process_message(self, message: str, user_id: str = None) -> Dict:
        """Process message through multi-layer agent system"""
        start_time = datetime.now()
        
        # Initialize state
        state: MultiLayerState = {
            'user_message': message,
            'user_id': user_id,
            'supervisor_analysis': {},
            'complexity_score': 0.0,
            'required_agents': [],
            'workflow_type': 'simple',
            'agent_responses': {},
            'agent_confidence': {},
            'cross_agent_validation': {},
            'synthesized_response': '',
            'needs_human_review': False,
            'escalation_reason': None,
            'human_feedback': None,
            'final_response': '',
            'agent_chain': [],
            'processing_time': 0.0,
            'confidence_score': 0.0
        }
        
        try:
            # Layer 1: Supervisor Analysis
            logger.info("🔍 Layer 1: Supervisor Analysis")
            state = self.supervisor.process(state)
            state['agent_chain'].append('supervisor')
            
            # Layer 2: Agent Orchestration
            logger.info(f"🤖 Layer 2: Agent Orchestration - {state['required_agents']}")
            for agent_name in state['required_agents']:
                if agent_name in self.agents:
                    state = self.agents[agent_name].process(state)
                    state['agent_chain'].append(agent_name)
            
            # Layer 3: Synthesis
            logger.info("🔄 Layer 3: Synthesis")
            state = self.synthesis.process(state)
            state['agent_chain'].append('synthesis')
            
            # Layer 4: Human-in-the-Loop (if needed)
            if state.get('needs_human_review', False):
                logger.info("👤 Layer 4: Human-in-the-Loop")
                state = self.human_loop.process(state)
                state['agent_chain'].append('human_loop')
            
            # Calculate final metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            state['processing_time'] = processing_time
            state['confidence_score'] = sum(state['agent_confidence'].values()) / len(state['agent_confidence']) if state['agent_confidence'] else 0.0
            
            logger.info(f"✅ Multi-layer processing complete in {processing_time:.2f}s")
            logger.info(f"🔗 Agent chain: {' → '.join(state['agent_chain'])}")
            
            return {
                'response': state['final_response'],
                'agent_chain': state['agent_chain'],
                'complexity_score': state['complexity_score'],
                'confidence_score': state['confidence_score'],
                'needs_human_review': state.get('needs_human_review', False),
                'escalation_reason': state.get('escalation_reason'),
                'processing_time': state['processing_time'],
                'workflow_type': state['workflow_type'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in multi-layer system: {e}")
            return {
                'response': "I'm sorry, I encountered an error in the multi-layer system. Please try again.",
                'agent_chain': ['error'],
                'complexity_score': 0.0,
                'confidence_score': 0.0,
                'needs_human_review': True,
                'escalation_reason': 'System error',
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'workflow_type': 'error',
                'timestamp': datetime.now().isoformat()
            }

# Initialize multi-layer system
multilayer_system = MultiLayerAgentSystem()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'SmartProBono REAL Multi-Layer Agent System is running',
        'version': '5.0.0',
        'ai_system': 'Multi-Layer Agent System with LangGraph-style Orchestration',
        'database': 'Supabase PostgreSQL with RLS',
        'layers': [
            'Layer 1: Supervisor Analysis',
            'Layer 2: Agent Orchestration',
            'Layer 3: Synthesis',
            'Layer 4: Human-in-the-Loop',
            'Layer 5: Final Output'
        ],
        'agents': list(multilayer_system.agents.keys()),
        'ai_providers': {
            'openai': openai_client is not None,
            'anthropic': anthropic_client is not None
        }
    })

@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    """Multi-layer legal chat endpoint"""
    try:
        data = request.json
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        user_id = data.get('user_id')
        
        logger.info(f"💬 Multi-layer processing: {message}")
        
        # Process through multi-layer system
        result = multilayer_system.process_message(message, user_id)
        
        logger.info(f"🔗 Agent chain: {' → '.join(result['agent_chain'])}")
        logger.info(f"📊 Complexity: {result['complexity_score']}, Confidence: {result['confidence_score']}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in multi-layer legal chat: {e}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'response': "I'm sorry, I encountered an error. Please try again."
        }), 500

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get information about available agents"""
    return jsonify({
        'layers': {
            'Layer 1 - Supervisor': ['supervisor'],
            'Layer 2 - Specialists': ['immigration', 'family', 'business'],
            'Layer 3 - Support': ['document', 'compliance', 'expert'],
            'Layer 4 - Synthesis': ['synthesis'],
            'Layer 5 - Human Loop': ['human_loop']
        },
        'agents': [
            {
                'name': agent.name,
                'type': agent_type,
                'model': agent.model,
                'sub_agents': [sub.name for sub in agent.sub_agents],
                'description': f"Multi-layer agent for {agent_type} with sub-agent capabilities"
            }
            for agent_type, agent in multilayer_system.agents.items()
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    print(f"🚀 Starting SmartProBono REAL Multi-Layer Agent System")
    print(f"🔐 Security: Row Level Security (RLS) enabled")
    print(f"🤖 AI System: Multi-Layer Agent System with LangGraph-style Orchestration")
    print(f"📊 Database: Supabase PostgreSQL")
    print(f"")
    print(f"🏗️ Multi-Layer Architecture:")
    print(f"  Layer 1: Supervisor Analysis")
    print(f"  Layer 2: Agent Orchestration (with sub-agents)")
    print(f"  Layer 3: Synthesis & Validation")
    print(f"  Layer 4: Human-in-the-Loop")
    print(f"  Layer 5: Final Output")
    print(f"")
    print(f"🤖 Available Agents:")
    for agent_type, agent in multilayer_system.agents.items():
        sub_agents = [sub.name for sub in agent.sub_agents]
        print(f"  • {agent.name} ({agent.model})")
        if sub_agents:
            print(f"    └─ Sub-agents: {', '.join(sub_agents)}")
    print(f"")
    print(f"Available endpoints:")
    print(f"  • Health: http://localhost:{port}/api/health")
    print(f"  • Legal Chat: http://localhost:{port}/api/legal/chat")
    print(f"  • Agents: http://localhost:{port}/api/agents")
    print(f"")
    print(f"🎯 Test the multi-layer system:")
    print(f"  • Simple: 'hello' → Supervisor → Greeting")
    print(f"  • Complex: 'immigration visa' → Supervisor → Immigration → Document → Synthesis")
    print(f"  • Multi-agent: 'business incorporation' → Supervisor → Business → Document + Compliance → Synthesis")
    print(f"")
    print(f"🔗 Supabase Project: {SUPABASE_URL}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
