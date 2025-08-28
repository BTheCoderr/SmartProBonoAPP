from flask import Blueprint, jsonify
from services.performance_monitor import performance_monitor
from config.ai_config import AI_CONFIG

performance = Blueprint('performance', __name__, url_prefix='/api/performance')

@performance.route('/<model>', methods=['GET'])
def get_model_performance(model):
    """Get performance metrics for a specific model or all models"""
    try:
        if model == 'all':
            # Aggregate metrics for all models
            all_metrics = {}
            total_requests = 0
            total_response_time = 0
            total_success = 0
            
            for model_name in AI_CONFIG['models'].keys():
                metrics = performance_monitor.get_model_performance(model_name)
                all_metrics[model_name] = metrics
                total_requests += metrics['total_requests']
                total_response_time += (metrics['average_response_time'] * metrics['total_requests'])
                total_success += (metrics['success_rate'] * metrics['total_requests'] / 100)

            if total_requests > 0:
                return jsonify({
                    'average_response_time': total_response_time / total_requests,
                    'success_rate': (total_success / total_requests) * 100,
                    'total_requests': total_requests,
                    'error_rate': 100 - ((total_success / total_requests) * 100),
                    'model_breakdown': all_metrics
                })
            else:
                return jsonify({
                    'average_response_time': 0,
                    'success_rate': 0,
                    'total_requests': 0,
                    'error_rate': 0,
                    'model_breakdown': all_metrics
                })
        else:
            # Get metrics for specific model
            if model not in AI_CONFIG['models']:
                return jsonify({'error': f'Invalid model: {model}'}), 400
                
            metrics = performance_monitor.get_model_performance(model)
            return jsonify(metrics)

    except Exception as e:
        return jsonify({'error': str(e)}), 500 