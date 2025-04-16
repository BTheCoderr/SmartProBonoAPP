"""
Legal Assistant Service for SmartProBono
This module provides an enhanced legal assistant with citation capabilities and 
jurisdiction-specific responses.
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re
import time

# Import AI components
from services.ai_service_manager import ai_service_manager, AIProvider
from ai.vector_db_manager import VectorDatabaseManager, get_vector_db_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalAssistantService:
    """
    Enhanced legal assistant service with citation capabilities and
    jurisdiction-specific responses.
    """
    
    def __init__(self):
        """Initialize the legal assistant service."""
        # Initialize vector database for legal knowledge retrieval
        self.vector_db_config = get_vector_db_config()
        self.vector_db = VectorDatabaseManager(**self.vector_db_config)
        
        # Load vector database indexes
        self._load_vector_indexes()
        
        # Legal domains for categorization
        self.legal_domains = {
            'tenant_rights': {
                'keywords': ['tenant', 'landlord', 'lease', 'rent', 'apartment', 'eviction', 
                            'housing', 'security deposit', 'repairs', 'rental'],
                'index': 'housing_law',
                'has_specialized_model': True
            },
            'employment': {
                'keywords': ['employee', 'employer', 'workplace', 'job', 'salary', 'wage', 
                            'discrimination', 'harassment', 'termination', 'firing', 'benefits',
                            'workers comp', 'unemployment', 'leave', 'contract'],
                'index': 'employment_law',
                'has_specialized_model': True
            },
            'immigration': {
                'keywords': ['immigrant', 'visa', 'citizenship', 'green card', 'asylum', 
                            'deportation', 'immigration', 'DACA', 'refugee', 'status',
                            'naturalization', 'passport'],
                'index': 'immigration_law',
                'has_specialized_model': True
            },
            'family': {
                'keywords': ['divorce', 'custody', 'child support', 'alimony', 'visitation',
                            'separation', 'spouse', 'marriage', 'parental rights', 'adoption'],
                'index': 'family_law',
                'has_specialized_model': False
            },
            'consumer': {
                'keywords': ['debt', 'collection', 'credit', 'loan', 'contract', 'warranty',
                            'refund', 'consumer', 'product', 'service', 'fraud', 'lemon law'],
                'index': 'consumer_law',
                'has_specialized_model': False
            },
            'criminal': {
                'keywords': ['arrest', 'charge', 'offense', 'defense', 'probation', 'parole',
                            'conviction', 'sentence', 'misdemeanor', 'felony', 'rights'],
                'index': 'criminal_law',
                'has_specialized_model': False
            }
        }
        
        # Citation patterns for extraction
        self.citation_patterns = {
            'case': r'([A-Z][a-z]+\s+v\.\s+[A-Z][a-z]+),\s+(\d+)\s+([A-Z]\.[\w\.]+)\s+(\d+)\s+\((\d{4})\)',
            'statute': r'([A-Z][a-z\.]+)\s+Code\s+[§\s]+(\d+[\w\-\.]*)',
            'regulation': r'(\d+)\s+C\.F\.R\.\s+[§\s]+(\d+[\w\-\.]*)',
            'constitution': r'([A-Z][a-z]+)\s+Constitution,\s+Article\s+([IVX]+),\s+[§\s]+(\d+)',
        }
        
        # Initialize response cache
        self.response_cache = {}
        self.cache_ttl = 86400  # 24 hours in seconds
        self.default_cache_size = 1000  # Maximum number of items in cache
        self.default_index = 'legal_general'
        
        # Available jurisdictions
        self.jurisdictions = self._load_available_jurisdictions()
        
        # Schedule cache cleanup
        self._schedule_cache_cleanup()
        
    def _load_vector_indexes(self):
        """Load available vector database indexes."""
        # Load metadata record
        self.vector_db._load_metadata_record()
        
        # Log available indexes
        indexes = self.vector_db.get_available_indexes()
        if indexes:
            logger.info(f"Available vector indexes: {', '.join([idx['name'] for idx in indexes])}")
        else:
            logger.warning("No vector indexes available. Legal citation functionality will be limited.")
            
    def detect_legal_domain(self, query: str) -> Tuple[str, float]:
        """
        Detect the legal domain of a query.
        
        Args:
            query: User's legal question
            
        Returns:
            Tuple of (domain_name, confidence_score)
        """
        query_lower = query.lower()
        domain_scores = {}
        
        # Calculate keyword matches for each domain
        for domain, info in self.legal_domains.items():
            keywords = info['keywords']
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword.lower() in query_lower)
            # Weight by keyword count to avoid bias toward domains with more keywords
            score = matches / len(keywords) if keywords else 0
            domain_scores[domain] = score
            
        # Get domain with highest score
        if domain_scores:
            best_domain = max(domain_scores.items(), key=lambda x: x[1])
            # Only return if confidence is above threshold
            if best_domain[1] > 0.1:  # At least 10% of keywords matched
                return best_domain
                
        return ('general', 0.0)
        
    def detect_jurisdiction(self, query: str) -> Optional[str]:
        """
        Detect the jurisdiction from a query.
        
        Args:
            query: User's legal question
            
        Returns:
            Jurisdiction name or None
        """
        query_words = query.lower().split()
        
        # Look for jurisdictions in the query
        for jurisdiction in self.jurisdictions:
            if jurisdiction.lower() in query_words or jurisdiction.lower() in query.lower():
                return jurisdiction
                
        # Look for common patterns
        if "in the state of" in query.lower():
            parts = query.lower().split("in the state of")
            if len(parts) > 1:
                state_part = parts[1].strip().split()
                if state_part and state_part[0].capitalize() in self.jurisdictions:
                    return state_part[0].capitalize()
                    
        # No jurisdiction detected
        return None
        
    async def get_legal_response_with_citations(
        self, 
        query: str, 
        jurisdiction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a legal response with relevant citations.
        
        Args:
            query: Legal question from user
            jurisdiction: Optional jurisdiction to filter by
            
        Returns:
            Response with text, citations, and metadata
        """
        start_time = time.time()
        logger.info(f"Processing legal query: {query}")
        
        # Check cache first
        cache_key = self._create_cache_key(query, jurisdiction)
        cached_response = self._get_from_cache(cache_key)
        
        if cached_response:
            # Add cache metadata
            cached_response['metadata'] = cached_response.get('metadata', {})
            cached_response['metadata']['cache_hit'] = True
            cached_response['metadata']['response_time'] = time.time() - start_time
            return cached_response
        
        # Continue with normal processing if not in cache
        try:
            # Detect domain and jurisdiction if not provided
            domain, domain_confidence = self.detect_legal_domain(query)
            if jurisdiction is None:
                jurisdiction = self.detect_jurisdiction(query)
            
            logger.info(f"Detected domain: {domain} (confidence: {domain_confidence:.2f})")
            if jurisdiction:
                logger.info(f"Detected jurisdiction: {jurisdiction}")
            
            # Get vector index for the domain
            index_name = self.legal_domains.get(domain, {}).get('index', self.default_index)
            
            # Get relevant legal information from vector database
            vector_results = []
            try:
                if jurisdiction:
                    vector_results = self.vector_db.search_by_jurisdiction(
                        query=query,
                        jurisdiction=jurisdiction,
                        index_name=index_name
                    )
                else:
                    vector_results = self.vector_db.search(
                        query=query,
                        index_name=index_name
                    )
                
                logger.info(f"Found {len(vector_results)} relevant vector results")
            except Exception as e:
                logger.error(f"Error retrieving from vector database: {str(e)}")
            
            # Extract citations
            citations = []
            if vector_results:
                try:
                    citations = self.vector_db.extract_citations(vector_results)
                    logger.info(f"Extracted {len(citations)} citations")
                except Exception as e:
                    logger.error(f"Error extracting citations: {str(e)}")
            
            # Select appropriate AI model based on domain
            task_type = 'legal_qa'
            if domain == 'employment' or domain == 'immigration':
                task_type = 'rights_research'
            elif domain == 'general' and domain_confidence < 0.2:
                task_type = 'chat'  # Use simple chat for very general questions
            
            # Get provider for task type
            provider = ai_service_manager.get_best_provider(task_type)
            
            # Build context from citations
            citation_context = ""
            if citations:
                citation_context = "\n\nRelevant legal information:\n"
                for i, citation in enumerate(citations[:3]):  # Limit to top 3 citations
                    citation_context += f"{i+1}. {citation['text']} ({citation['jurisdiction']})\n"
            
            # Build system prompt based on the detected domain and jurisdiction
            system_prompt = """You are an AI legal assistant providing information on legal topics. Your role is to:

1. Provide accurate legal information based on established laws, regulations, and precedents
2. Reference relevant statutes, regulations, and case law when available
3. Explain legal concepts and processes in clear, understandable language
4. Recognize the limitations of AI legal advice
5. Always include appropriate disclaimers

Guidelines for responses:
- Be detailed but concise
- Structure responses logically with clear sections
- Acknowledge legal uncertainties and alternative interpretations
- Provide procedural information when relevant
- Cite sources when possible"""

            if domain != 'general':
                domain_context = f"This question relates to {domain.replace('_', ' ')} law. Focus your response on this legal domain."
                system_prompt += f"\n\n{domain_context}"
                
            if jurisdiction:
                jurisdiction_context = f"Provide information specific to {jurisdiction} jurisdiction. Focus on the laws, regulations, and procedures applicable in {jurisdiction}."
                system_prompt += f"\n\n{jurisdiction_context}"
                
            if citations:
                citation_guidance = "Use the provided legal information and citations in your response. Cite specific sections when relevant."
                system_prompt += f"\n\n{citation_guidance}"
                
            full_prompt = f"{system_prompt}\n\nUser question: {query}"
            if citation_context:
                full_prompt += f"\n{citation_context}"
                
            # Get response from AI
            ai_response = await ai_service_manager.get_response(
                prompt=full_prompt,
                provider=provider,
                task_type=task_type
            )
            
            response_text = ai_response.get('text', '')
            
            # Extract any additional citations from the response
            additional_citations = self.parse_citations_from_text(response_text)
            
            # Add any additional citations not already in the list
            existing_citation_texts = [c['text'] for c in citations]
            for citation in additional_citations:
                if citation['text'] not in existing_citation_texts:
                    citations.append(citation)
                    
            # Add disclaimer if not already present
            if "disclaimer" not in response_text.lower() and "not legal advice" not in response_text.lower():
                response_text += "\n\nPLEASE NOTE: This information is provided for general educational purposes only and should not be considered legal advice. For specific legal advice tailored to your situation, please consult with a qualified legal professional."
                
            # Prepare final response
            response = {
                'text': response_text,
                'citations': citations,
                'domain': domain,
                'jurisdiction': jurisdiction,
                'confidence': {
                    'domain': domain_confidence,
                    'response': ai_response.get('confidence_score', 0.8)
                },
                'metadata': {
                    'model_used': ai_response.get('model', 'unknown'),
                    'response_time': time.time() - start_time,
                    'token_count': ai_response.get('token_count', 0)
                }
            }
            
            # Add resources if available
            resources = self.get_legal_resources(domain, jurisdiction)
            if resources:
                response['resources'] = resources
                
            # Add to cache before returning
            self._add_to_cache(cache_key, response)
            return response
            
        except Exception as e:
            logger.error(f"Error generating legal response: {str(e)}")
            
            # Return error response
            return {
                'text': "I'm sorry, but I encountered an error while processing your legal question. Please try again or rephrase your question.",
                'citations': [],
                'metadata': {
                    'error': str(e),
                    'response_time': time.time() - start_time
                }
            }

    def parse_citations_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Extract citations from response text.
        
        Args:
            text: Response text to parse
            
        Returns:
            List of extracted citations
        """
        citations = []
        
        for citation_type, pattern in self.citation_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                citation = {
                    'type': citation_type,
                    'text': match.group(0),
                    'source': 'text_extraction'
                }
                citations.append(citation)
                
        return citations
        
    def get_legal_resources(self, domain: str, jurisdiction: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Get relevant legal resources for a domain and jurisdiction.
        
        Args:
            domain: Legal domain
            jurisdiction: Optional jurisdiction
            
        Returns:
            List of resource information
        """
        # Default resources
        resources = [
            {
                'name': 'LawHelp.org',
                'url': 'https://www.lawhelp.org/',
                'description': 'Free legal aid resources'
            },
            {
                'name': 'American Bar Association',
                'url': 'https://www.americanbar.org/groups/legal_services/flh-home/',
                'description': 'Free legal answers'
            },
            {
                'name': 'Legal Services Corporation',
                'url': 'https://www.lsc.gov/what-legal-aid/find-legal-aid',
                'description': 'Find legal aid'
            }
        ]
        
        # Domain-specific resources
        domain_resources = {
            'tenant_rights': [
                {
                    'name': 'HUD Housing Discrimination',
                    'url': 'https://www.hud.gov/program_offices/fair_housing_equal_opp/online-complaint',
                    'description': 'File a housing discrimination complaint'
                },
                {
                    'name': 'Tenant Rights & Resources',
                    'url': 'https://www.hud.gov/topics/rental_assistance/tenantrights',
                    'description': 'HUD tenant rights information'
                }
            ],
            'employment': [
                {
                    'name': 'Equal Employment Opportunity Commission',
                    'url': 'https://www.eeoc.gov/how-file-charge-employment-discrimination',
                    'description': 'File a workplace discrimination charge'
                },
                {
                    'name': 'Department of Labor',
                    'url': 'https://www.dol.gov/agencies/whd/contact/complaints',
                    'description': 'Wage and hour complaints'
                }
            ],
            'immigration': [
                {
                    'name': 'USCIS',
                    'url': 'https://www.uscis.gov/',
                    'description': 'Official immigration forms and information'
                },
                {
                    'name': 'Immigration Law Help',
                    'url': 'https://www.immigrationlawhelp.org/',
                    'description': 'Nonprofit immigration legal services'
                }
            ]
        }
        
        # Add domain-specific resources if available
        if domain in domain_resources:
            resources.extend(domain_resources[domain])
            
        # Add jurisdiction-specific resources if available
        if jurisdiction:
            # This would be expanded with actual jurisdiction-specific resources
            # For now, add a generic legal aid finder
            resources.append({
                'name': f'Legal Aid in {jurisdiction}',
                'url': f'https://www.lawhelp.org/find-legal-help',
                'description': f'Find legal aid in {jurisdiction}'
            })
            
        return resources
        
    def get_citation_details(self, citation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific citation.
        
        Args:
            citation_id: The ID of the citation to retrieve
            
        Returns:
            Dictionary with citation details or None if not found
        """
        try:
            # Check if citation_id is a valid UUID (used for vector DB entries)
            try:
                import uuid
                uuid_obj = uuid.UUID(citation_id)
                # If valid UUID, attempt to retrieve from vector database
                vector_results = self.vector_db.get_document_by_id(citation_id)
                if vector_results:
                    citation = {
                        'id': citation_id,
                        'text': vector_results.get('text', ''),
                        'type': vector_results.get('type', 'Unknown'),
                        'jurisdiction': vector_results.get('jurisdiction', 'Unknown'),
                        'title': vector_results.get('title', ''),
                        'section': vector_results.get('section', ''),
                        'content': vector_results.get('content', ''),
                        'url': vector_results.get('url', ''),
                        'year': vector_results.get('year', '')
                    }
                    return citation
            except (ValueError, TypeError):
                # Not a UUID, continue with other lookup methods
                pass
                
            # Parse citation ID format (common format: type-jurisdiction-identifier)
            parts = citation_id.split('-', 2)
            if len(parts) >= 3:
                citation_type, jurisdiction, identifier = parts
                
                # Build search query based on citation parts
                search_query = f"{jurisdiction} {identifier}"
                index_name = self.default_index
                
                # Search in vector database
                vector_results = self.vector_db.search(
                    query=search_query,
                    index_name=index_name,
                    k=1  # Only get the most relevant result
                )
                
                if vector_results and len(vector_results) > 0:
                    result = vector_results[0]
                    citation = {
                        'id': citation_id,
                        'text': result.get('text', ''),
                        'type': citation_type.capitalize(),
                        'jurisdiction': jurisdiction.capitalize(),
                        'title': result.get('title', ''),
                        'section': identifier,
                        'content': result.get('content', ''),
                        'url': result.get('url', ''),
                        'year': result.get('year', '')
                    }
                    return citation
            
            # Fallback for known citation formats
            if 'statute' in citation_id:
                statute_match = re.search(r'([a-z]+)-([a-z]+)-(\d+)', citation_id)
                if statute_match:
                    _, jurisdiction, section = statute_match.groups()
                    return {
                        'id': citation_id,
                        'text': f"{jurisdiction.upper()} Code § {section}",
                        'type': 'Statute',
                        'jurisdiction': jurisdiction.capitalize(),
                        'title': f"{jurisdiction.upper()} Code",
                        'section': section,
                        'content': "Full text not available. Please refer to the official code.",
                        'url': f"https://www.law.cornell.edu/statutes/{jurisdiction}/section/{section}",
                        'year': 'Current'
                    }
            
            # Citation not found
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving citation details: {str(e)}")
            return None

    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get available AI models for legal assistance.
        
        Returns:
            List of available models with their specifications
        """
        models = []
        
        # Add general-purpose model
        models.append({
            'id': 'general-legal-assistant',
            'name': 'General Legal Assistant',
            'description': 'Balanced model for all legal questions',
            'specialization': []
        })
        
        # Add domain-specific models
        for domain, info in self.legal_domains.items():
            if info.get('has_specialized_model', False):
                models.append({
                    'id': f"{domain}-legal-assistant",
                    'name': f"{domain.replace('_', ' ').title()} Specialist",
                    'description': f"Specialized for {domain.replace('_', ' ')} law",
                    'specialization': [domain]
                })
        
        # Add jurisdiction-specific models
        for jurisdiction in ['federal', 'california', 'new_york', 'texas']:
            if jurisdiction in self.jurisdictions:
                models.append({
                    'id': f"{jurisdiction}-legal-assistant",
                    'name': f"{jurisdiction.capitalize()} Law Specialist",
                    'description': f"Specialized for {jurisdiction.capitalize()} jurisdiction",
                    'specialization': [jurisdiction]
                })
        
        return models

    async def get_specialized_legal_response(
        self,
        query: str,
        domain: str,
        jurisdiction: Optional[str] = None,
        model_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a specialized legal response for a specific domain.
        
        Args:
            query: User's legal question
            domain: Legal domain to target
            jurisdiction: Optional jurisdiction to filter by
            model_id: Optional model ID to use
            
        Returns:
            Dictionary with response text, citations, and metadata
        """
        start_time = time.time()
        logger.info(f"Processing specialized legal query in {domain} domain: {query}")
        
        # Check cache first
        cache_key = self._create_cache_key(query, jurisdiction, domain)
        cached_response = self._get_from_cache(cache_key)
        
        if cached_response:
            # Add cache metadata to response
            cached_response['metadata'] = cached_response.get('metadata', {})
            cached_response['metadata']['cache_hit'] = True
            cached_response['metadata']['response_time'] = time.time() - start_time
            return cached_response
            
        try:
            # Make sure domain is valid
            if domain not in self.legal_domains and domain != 'general':
                domain = 'general'
                logger.warning(f"Invalid domain: {domain}, defaulting to general")
            
            # Get vector index for the domain
            index_name = self.legal_domains.get(domain, {}).get('index', self.default_index)
            
            # Get relevant legal information from vector database
            vector_results = []
            try:
                if jurisdiction:
                    vector_results = self.vector_db.search_by_jurisdiction(
                        query=query,
                        jurisdiction=jurisdiction,
                        index_name=index_name,
                        k=5  # Get top 5 results for specialized domains
                    )
                else:
                    vector_results = self.vector_db.search(
                        query=query,
                        index_name=index_name,
                        k=5
                    )
                    
                logger.info(f"Found {len(vector_results)} relevant vector results for specialized query")
            except Exception as e:
                logger.error(f"Error retrieving from vector database: {str(e)}")
                
            # Extract citations
            citations = []
            if vector_results:
                try:
                    citations = self.vector_db.extract_citations(vector_results)
                    logger.info(f"Extracted {len(citations)} citations for specialized query")
                except Exception as e:
                    logger.error(f"Error extracting citations: {str(e)}")
            
            # Select appropriate model for domain
            if model_id:
                task_type = 'specialized_legal_qa'
            else:
                task_type = f"{domain}_legal_qa" if domain != 'general' else 'legal_qa'
            
            # Get provider for specialized task
            provider = ai_service_manager.get_best_provider(task_type)
            
            # Build context from citations
            citation_context = ""
            if citations:
                citation_context = "\n\nRelevant legal information:\n"
                for i, citation in enumerate(citations[:5]):  # Include up to 5 citations
                    citation_context += f"{i+1}. {citation['text']} ({citation['jurisdiction']})\n"
                    if 'content' in citation and citation['content']:
                        # Include snippet of content if available
                        content_snippet = citation['content']
                        if len(content_snippet) > 200:
                            content_snippet = content_snippet[:200] + "..."
                        citation_context += f"   {content_snippet}\n"
            
            # Build domain-specific system prompt
            system_prompt = """You are a specialized AI legal assistant providing detailed information on a specific legal domain. Your role is to:

1. Provide accurate, domain-specific legal information with appropriate technical depth
2. Reference relevant statutes, regulations, and case law applicable to the domain
3. Explain domain-specific legal concepts, procedures, and rights
4. Include citations to authoritative sources when available
5. Structure your response in an organized, easy to follow format
6. Always include appropriate disclaimers about the limitations of AI legal information

Guidelines for specialized responses:
- Start with a clear overview of the relevant legal framework
- Provide detailed, step-by-step explanations for procedural questions
- Break down complex domain-specific terms into understandable explanations
- Use headers and bullet points to organize information
- Include specific references to applicable laws and regulations
- End with next steps and resources specific to this legal domain"""

            # Add domain-specific context
            if domain and domain != 'general':
                domain_name = domain.replace('_', ' ')
                domain_context = f"You are specifically responding to a question about {domain_name} law. Focus your response on this specific legal domain in precise detail."
                system_prompt += f"\n\n{domain_context}"
                
            # Add jurisdiction-specific context
            if jurisdiction:
                jurisdiction_context = f"Provide information specific to {jurisdiction} jurisdiction. Focus on the laws, regulations, and procedures applicable in {jurisdiction}."
                system_prompt += f"\n\n{jurisdiction_context}"
                
            # Add citation guidance
            if citations:
                citation_guidance = "Use the provided legal information and citations in your response. Cite specific sections when relevant."
                system_prompt += f"\n\n{citation_guidance}"
                
            # Full prompt with query and context
            full_prompt = f"{system_prompt}\n\nUser question: {query}"
            if citation_context:
                full_prompt += f"\n{citation_context}"
                
            # Get response from AI
            ai_response = await ai_service_manager.get_response(
                prompt=full_prompt,
                provider=provider,
                task_type=task_type
            )
            
            response_text = ai_response.get('text', '')
            
            # Add specialized disclaimer
            disclaimer = f"\n\nPLEASE NOTE: This information is specialized for {domain.replace('_', ' ')} law"
            if jurisdiction:
                disclaimer += f" in {jurisdiction}"
            disclaimer += ", but should not be considered legal advice. For specific legal advice tailored to your situation, please consult with a qualified legal professional."
            
            # Add disclaimer if not already present
            if "disclaimer" not in response_text.lower() and "not legal advice" not in response_text.lower():
                response_text += disclaimer
                
            # Return structured response
            response = {
                'text': response_text,
                'citations': citations,
                'domain': domain,
                'jurisdiction': jurisdiction,
                'confidence': {
                    'domain': 0.95,  # Higher confidence for specialized domain
                    'response': ai_response.get('confidence_score', 0.9)
                },
                'model_used': model_id or f"{domain}-specialized-model",
                'metadata': {
                    'response_time': time.time() - start_time,
                    'token_count': ai_response.get('token_count', 0)
                }
            }
            
            # Add resources if available
            resources = self.get_legal_resources(domain, jurisdiction)
            if resources:
                response['resources'] = resources
                
            # Add to cache before returning
            self._add_to_cache(cache_key, response)
            return response
            
        except Exception as e:
            logger.error(f"Error getting specialized AI response: {str(e)}")
            return {
                'text': f"I'm sorry, but I encountered an error while processing your specialized legal question about {domain.replace('_', ' ')}. Please try again or rephrase your question.",
                'citations': [],
                'domain': domain,
                'jurisdiction': jurisdiction,
                'confidence': {
                    'domain': 0.0,
                    'response': 0.0
                },
                'error': str(e),
                'metadata': {
                    'response_time': time.time() - start_time
                }
            }
        
    async def log_interaction(self, query: str, response: Dict[str, Any], user_id: Optional[str] = None):
        """
        Log user interaction for future training and analysis.
        
        Args:
            query: User query
            response: Generated response
            user_id: Optional user ID
        """
        try:
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'query': query,
                'response': response,
                'user_id': user_id,
            }
            
            # Log directory
            log_dir = os.path.join('data', 'logs', 'legal_assistant')
            os.makedirs(log_dir, exist_ok=True)
            
            # Create log file with today's date
            today = datetime.now().strftime('%Y-%m-%d')
            log_file = os.path.join(log_dir, f'interactions_{today}.jsonl')
            
            # Append to log file
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_data) + '\n')
                
        except Exception as e:
            logger.error(f"Error logging interaction: {str(e)}")

    def _schedule_cache_cleanup(self):
        """Schedule regular cache cleanup to prevent memory issues."""
        from threading import Timer
        
        # Run cleanup every 12 hours
        cleanup_interval = 43200  # 12 hours in seconds
        
        def cleanup():
            self._cleanup_cache()
            # Schedule next cleanup
            Timer(cleanup_interval, cleanup).start()
        
        # Start the first cleanup timer
        Timer(cleanup_interval, cleanup).start()
        
    def _cleanup_cache(self):
        """Remove expired cache entries."""
        current_time = time.time()
        keys_to_remove = []
        
        for key, cache_item in self.response_cache.items():
            if current_time > cache_item.get('expiry', 0):
                keys_to_remove.append(key)
                
        # Remove expired items
        for key in keys_to_remove:
            del self.response_cache[key]
            
        # Check if cache is too large and remove oldest entries if needed
        if len(self.response_cache) > self.default_cache_size:
            # Sort by last accessed time
            sorted_cache = sorted(
                self.response_cache.items(),
                key=lambda x: x[1].get('last_accessed', 0)
            )
            
            # Remove oldest entries until we're back to the size limit
            for key, _ in sorted_cache[:len(sorted_cache) - self.default_cache_size]:
                del self.response_cache[key]
                
        logger.info(f"Cache cleanup completed. {len(keys_to_remove)} expired items removed. "
                   f"Current cache size: {len(self.response_cache)}")
                   
    def _create_cache_key(self, query: str, jurisdiction: Optional[str] = None, domain: Optional[str] = None) -> str:
        """Create a normalized cache key from query and parameters."""
        # Normalize query by lowercasing and removing extra whitespace
        normalized_query = ' '.join(query.lower().split())
        
        # Create a hashable key
        key_parts = [normalized_query]
        if jurisdiction:
            key_parts.append(f"jur:{jurisdiction.lower()}")
        if domain:
            key_parts.append(f"dom:{domain.lower()}")
            
        return '|'.join(key_parts)
        
    def _get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Try to retrieve a response from the cache."""
        if key in self.response_cache:
            cache_item = self.response_cache[key]
            current_time = time.time()
            
            # Check if the item is still valid
            if current_time <= cache_item.get('expiry', 0):
                # Update last accessed time
                self.response_cache[key]['last_accessed'] = current_time
                logger.info(f"Cache hit for key: {key}")
                return cache_item.get('response')
                
            # Remove expired item
            del self.response_cache[key]
            
        return None
        
    def _add_to_cache(self, key: str, response: Dict[str, Any], ttl: Optional[int] = None):
        """Add a response to the cache."""
        if not ttl:
            ttl = self.cache_ttl
            
        current_time = time.time()
        
        self.response_cache[key] = {
            'response': response,
            'created': current_time,
            'last_accessed': current_time,
            'expiry': current_time + ttl
        }
        
        logger.info(f"Added to cache: {key}")
        
    def _load_available_jurisdictions(self) -> List[str]:
        """Load available jurisdictions from vector database."""
        try:
            # Get indexed jurisdictions
            jurisdictions = set()
            
            # Check all indexes for jurisdiction metadata
            for index_name, index_info in self.vector_db.metadata.get('indexes', {}).items():
                if 'jurisdictions' in index_info:
                    jurisdictions.update(index_info['jurisdictions'])
                    
            # Always include these common jurisdictions
            default_jurisdictions = {
                'federal', 'california', 'new_york', 'texas', 
                'florida', 'illinois'
            }
            
            jurisdictions.update(default_jurisdictions)
            return sorted(list(jurisdictions))
            
        except Exception as e:
            logger.error(f"Error loading jurisdictions: {str(e)}")
            return ['federal', 'california', 'new_york', 'texas']

# Example usage
async def example():
    # Initialize service
    service = LegalAssistantService()
    
    # Example query
    query = "What are my rights as a tenant in California if my landlord refuses to make repairs?"
    
    # Get response
    response = await service.get_legal_response_with_citations(query)
    
    # Print response
    print(f"Query: {query}\n")
    print(f"Response: {response['text']}\n")
    print("Citations:")
    for citation in response['citations']:
        print(f"- {citation['text']} ({citation.get('jurisdiction', 'Unknown')})")
        
    # Log interaction
    await service.log_interaction(query, response)

if __name__ == "__main__":
    asyncio.run(example()) 