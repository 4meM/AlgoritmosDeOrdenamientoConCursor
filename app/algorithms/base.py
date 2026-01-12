from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
import time
import tracemalloc

class AlgorithmResult:
    """Clase para encapsular el resultado de un algoritmo"""
    def __init__(self, result: Any, metadata: Dict[str, Any] = None):
        self.result = result
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el resultado a diccionario"""
        return {
            'result': self.result,
            'metadata': self.metadata
        }

class AlgorithmBase(ABC):
    """Clase base abstracta para todos los algoritmos"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.comparisons = 0
        self.swaps = 0
        self.steps = []
    
    @abstractmethod
    def execute(self, data: List[Any], **kwargs) -> Any:
        """
        Ejecuta el algoritmo sobre los datos proporcionados
        
        Args:
            data: Lista de datos a procesar
            **kwargs: Argumentos adicionales específicos del algoritmo
            
        Returns:
            Resultado del algoritmo
        """
        pass
    
    def reset_metrics(self):
        """Reinicia las métricas del algoritmo"""
        self.comparisons = 0
        self.swaps = 0
        self.steps = []
    
    def run_with_metrics(self, data: List[Any], **kwargs) -> AlgorithmResult:
        """
        Ejecuta el algoritmo y mide tiempo y memoria
        
        Args:
            data: Lista de datos a procesar
            **kwargs: Argumentos adicionales específicos del algoritmo
            
        Returns:
            AlgorithmResult con resultado y métricas
        """
        # Reiniciar métricas
        self.reset_metrics()
        
        # Medir memoria
        tracemalloc.start()
        memory_before = tracemalloc.get_traced_memory()[0]
        
        # Medir tiempo
        start_time = time.perf_counter()
        
        # Ejecutar algoritmo
        try:
            result = self.execute(data.copy(), **kwargs)
        except Exception as e:
            tracemalloc.stop()
            raise e
        
        end_time = time.perf_counter()
        memory_after, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Calcular métricas
        execution_time = (end_time - start_time) * 1000  # Convertir a milisegundos
        memory_used = (memory_after - memory_before) / 1024  # Convertir a KB
        memory_peak_kb = memory_peak / 1024  # Convertir a KB
        
        metadata = {
            'execution_time_ms': round(execution_time, 4),
            'memory_used_kb': round(memory_used, 4),
            'memory_peak_kb': round(memory_peak_kb, 4),
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'input_size': len(data),
            'steps_count': len(self.steps)
        }
        
        return AlgorithmResult(result, metadata)
    
    def __str__(self):
        return f"{self.name}: {self.description}"
