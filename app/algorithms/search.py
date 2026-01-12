from app.algorithms.base import AlgorithmBase
from typing import List, Any, Optional, Dict

class LinearSearch(AlgorithmBase):
    """Implementación de Búsqueda Lineal"""
    
    def __init__(self):
        super().__init__(
            name="Linear Search",
            description="Busca un elemento en una lista recorriéndola secuencialmente"
        )
    
    def execute(self, data: List[Any], **kwargs) -> Dict[str, Any]:
        """Ejecuta búsqueda lineal"""
        target = kwargs.get('target')
        if target is None:
            raise ValueError("Se requiere el parámetro 'target' para la búsqueda")
        
        for i, item in enumerate(data):
            self.comparisons += 1
            self.steps.append({
                'action': 'compare',
                'index': i,
                'value': item,
                'target': target
            })
            
            if item == target:
                return {
                    'found': True,
                    'index': i,
                    'value': item
                }
        
        return {
            'found': False,
            'index': -1,
            'value': None
        }

class BinarySearch(AlgorithmBase):
    """Implementación de Búsqueda Binaria"""
    
    def __init__(self):
        super().__init__(
            name="Binary Search",
            description="Busca un elemento en una lista ordenada dividiendo repetidamente el espacio de búsqueda a la mitad"
        )
    
    def execute(self, data: List[Any], **kwargs) -> Dict[str, Any]:
        """Ejecuta búsqueda binaria"""
        target = kwargs.get('target')
        if target is None:
            raise ValueError("Se requiere el parámetro 'target' para la búsqueda")
        
        # Verificar si la lista está ordenada
        if data != sorted(data):
            raise ValueError("La lista debe estar ordenada para usar Binary Search")
        
        left, right = 0, len(data) - 1
        
        while left <= right:
            mid = (left + right) // 2
            mid_value = data[mid]
            
            self.comparisons += 1
            self.steps.append({
                'action': 'compare',
                'left': left,
                'right': right,
                'mid': mid,
                'value': mid_value,
                'target': target
            })
            
            if mid_value == target:
                return {
                    'found': True,
                    'index': mid,
                    'value': mid_value
                }
            elif mid_value < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return {
            'found': False,
            'index': -1,
            'value': None
        }
