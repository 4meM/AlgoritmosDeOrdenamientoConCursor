from app.algorithms.base import AlgorithmBase
from app.algorithms.sorting import BubbleSort, MergeSort, QuickSort, HeapSort
from app.algorithms.search import LinearSearch, BinarySearch

# Registro de todos los algoritmos disponibles
AVAILABLE_ALGORITHMS = {
    'bubble_sort': BubbleSort(),
    'merge_sort': MergeSort(),
    'quick_sort': QuickSort(),
    'heap_sort': HeapSort(),
    'linear_search': LinearSearch(),
    'binary_search': BinarySearch(),
}

__all__ = ['AlgorithmBase', 'AVAILABLE_ALGORITHMS']
