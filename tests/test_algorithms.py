import pytest
from app.algorithms.sorting import BubbleSort, MergeSort, QuickSort, HeapSort
from app.algorithms.search import LinearSearch, BinarySearch

class TestSortingAlgorithms:
    """Tests para algoritmos de ordenamiento"""
    
    def test_bubble_sort(self):
        algo = BubbleSort()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = algo.execute(data)
        assert result == [11, 12, 22, 25, 34, 64, 90]
        assert algo.comparisons > 0
    
    def test_merge_sort(self):
        algo = MergeSort()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = algo.execute(data)
        assert result == [11, 12, 22, 25, 34, 64, 90]
        assert algo.comparisons > 0
    
    def test_quick_sort(self):
        algo = QuickSort()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = algo.execute(data)
        assert result == [11, 12, 22, 25, 34, 64, 90]
        assert algo.comparisons > 0
    
    def test_heap_sort(self):
        algo = HeapSort()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = algo.execute(data)
        assert result == [11, 12, 22, 25, 34, 64, 90]
        assert algo.comparisons > 0
    
    def test_sort_empty_list(self):
        algo = BubbleSort()
        result = algo.execute([])
        assert result == []
    
    def test_sort_single_element(self):
        algo = MergeSort()
        result = algo.execute([5])
        assert result == [5]
    
    def test_sort_already_sorted(self):
        algo = QuickSort()
        data = [1, 2, 3, 4, 5]
        result = algo.execute(data)
        assert result == [1, 2, 3, 4, 5]

class TestSearchAlgorithms:
    """Tests para algoritmos de búsqueda"""
    
    def test_linear_search_found(self):
        algo = LinearSearch()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = algo.execute(data, target=25)
        assert result['found'] == True
        assert result['index'] == 2
        assert result['value'] == 25
    
    def test_linear_search_not_found(self):
        algo = LinearSearch()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = algo.execute(data, target=100)
        assert result['found'] == False
        assert result['index'] == -1
    
    def test_binary_search_found(self):
        algo = BinarySearch()
        data = [11, 12, 22, 25, 34, 64, 90]
        result = algo.execute(data, target=25)
        assert result['found'] == True
        assert result['index'] == 3
        assert result['value'] == 25
    
    def test_binary_search_not_found(self):
        algo = BinarySearch()
        data = [11, 12, 22, 25, 34, 64, 90]
        result = algo.execute(data, target=100)
        assert result['found'] == False
        assert result['index'] == -1
    
    def test_binary_search_requires_sorted(self):
        algo = BinarySearch()
        data = [64, 34, 25, 12, 22, 11, 90]
        with pytest.raises(ValueError):
            algo.execute(data, target=25)

class TestMetrics:
    """Tests para métricas de algoritmos"""
    
    def test_bubble_sort_metrics(self):
        algo = BubbleSort()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = algo.run_with_metrics(data)
        
        assert result.result == [11, 12, 22, 25, 34, 64, 90]
        assert 'execution_time_ms' in result.metadata
        assert 'memory_used_kb' in result.metadata
        assert 'comparisons' in result.metadata
        assert result.metadata['input_size'] == 7
    
    def test_linear_search_metrics(self):
        algo = LinearSearch()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = algo.run_with_metrics(data, target=25)
        
        assert result.result['found'] == True
        assert 'execution_time_ms' in result.metadata
        assert 'memory_used_kb' in result.metadata
        assert 'comparisons' in result.metadata
