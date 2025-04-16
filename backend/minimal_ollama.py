import os
import time
import json
import hashlib
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import openai  # Add import for OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Cache configuration
CACHE_ENABLED = True
CACHE_TTL_SECONDS = 3600 * 24  # 24 hours
CACHE_DIR = os.path.join(os.path.dirname(__file__), "instance", "cache")

# Create cache directory if it doesn't exist
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Available models - only include those actually installed on the system
DEFAULT_MODEL = "llama3:8b"
AVAILABLE_MODELS = [
    # Local Models (via Ollama)
    "llama3:8b",     # Good balance of speed and quality
    "mistral",       # Good for legal reasoning
    "deepseek",      # Good for legal research
    "openhermes",    # Strong for legal QA
    
    # Cloud Models (via HuggingFace)
    "huggingface/mistral",      # Mistral-7B-Instruct v0.3 for general legal QA
    "huggingface/mixtral",      # Mixtral-8x7B for complex analysis
    "huggingface/legal-bert",   # Specialized for legal text
    "huggingface/legal-bertimbau", # Portuguese legal analysis
    "huggingface/legalbert-large", # Advanced legal classification
    "huggingface/legal-roberta",# Specialized for legal documents
    "huggingface/phi2",         # Quick, efficient responses
    "huggingface/phi-4",        # Advanced reasoning and code
    "huggingface/lawgpt",       # Specialized legal model
    
    # Other Options
    "openai",        # OpenAI integration option
    "static"         # Static fallback option (no LLM required)
]

# Legal data repository (simplified for demo)
LEGAL_TOPICS = {
    "tenancy": {
        "title": "Tenant Rights in California",
        "content": """
California tenants have the following key rights:
1. Right to a habitable dwelling
2. Protection against unlawful discrimination
3. Protection against unlawful eviction
4. Right to privacy
5. Security deposit protections
6. Right to sue for violations

Landlords must provide safe, clean, and habitable housing that complies with state and local housing codes. They must make necessary repairs and maintain the property.

California law prohibits evictions without proper notice and legal cause. Most evictions require a 3-day, 30-day, or 60-day notice depending on the circumstances.

Landlords may only enter a tenant's unit with proper notice (usually 24 hours) except in emergencies.

Security deposits are limited to 2 months' rent for unfurnished units or 3 months' rent for furnished units. Landlords must return deposits within 21 days after move-out, with an itemized statement of deductions.
        """
    },
    "employment": {
        "title": "Employment Rights in California",
        "content": """
California employees have these fundamental rights:
1. Minimum wage and overtime protections
2. Right to meal and rest breaks
3. Protection from workplace discrimination and harassment
4. Paid sick leave
5. Protection from retaliation
6. Right to workers' compensation for injuries

As of 2023, California's minimum wage is $15.50 per hour for all employers. Employees are entitled to overtime pay (1.5x regular rate) for work over 8 hours/day or 40 hours/week.

California prohibits workplace discrimination based on protected characteristics including race, religion, gender, age, disability, sexual orientation, and more.

Most California employees are entitled to paid sick leave, accruing at least 1 hour for every 30 hours worked.

Employers may not retaliate against employees for exercising their legal rights, including reporting violations or filing claims.
        """
    }
}

# Cache functions
def generate_cache_key(payload):
    """Generate a unique cache key based on the request payload"""
    cache_key = hashlib.md5(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return cache_key

def get_from_cache(cache_key):
    """Get response from cache if available and not expired"""
    if not CACHE_ENABLED:
        return None
        
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
            
            # Check if cache is expired
            timestamp = cached_data.get('timestamp', 0)
            current_time = time.time()
            
            if current_time - timestamp < CACHE_TTL_SECONDS:
                logger.info(f"Cache hit for key: {cache_key[:8]}...")
                # Add cached flag to help with development
                cached_data['response']['cached'] = True
                return cached_data['response']
            else:
                # Cache expired
                logger.info(f"Cache expired for key: {cache_key[:8]}...")
                os.remove(cache_file)
                return None
        except Exception as e:
            logger.error(f"Error reading from cache: {e}")
            return None
    return None

def save_to_cache(cache_key, response):
    """Save response to cache"""
    if not CACHE_ENABLED:
        return
        
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    try:
        cached_data = {
            'timestamp': time.time(),
            'response': response
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cached_data, f)
        
        logger.info(f"Cached response with key: {cache_key[:8]}...")
    except Exception as e:
        logger.error(f"Error saving to cache: {e}")

def clear_all_cache():
    """Clear all cache files"""
    cleared_count = 0
    try:
        for filename in os.listdir(CACHE_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(CACHE_DIR, filename)
                os.remove(file_path)
                cleared_count += 1
        return cleared_count
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return 0

def get_cache_stats():
    """Get cache statistics"""
    if not CACHE_ENABLED:
        return {
            'status': 'disabled',
            'entries': 0,
            'size_kb': 0,
            'ttl_seconds': 0
        }
        
    try:
        entries = 0
        total_size = 0
        
        for filename in os.listdir(CACHE_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(CACHE_DIR, filename)
                total_size += os.path.getsize(file_path)
                entries += 1
                
        return {
            'status': 'enabled',
            'entries': entries,
            'size_kb': round(total_size / 1024, 2),
            'ttl_seconds': CACHE_TTL_SECONDS
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }

# Helper functions
def get_static_response(topic, jurisdiction=None):
    """Get static response based on topic"""
    topic_data = LEGAL_TOPICS.get(topic.lower(), None)
    
    if not topic_data:
        return {
            "answer": f"I don't have information about {topic}.",
            "sources": [],
            "provider": "static_test",
            "model": "static"
        }
        
    # Add jurisdiction context if provided
    jurisdiction_text = ""
    if jurisdiction:
        jurisdiction_text = f" Note that this information is specifically for {jurisdiction}."
    
    return {
        "answer": f"{topic_data['title']}\n\n{topic_data['content']}{jurisdiction_text}",
        "sources": [{"title": topic_data['title'], "url": f"https://example.com/legal/{topic}"}],
        "provider": "static_test",
        "model": "static"
    }

def get_ollama_response(prompt, model=DEFAULT_MODEL):
    """Get response from Ollama API"""
    # Static test mode - return a fixed response for testing
    if model == "static":
        return get_static_response("general")
    
    # OpenAI mode - use OpenAI API instead of Ollama
    if model == "openai":
        return get_openai_response(prompt)
    
    # HuggingFace mode - use HuggingFace API instead of Ollama
    if model == "huggingface":
        return get_huggingface_response(prompt)
    
    # Format system message for legal focus
    system_message = """You are a helpful legal assistant providing information about basic rights and legal concepts. 
    Focus on giving accurate, clear legal information while noting that you are not providing legal advice. 
    If you don't know something, say so rather than making information up."""
    
    # Prepare request payload
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    
    try:
        # Make request to Ollama API
        logger.info(f"Sending request to Ollama with model {model}...")
        response = requests.post("http://localhost:11434/api/chat", json=payload, timeout=45)  # Increased timeout from 30 to 45 seconds
        
        if response.status_code == 200:
            data = response.json()
            # Format the response in our standard structure - safely access content
            message_content = ""
            if data and isinstance(data, dict):
                message = data.get("message", {})
                if isinstance(message, dict):
                    message_content = message.get("content", "")
            
            return {
                "answer": message_content,
                "sources": [],  # Ollama doesn't provide sources
                "provider": "ollama",
                "model": model
            }
        else:
            # API error, return error message
            error_message = f"Error from Ollama API: {response.status_code} - {response.text}"
            logger.error(error_message)
            return {
                "answer": "Sorry, I encountered an error communicating with the AI service.",
                "error": error_message,
                "sources": [],
                "provider": "error",
                "model": model
            }
    except Exception as e:
        # Connection error, return error message
        error_message = f"Failed to connect to Ollama API: {str(e)}"
        logger.error(error_message)
        return {
            "answer": "Sorry, I couldn't connect to the AI service. Please check if Ollama is running.",
            "error": error_message,
            "sources": [],
            "provider": "error",
            "model": model
        }

# Add helper function for safely accessing token count
def try_get_token_count(response):
    """Safely get token count from response with error handling"""
    try:
        if response and hasattr(response, 'usage'):
            return response.usage.total_tokens
        return 0
    except:
        return 0

# Add a function to use OpenAI API
def get_openai_response(prompt):
    """Get response from OpenAI API"""
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_api_key or openai_api_key == 'dummy_key':
        return {
            "answer": "OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.",
            "error": "API key missing",
            "sources": [],
            "provider": "error",
            "model": "openai"
        }
    
    try:
        # Initialize the OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Make request to OpenAI API
        logger.info(f"Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful legal assistant providing information about basic rights and legal concepts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Format the response in our standard structure
        if response and response.choices and len(response.choices) > 0:
            message_content = response.choices[0].message.content
            
            return {
                "answer": message_content,
                "sources": [],  # OpenAI doesn't provide sources
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "tokens": try_get_token_count(response)
            }
        else:
            return {
                "answer": "No response generated from OpenAI.",
                "error": "Empty response",
                "sources": [],
                "provider": "openai",
                "model": "gpt-3.5-turbo"
            }
    except Exception as e:
        # API error, return error message
        error_message = f"Error from OpenAI API: {str(e)}"
        logger.error(error_message)
        return {
            "answer": "Sorry, I encountered an error communicating with the OpenAI service.",
            "error": error_message,
            "sources": [],
            "provider": "error",
            "model": "openai"
        }

# Add a function to use HuggingFace API
def get_huggingface_response(prompt):
    """Get response from HuggingFace API"""
    import requests
    
    huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not huggingface_api_key or huggingface_api_key == 'dummy_key':
        return {
            "answer": "HuggingFace API key not configured. Please set HUGGINGFACE_API_KEY in your .env file.",
            "error": "API key missing",
            "sources": [],
            "provider": "error",
            "model": "huggingface"
        }
    
    try:
        # Using Mistral model from HuggingFace
        api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
        headers = {"Authorization": f"Bearer {huggingface_api_key}"}
        
        # Make request to HuggingFace API
        logger.info(f"Sending request to HuggingFace API...")
        
        # Format the prompt
        payload = {
            "inputs": f"<s>[INST] {prompt} [/INST]",
            "parameters": {
                "max_new_tokens": 1024,
                "temperature": 0.7
            }
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Format the response in our standard structure
        if response.status_code == 200:
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                
                # Extract the response part after [/INST]
                response_text = generated_text.split('[/INST]')[-1].strip()
                
                return {
                    "answer": response_text,
                    "sources": [],  # HuggingFace doesn't provide sources
                    "provider": "huggingface",
                    "model": "mistral-7b-instruct",
                    "tokens": len(response_text.split())
                }
            else:
                return {
                    "answer": "No valid response generated from HuggingFace.",
                    "error": "Empty or invalid response",
                    "sources": [],
                    "provider": "huggingface",
                    "model": "mistral-7b-instruct"
                }
        else:
            # API error, return error message
            error_message = f"Error from HuggingFace API: {response.status_code} - {response.text}"
            logger.error(error_message)
            return {
                "answer": "Sorry, I encountered an error communicating with the HuggingFace service.",
                "error": error_message,
                "sources": [],
                "provider": "error",
                "model": "huggingface"
            }
    except Exception as e:
        # Connection error, return error message
        error_message = f"Failed to connect to HuggingFace API: {str(e)}"
        logger.error(error_message)
        return {
            "answer": "Sorry, I couldn't connect to the HuggingFace service.",
            "error": error_message,
            "sources": [],
            "provider": "error",
            "model": "huggingface"
        }

# Add a function to check if Ollama is available
def check_ollama_connection():
    """Check if Ollama API is available and responsive"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            logger.info(f"Ollama connection successful. Models available: {len(models_data.get('models', []))}")
            return True
        else:
            logger.warning(f"Ollama responded with status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error connecting to Ollama: {str(e)}")
        return False

# API Routes
@app.route('/')
def home():
    logger.info("Health check endpoint accessed")
    return 'SmartProBono API is running!'

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json or {}  # Default to empty dict if None
    message = data.get('message', '')
    logger.info(f"Echo endpoint: Received data: {data}")
    return jsonify({
        "status": "success",
        "message": message,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/legal/chat', methods=['POST'])
def legal_chat():
    logger.info("Legal chat endpoint accessed")
    data = request.json or {}  # Default to empty dict if None
    message = data.get('message', '')
    model = data.get('model', DEFAULT_MODEL)
    
    logger.info(f"Chat endpoint: Processing message: {message[:50]}... using model: {model}")
    
    # Generate cache key from the request
    cache_key = generate_cache_key({
        "type": "chat",
        "message": message,
        "model": model
    })
    
    # Check cache first
    cached_response = get_from_cache(cache_key)
    if cached_response:
        return jsonify(cached_response)
    
    # Generate a response
    if model == "static":
        response = get_static_response("general")
    else:
        response = get_ollama_response(message, model)
    
    # Cache the response
    save_to_cache(cache_key, response)
    
    return jsonify(response)

@app.route('/api/legal/rights', methods=['POST'])
def legal_rights():
    logger.info("Legal rights endpoint accessed")
    data = request.json or {}  # Default to empty dict if None
    topic = data.get('topic', '')
    jurisdiction = data.get('jurisdiction', None)
    model = data.get('model', DEFAULT_MODEL)
    
    logger.info(f"Rights endpoint: Processing topic: {topic}, jurisdiction: {jurisdiction}")
    
    # Generate cache key from the request
    cache_key = generate_cache_key({
        "type": "rights",
        "topic": topic,
        "jurisdiction": jurisdiction,
        "model": model
    })
    
    # Check cache first
    cached_response = get_from_cache(cache_key)
    if cached_response:
        return jsonify(cached_response)
    
    # For static mode, use our built-in database
    if model == "static":
        response = get_static_response(topic, jurisdiction)
    else:
        # For AI mode, generate a prompt about the legal topic
        prompt = f"Explain basic legal rights regarding {topic}"
        if jurisdiction:
            prompt += f" in {jurisdiction}"
        prompt += ". Focus on fundamental rights and protections."
        
        response = get_ollama_response(prompt, model)
    
    # Cache the response
    save_to_cache(cache_key, response)
    
    return jsonify(response)

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    # In a real application, this might query Ollama for available models
    return jsonify({
        "status": "success",
        "models": AVAILABLE_MODELS
    })

@app.route('/api/cache/stats', methods=['GET'])
def cache_stats():
    """Get cache statistics"""
    return jsonify(get_cache_stats())

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear all cache entries"""
    cleared_entries = clear_all_cache()
    return jsonify({
        "status": "success",
        "cleared_entries": cleared_entries
    })

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run the minimal server')
    parser.add_argument('--port', type=int, default=5002, help='Port to run the server on')
    parser.add_argument('--no-cache', action='store_true', help='Disable response caching')
    parser.add_argument('--static-only', action='store_true', help='Use only static responses (no Ollama)')
    parser.add_argument('--openai', action='store_true', help='Use OpenAI API instead of Ollama')
    parser.add_argument('--huggingface', action='store_true', help='Use HuggingFace API instead of Ollama')
    
    args = parser.parse_args()
    
    if args.no_cache:
        CACHE_ENABLED = False
        logger.info("Response caching is DISABLED")
        
    if args.openai:
        DEFAULT_MODEL = "openai"
        logger.info("Using OpenAI API instead of Ollama")
    
    if args.huggingface:
        DEFAULT_MODEL = "huggingface"
        logger.info("Using HuggingFace API instead of Ollama")
    
    print(f"Starting SmartProBono minimal API with Ollama integration...")
    print(f"Cache directory: {CACHE_DIR}")
    print(f"Cache enabled: {CACHE_ENABLED}")
    print(f"Available models: {', '.join(AVAILABLE_MODELS)}")
    
    # Check Ollama connection on startup
    ollama_available = check_ollama_connection()
    if not ollama_available and not args.static_only and DEFAULT_MODEL != "openai":
        print("WARNING: Ollama is not available. LLM-based responses will fall back to static mode.")
        print("You can still use the API with the 'static' model option or the 'openai' model if configured.")
    
    app.run(host='0.0.0.0', port=args.port, debug=True) 