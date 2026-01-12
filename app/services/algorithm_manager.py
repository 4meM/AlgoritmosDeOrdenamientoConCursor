from app.algorithms import AVAILABLE_ALGORITHMS
from app.algorithms.base import AlgorithmBase, AlgorithmResult
from typing import List, Any, Dict, Optional

class AlgorithmManager:
    """Gestor de algoritmos para registro y ejecución"""
    
    def __init__(self):
        self.algorithms = AVAILABLE_ALGORITHMS.copy()
        self.execution_history = []
    
    def register_algorithm(self, name: str, algorithm: AlgorithmBase):
        """Registra un nuevo algoritmo"""
        self.algorithms[name] = algorithm
    
    def get_algorithm(self, name: str) -> Optional[AlgorithmBase]:
        """Obtiene un algoritmo por nombre"""
        return self.algorithms.get(name)
    
    def list_algorithms(self) -> Dict[str, Dict[str, str]]:
        """Lista todos los algoritmos disponibles"""
        return {
            name: {
                'name': algo.name,
                'description': algo.description
            }
            for name, algo in self.algorithms.items()
        }
    
    def execute_algorithm(self, name: str, data: List[Any], **kwargs) -> AlgorithmResult:
        """
        Ejecuta un algoritmo por nombre
        
        Args:
            name: Nombre del algoritmo
            data: Datos de entrada
            **kwargs: Argumentos adicionales para el algoritmo
            
        Returns:
            AlgorithmResult con resultado y métricas
            
        Raises:
            ValueError: Si el algoritmo no existe
            Exception: Si hay un error en la ejecución
        """
        algorithm = self.get_algorithm(name)
        if not algorithm:
            raise ValueError(f"Algoritmo '{name}' no encontrado")
        
        # Validar entrada
        self._validate_input(data)
        
        # Ejecutar algoritmo
        try:
            result = algorithm.run_with_metrics(data, **kwargs)
            
            # Guardar en historial
            self.execution_history.append({
                'algorithm': name,
                'input_size': len(data),
                'result': result.to_dict(),
                'timestamp': None  # Se puede agregar datetime si se necesita
            })
            
            return result
        except Exception as e:
            raise Exception(f"Error ejecutando algoritmo '{name}': {str(e)}")
    
    def _validate_input(self, data: List[Any]):
        """Valida los datos de entrada"""
        if not isinstance(data, list):
            raise ValueError("Los datos deben ser una lista")
        
        if len(data) == 0:
            raise ValueError("La lista no puede estar vacía")
        
        if len(data) > 100000:  # Límite de seguridad
            raise ValueError("La lista es demasiado grande (máximo 100,000 elementos)")
        
        # Validar tipos de datos
        if data:
            first_type = type(data[0])
            if not all(isinstance(item, (int, float, str)) for item in data):
                raise ValueError("Los elementos deben ser números o strings")
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Obtiene el historial de ejecuciones"""
        return self.execution_history[-limit:]
    
    def compare_algorithms(self, algorithm_names: List[str], data: List[Any], **kwargs) -> Dict[str, AlgorithmResult]:
        """
        Compara múltiples algoritmos con los mismos datos
        
        Args:
            algorithm_names: Lista de nombres de algoritmos a comparar
            data: Datos de entrada
            **kwargs: Argumentos adicionales
            
        Returns:
            Diccionario con resultados de cada algoritmo
        """
        results = {}
        
        for name in algorithm_names:
            try:
                result = self.execute_algorithm(name, data, **kwargs)
                results[name] = result
            except Exception as e:
                results[name] = {'error': str(e)}
        
        return results
