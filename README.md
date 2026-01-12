# Gestor de Algoritmos con Flask

Sistema web para ejecutar, comparar y visualizar algoritmos de ordenamiento y búsqueda con métricas de rendimiento (tiempo y memoria).

## Características

- ✅ **Algoritmos de Ordenamiento**: Bubble Sort, Merge Sort, Quick Sort, Heap Sort
- ✅ **Algoritmos de Búsqueda**: Búsqueda Lineal, Búsqueda Binaria
- ✅ **Medición de Complejidad Temporal**: Tiempo de ejecución en milisegundos
- ✅ **Medición de Complejidad Espacial**: Uso de memoria en KB
- ✅ **Generación de Datos**: Aleatorios, ordenados, inversamente ordenados
- ✅ **Comparación de Algoritmos**: Ejecuta múltiples algoritmos y compara resultados
- ✅ **Visualización**: Gráficos interactivos con Chart.js
- ✅ **API REST**: Endpoints para integración programática

## Estructura del Proyecto

```
.
├── app/
│   ├── __init__.py          # Factory de la aplicación Flask
│   ├── algorithms/          # Implementaciones de algoritmos
│   │   ├── __init__.py
│   │   ├── base.py          # Clase base AlgorithmBase
│   │   ├── sorting.py       # Algoritmos de ordenamiento
│   │   └── search.py        # Algoritmos de búsqueda
│   ├── services/            # Servicios del sistema
│   │   ├── __init__.py
│   │   ├── algorithm_manager.py  # Gestor de algoritmos
│   │   └── data_generator.py     # Generador de datos
│   ├── routes/              # Rutas Flask
│   │   ├── __init__.py
│   │   ├── main.py         # Rutas principales
│   │   └── algorithms.py   # API de algoritmos
│   ├── templates/          # Templates HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   └── compare.html
│   └── static/             # Archivos estáticos
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── main.js
│           └── compare.js
├── tests/                  # Tests unitarios
│   ├── test_algorithms.py
│   ├── test_services.py
│   └── test_routes.py
├── app.py                  # Punto de entrada
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd CURSOR
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno (opcional)

Copia `.env.example` a `.env` y ajusta las variables si es necesario:

```bash
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=tu-clave-secreta-aqui
```

## Uso

### Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

### Interfaz Web

1. **Página Principal (`/`)**: Ejecuta un algoritmo individual
   - Selecciona un algoritmo
   - Genera o ingresa datos
   - Visualiza resultados y métricas

2. **Página de Comparación (`/compare`)**: Compara múltiples algoritmos
   - Selecciona varios algoritmos
   - Usa los mismos datos para todos
   - Compara tiempos y memoria

### API REST

#### Listar algoritmos disponibles

```bash
GET /api/algorithms
```

#### Ejecutar un algoritmo

```bash
POST /api/run
Content-Type: application/json

{
    "algorithm": "bubble_sort",
    "data": [64, 34, 25, 12, 22, 11, 90]
}
```

Para algoritmos de búsqueda:

```bash
POST /api/run
Content-Type: application/json

{
    "algorithm": "linear_search",
    "data": [64, 34, 25, 12, 22, 11, 90],
    "target": 25
}
```

#### Generar datos de prueba

```bash
POST /api/generate
Content-Type: application/json

{
    "type": "random",
    "size": 100,
    "min_val": 1,
    "max_val": 1000
}
```

Tipos disponibles: `random`, `sorted`, `reverse`, `nearly_sorted`, `strings`

#### Comparar algoritmos

```bash
POST /api/compare
Content-Type: application/json

{
    "algorithms": ["bubble_sort", "merge_sort", "quick_sort"],
    "data": [64, 34, 25, 12, 22, 11, 90]
}
```

#### Obtener historial

```bash
GET /api/history?limit=10
```

## Agregar Nuevos Algoritmos

### 1. Crear la clase del algoritmo

Crea una nueva clase que herede de `AlgorithmBase`:

```python
from app.algorithms.base import AlgorithmBase
from typing import List, Any

class MiAlgoritmo(AlgorithmBase):
    def __init__(self):
        super().__init__(
            name="Mi Algoritmo",
            description="Descripción del algoritmo"
        )
    
    def execute(self, data: List[Any], **kwargs) -> Any:
        # Implementación del algoritmo
        # Usar self.comparisons y self.swaps para métricas
        # Usar self.steps.append() para registrar pasos
        return resultado
```

### 2. Registrar el algoritmo

En `app/algorithms/__init__.py`:

```python
from app.algorithms.mi_algoritmo import MiAlgoritmo

AVAILABLE_ALGORITHMS = {
    # ... algoritmos existentes ...
    'mi_algoritmo': MiAlgoritmo(),
}
```

### 3. El algoritmo estará disponible automáticamente

El nuevo algoritmo aparecerá en la interfaz web y en la API.

## Testing

Ejecutar todos los tests:

```bash
pytest
```

Ejecutar tests específicos:

```bash
pytest tests/test_algorithms.py
pytest tests/test_services.py
pytest tests/test_routes.py
```

Con cobertura:

```bash
pytest --cov=app tests/
```

## Algoritmos Implementados

### Ordenamiento

- **Bubble Sort**: O(n²) tiempo, O(1) espacio
- **Merge Sort**: O(n log n) tiempo, O(n) espacio
- **Quick Sort**: O(n log n) promedio, O(n²) peor caso, O(log n) espacio
- **Heap Sort**: O(n log n) tiempo, O(1) espacio

### Búsqueda

- **Linear Search**: O(n) tiempo, O(1) espacio
- **Binary Search**: O(log n) tiempo, O(1) espacio (requiere lista ordenada)

## Métricas Capturadas

- **Tiempo de Ejecución**: En milisegundos (ms)
- **Memoria Usada**: En kilobytes (KB)
- **Memoria Pico**: Memoria máxima durante la ejecución (KB)
- **Comparaciones**: Número de comparaciones realizadas
- **Intercambios**: Número de intercambios realizados (solo ordenamiento)
- **Pasos**: Número de pasos registrados

## Tecnologías Utilizadas

- **Backend**: Flask 3.0
- **Frontend**: Bootstrap 5, Chart.js
- **Testing**: pytest, pytest-flask
- **Medición**: time.perf_counter, tracemalloc

## Limitaciones de Seguridad

- Tamaño máximo de entrada: 100,000 elementos
- Validación de tipos de datos
- Límite de tamaño de contenido HTTP: 16MB

## Autor

Erik Ramos - Tópicos de Software 2025-B

## Licencia

Este proyecto es para fines educativos.
