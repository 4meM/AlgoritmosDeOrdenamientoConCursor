from app.algorithms.base import AlgorithmBase
from typing import List, Any
import heapq

class BubbleSort(AlgorithmBase):
    """Implementación de Bubble Sort"""
    
    def __init__(self):
        super().__init__(
            name="Bubble Sort",
            description="Ordena una lista comparando elementos adyacentes e intercambiándolos si están en el orden incorrecto"
        )
    
    def execute(self, data: List[Any], **kwargs) -> List[Any]:
        """Ejecuta Bubble Sort"""
        arr = data.copy()
        n = len(arr)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                self.comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swaps += 1
                    swapped = True
                    self.steps.append({
                        'action': 'swap',
                        'indices': [j, j + 1],
                        'array': arr.copy()
                    })
            
            if not swapped:
                break
        
        return arr

class MergeSort(AlgorithmBase):
    """Implementación de Merge Sort"""
    
    def __init__(self):
        super().__init__(
            name="Merge Sort",
            description="Ordena una lista dividiéndola en mitades, ordenándolas recursivamente y luego fusionándolas"
        )
    
    def execute(self, data: List[Any], **kwargs) -> List[Any]:
        """Ejecuta Merge Sort"""
        arr = data.copy()
        return self._merge_sort(arr)
    
    def _merge_sort(self, arr: List[Any]) -> List[Any]:
        """Función recursiva de Merge Sort"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[Any], right: List[Any]) -> List[Any]:
        """Fusiona dos listas ordenadas"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            self.comparisons += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        self.steps.append({
            'action': 'merge',
            'left': left,
            'right': right,
            'result': result.copy()
        })
        
        return result

class QuickSort(AlgorithmBase):
    """Implementación de Quick Sort"""
    
    def __init__(self):
        super().__init__(
            name="Quick Sort",
            description="Ordena una lista usando el algoritmo de partición rápida"
        )
    
    def execute(self, data: List[Any], **kwargs) -> List[Any]:
        """Ejecuta Quick Sort"""
        arr = data.copy()
        self._quick_sort(arr, 0, len(arr) - 1)
        return arr
    
    def _quick_sort(self, arr: List[Any], low: int, high: int):
        """Función recursiva de Quick Sort"""
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick_sort(arr, low, pi - 1)
            self._quick_sort(arr, pi + 1, high)
    
    def _partition(self, arr: List[Any], low: int, high: int) -> int:
        """Particiona el array y retorna el índice del pivote"""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            self.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.swaps += 1
                self.steps.append({
                    'action': 'swap',
                    'indices': [i, j],
                    'array': arr.copy()
                })
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.swaps += 1
        self.steps.append({
            'action': 'pivot',
            'pivot_index': i + 1,
            'array': arr.copy()
        })
        
        return i + 1

class HeapSort(AlgorithmBase):
    """Implementación de Heap Sort"""
    
    def __init__(self):
        super().__init__(
            name="Heap Sort",
            description="Ordena una lista usando una estructura de heap (montículo)"
        )
    
    def execute(self, data: List[Any], **kwargs) -> List[Any]:
        """Ejecuta Heap Sort"""
        arr = data.copy()
        n = len(arr)
        
        # Construir max heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        
        # Extraer elementos del heap uno por uno
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self.swaps += 1
            self.steps.append({
                'action': 'swap',
                'indices': [0, i],
                'array': arr.copy()
            })
            self._heapify(arr, i, 0)
        
        return arr
    
    def _heapify(self, arr: List[Any], n: int, i: int):
        """Convierte un subárbol en un max heap"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            self.comparisons += 1
            if arr[left] > arr[largest]:
                largest = left
        
        if right < n:
            self.comparisons += 1
            if arr[right] > arr[largest]:
                largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.swaps += 1
            self.steps.append({
                'action': 'heapify',
                'indices': [i, largest],
                'array': arr.copy()
            })
            self._heapify(arr, n, largest)
