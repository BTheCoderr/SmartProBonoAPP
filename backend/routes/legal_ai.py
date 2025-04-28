from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
from services.openai_service import get_legal_response
from services.ai_service_manager import ai_service_manager, AIProvider
import asyncio

load_dotenv()

bp = Blueprint('legal_ai', __name__, url_prefix='/api/legal')

@bp.route('/chat', methods=['POST'])
async def chat():
    try:
        data = request.json or {}
        message = data.get('message')
        task_type = data.get('task_type', 'chat')
        requested_model = data.get('model', 'mistral')  # Default to mistral if not specified
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        try:
            # Try requested model first
            provider = AIProvider(requested_model)
            response = await ai_service_manager.get_response(
                prompt=message,
                provider=provider,
                task_type=task_type
            )
            
            return jsonify({
                'response': response['text'],
                'model': response['model'],
                'provider': response['provider'],
                'tokens': response['tokens'],
                'status': 'success'
            })
        except Exception as model_error:
            # If requested model fails, try OpenAI as fallback
            try:
                response = await ai_service_manager.get_response(
                    prompt=message,
                    provider=AIProvider.OPENAI,
                    task_type='default'
                )
                return jsonify({
                    'response': response['text'],
                    'model': response['model'],
                    'provider': response['provider'],
                    'tokens': response['tokens'],
                    'status': 'success'
                })
            except Exception as fallback_error:
                return jsonify({
                    'error': f'All providers failed. Primary error: {str(model_error)}. Fallback error: {str(fallback_error)}'
                }), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Ensure cleanup of resources
        if ai_service_manager.cleanup():
            await ai_service_manager.cleanup()

@bp.route('/analyze', methods=['POST'])
async def analyze_document():
    try:
        data = request.json or {}
        document = data.get('document')
        analysis_type = data.get('analysis_type', 'legal_research')
        
        if not document:
            return jsonify({'error': 'Document is required'}), 400

        # Use Falcon for deep legal analysis
        response = await ai_service_manager.get_response(
            prompt=document,
            provider=AIProvider.FALCON,
            task_type=analysis_type
        )
        
        return jsonify({
            'analysis': response['text'],
            'model': response['model'],
            'provider': response['provider'],
            'tokens': response['tokens'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/draft', methods=['POST'])
async def draft_document():
    try:
        data = request.json or {}
        template = data.get('template')
        details = data.get('details')
        doc_type = data.get('doc_type', 'document_drafting')
        
        if not template or not details:
            return jsonify({'error': 'Template and details are required'}), 400

        # Use Llama for document drafting
        response = await ai_service_manager.get_response(
            prompt=f"Template: {template}\nDetails: {details}",
            provider=AIProvider.LLAMA,
            task_type=doc_type
        )
        
        return jsonify({
            'document': response['text'],
            'model': response['model'],
            'provider': response['provider'],
            'tokens': response['tokens'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/rights', methods=['POST'])
async def explain_rights():
    try:
        data = request.json or {}
        topic = data.get('topic')
        jurisdiction = data.get('jurisdiction')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400

        prompt = f"Explain legal rights regarding {topic}"
        if jurisdiction:
            prompt += f" in {jurisdiction}"

        response = await ai_service_manager.get_response(
            prompt=prompt,
            provider=AIProvider.MISTRAL,
            task_type='rights_explanation'
        )
        
        return jsonify({
            'explanation': response['text'],
            'model': response['model'],
            'provider': response['provider'],
            'tokens': response['tokens'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/procedure', methods=['POST'])
async def explain_procedure():
    try:
        data = request.json or {}
        procedure_type = data.get('procedure_type')
        jurisdiction = data.get('jurisdiction')
        
        if not procedure_type:
            return jsonify({'error': 'Procedure type is required'}), 400

        prompt = f"Explain the procedure for {procedure_type}"
        if jurisdiction:
            prompt += f" in {jurisdiction}"

        response = await ai_service_manager.get_response(
            prompt=prompt,
            provider=AIProvider.MISTRAL,
            task_type='procedure_guidance'
        )
        
        return jsonify({
            'guidance': response['text'],
            'model': response['model'],
            'provider': response['provider'],
            'tokens': response['tokens'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/precedent', methods=['POST'])
async def search_precedents():
    try:
        data = request.json or {}
        case_details = data.get('case_details')
        jurisdiction = data.get('jurisdiction')
        
        if not case_details:
            return jsonify({'error': 'Case details are required'}), 400

        prompt = f"Find relevant precedents for: {case_details}"
        if jurisdiction:
            prompt += f" in {jurisdiction}"

        response = await ai_service_manager.get_response(
            prompt=prompt,
            provider=AIProvider.FALCON,
            task_type='precedent_search'
        )
        
        return jsonify({
            'precedents': response['text'],
            'model': response['model'],
            'provider': response['provider'],
            'tokens': response['tokens'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/statute', methods=['POST'])
async def interpret_statute():
    try:
        data = request.json or {}
        statute = data.get('statute')
        context = data.get('context')
        
        if not statute:
            return jsonify({'error': 'Statute reference is required'}), 400

        prompt = f"Interpret statute: {statute}"
        if context:
            prompt += f"\nContext: {context}"

        response = await ai_service_manager.get_response(
            prompt=prompt,
            provider=AIProvider.FALCON,
            task_type='statute_interpretation'
        )
        
        return jsonify({
            'interpretation': response['text'],
            'model': response['model'],
            'provider': response['provider'],
            'tokens': response['tokens'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/review-agreement', methods=['POST'])
async def review_agreement():
    try:
        data = request.json or {}
        agreement = data.get('agreement')
        focus_areas = data.get('focus_areas', [])
        
        if not agreement:
            return jsonify({'error': 'Agreement text is required'}), 400

        prompt = f"Review this agreement: {agreement}"
        if focus_areas:
            prompt += f"\nFocus on these areas: {', '.join(focus_areas)}"

        response = await ai_service_manager.get_response(
            prompt=prompt,
            provider=AIProvider.LLAMA,
            task_type='agreement_review'
        )
        
        return jsonify({
            'review': response['text'],
            'model': response['model'],
            'provider': response['provider'],
            'tokens': response['tokens'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/form-guidance', methods=['POST'])
async def provide_form_guidance():
    try:
        data = request.json or {}
        form_type = data.get('form_type')
        jurisdiction = data.get('jurisdiction')
        
        if not form_type:
            return jsonify({'error': 'Form type is required'}), 400

        prompt = f"Provide guidance for completing {form_type} form"
        if jurisdiction:
            prompt += f" in {jurisdiction}"

        response = await ai_service_manager.get_response(
            prompt=prompt,
            provider=AIProvider.LLAMA,
            task_type='legal_form_filling'
        )
        
        return jsonify({
            'guidance': response['text'],
            'model': response['model'],
            'provider': response['provider'],
            'tokens': response['tokens'],
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 