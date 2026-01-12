import pytest
from app.services import AlgorithmManager, DataGenerator

class TestAlgorithmManager:
    """Tests para AlgorithmManager"""
    
    def test_list_algorithms(self):
        manager = AlgorithmManager()
        algorithms = manager.list_algorithms()
        
        assert isinstance(algorithms, dict)
        assert 'bubble_sort' in algorithms
        assert 'merge_sort' in algorithms
        assert 'linear_search' in algorithms
    
    def test_execute_algorithm(self):
        manager = AlgorithmManager()
        data = [64, 34, 25, 12, 22, 11, 90]
        result = manager.execute_algorithm('bubble_sort', data)
        
        assert result.result == [11, 12, 22, 25, 34, 64, 90]
        assert 'execution_time_ms' in result.metadata
    
    def test_execute_nonexistent_algorithm(self):
        manager = AlgorithmManager()
        with pytest.raises(ValueError):
            manager.execute_algorithm('nonexistent', [1, 2, 3])
    
    def test_validate_input_empty(self):
        manager = AlgorithmManager()
        with pytest.raises(ValueError):
            manager.execute_algorithm('bubble_sort', [])
    
    def test_validate_input_not_list(self):
        manager = AlgorithmManager()
        with pytest.raises(ValueError):
            manager.execute_algorithm('bubble_sort', "not a list")
    
    def test_compare_algorithms(self):
        manager = AlgorithmManager()
        data = [64, 34, 25, 12, 22, 11, 90]
        results = manager.compare_algorithms(['bubble_sort', 'merge_sort'], data)
        
        assert 'bubble_sort' in results
        assert 'merge_sort' in results
        assert results['bubble_sort'].result == results['merge_sort'].result

class TestDataGenerator:
    """Tests para DataGenerator"""
    
    def test_generate_random(self):
        data = DataGenerator.generate_random(10)
        assert len(data) == 10
        assert all(isinstance(x, int) for x in data)
    
    def test_generate_sorted(self):
        data = DataGenerator.generate_sorted(10)
        assert len(data) == 10
        assert data == sorted(data)
    
    def test_generate_reverse_sorted(self):
        data = DataGenerator.generate_reverse_sorted(10)
        assert len(data) == 10
        assert data == sorted(data, reverse=True)
    
    def test_generate_strings(self):
        data = DataGenerator.generate_strings(5)
        assert len(data) == 5
        assert all(isinstance(x, str) for x in data)
    
    def test_generate_custom(self):
        data = DataGenerator.generate_custom('random', 10)
        assert len(data) == 10
        
        data = DataGenerator.generate_custom('sorted', 10)
        assert len(data) == 10
        assert data == sorted(data)
    
    def test_generate_custom_invalid_type(self):
        with pytest.raises(ValueError):
            DataGenerator.generate_custom('invalid', 10)
