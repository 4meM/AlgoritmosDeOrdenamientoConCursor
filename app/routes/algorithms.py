from flask import Blueprint, request, jsonify
from app.services import AlgorithmManager, DataGenerator
from typing import List, Any

algorithms_bp = Blueprint('algorithms', __name__, url_prefix='/api')
algorithm_manager = AlgorithmManager()
data_generator = DataGenerator()

@algorithms_bp.route('/algorithms', methods=['GET'])
def list_algorithms():
    """Lista todos los algoritmos disponibles"""
    try:
        algorithms = algorithm_manager.list_algorithms()
        return jsonify({
            'success': True,
            'algorithms': algorithms
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@algorithms_bp.route('/run', methods=['POST'])
def run_algorithm():
    """Ejecuta un algoritmo con datos proporcionados"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        algorithm_name = data.get('algorithm')
        input_data = data.get('data')
        target = data.get('target')  # Para algoritmos de búsqueda
        
        if not algorithm_name:
            return jsonify({
                'success': False,
                'error': 'Se requiere el nombre del algoritmo'
            }), 400
        
        if input_data is None:
            return jsonify({
                'success': False,
                'error': 'Se requieren datos de entrada'
            }), 400
        
        # Validar que input_data sea una lista
        if not isinstance(input_data, list):
            return jsonify({
                'success': False,
                'error': 'Los datos deben ser una lista'
            }), 400
        
        # Ejecutar algoritmo
        kwargs = {}
        if target is not None:
            kwargs['target'] = target
        
        result = algorithm_manager.execute_algorithm(algorithm_name, input_data, **kwargs)
        
        return jsonify({
            'success': True,
            'algorithm': algorithm_name,
            'result': result.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@algorithms_bp.route('/generate', methods=['POST'])
def generate_data():
    """Genera datos de prueba"""
    try:
        data = request.get_json() or {}
        
        data_type = data.get('type', 'random')
        size = data.get('size', 100)
        min_val = data.get('min_val', 1)
        max_val = data.get('max_val', 1000)
        
        if size < 1 or size > 100000:
            return jsonify({
                'success': False,
                'error': 'El tamaño debe estar entre 1 y 100,000'
            }), 400
        
        generated_data = data_generator.generate_custom(
            data_type,
            size,
            min_val=min_val,
            max_val=max_val
        )
        
        return jsonify({
            'success': True,
            'data': generated_data,
            'type': data_type,
            'size': size
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@algorithms_bp.route('/compare', methods=['POST'])
def compare_algorithms():
    """Compara múltiples algoritmos con los mismos datos"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        algorithm_names = data.get('algorithms', [])
        input_data = data.get('data')
        target = data.get('target')
        
        if not algorithm_names:
            return jsonify({
                'success': False,
                'error': 'Se requiere al menos un algoritmo'
            }), 400
        
        if input_data is None:
            return jsonify({
                'success': False,
                'error': 'Se requieren datos de entrada'
            }), 400
        
        if not isinstance(input_data, list):
            return jsonify({
                'success': False,
                'error': 'Los datos deben ser una lista'
            }), 400
        
        kwargs = {}
        if target is not None:
            kwargs['target'] = target
        
        results = algorithm_manager.compare_algorithms(algorithm_names, input_data, **kwargs)
        
        # Convertir resultados a diccionario
        comparison_results = {}
        for name, result in results.items():
            if isinstance(result, dict) and 'error' in result:
                comparison_results[name] = {'error': result['error']}
            else:
                comparison_results[name] = result.to_dict()
        
        return jsonify({
            'success': True,
            'results': comparison_results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@algorithms_bp.route('/history', methods=['GET'])
def get_history():
    """Obtiene el historial de ejecuciones"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = algorithm_manager.get_history(limit)
        return jsonify({
            'success': True,
            'history': history
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
