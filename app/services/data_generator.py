import random
from typing import List, Any

class DataGenerator:
    """Generador de datasets para pruebas"""
    
    @staticmethod
    def generate_random(size: int, min_val: int = 1, max_val: int = 1000) -> List[int]:
        """Genera una lista aleatoria de enteros"""
        return [random.randint(min_val, max_val) for _ in range(size)]
    
    @staticmethod
    def generate_sorted(size: int, min_val: int = 1, max_val: int = 1000) -> List[int]:
        """Genera una lista ordenada de enteros"""
        return sorted(DataGenerator.generate_random(size, min_val, max_val))
    
    @staticmethod
    def generate_reverse_sorted(size: int, min_val: int = 1, max_val: int = 1000) -> List[int]:
        """Genera una lista inversamente ordenada de enteros"""
        return sorted(DataGenerator.generate_random(size, min_val, max_val), reverse=True)
    
    @staticmethod
    def generate_nearly_sorted(size: int, min_val: int = 1, max_val: int = 1000, swaps: int = 10) -> List[int]:
        """Genera una lista casi ordenada con algunos elementos intercambiados"""
        arr = DataGenerator.generate_sorted(size, min_val, max_val)
        for _ in range(swaps):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    
    @staticmethod
    def generate_strings(size: int, min_length: int = 3, max_length: int = 10) -> List[str]:
        """Genera una lista aleatoria de strings"""
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return [
            ''.join(random.choice(chars) for _ in range(random.randint(min_length, max_length)))
            for _ in range(size)
        ]
    
    @staticmethod
    def generate_custom(data_type: str, size: int, **kwargs) -> List[Any]:
        """
        Genera datos personalizados según el tipo especificado
        
        Args:
            data_type: Tipo de datos ('random', 'sorted', 'reverse', 'nearly_sorted', 'strings')
            size: Tamaño de la lista
            **kwargs: Parámetros adicionales según el tipo
        """
        generators = {
            'random': DataGenerator.generate_random,
            'sorted': DataGenerator.generate_sorted,
            'reverse': DataGenerator.generate_reverse_sorted,
            'nearly_sorted': DataGenerator.generate_nearly_sorted,
            'strings': DataGenerator.generate_strings
        }
        
        generator = generators.get(data_type)
        if not generator:
            raise ValueError(f"Tipo de datos '{data_type}' no soportado")
        
        return generator(size, **kwargs)
