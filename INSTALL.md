# Guía de Instalación Rápida

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Pasos de Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

### 5. Abrir en el navegador

Abre tu navegador y ve a: `http://localhost:5000`

## Verificar Instalación

Ejecuta los tests para verificar que todo funciona correctamente:

```bash
pytest
```

## Solución de Problemas

### Error: "ModuleNotFoundError"

Asegúrate de que el entorno virtual esté activado y las dependencias estén instaladas.

### Error: "Port already in use"

Cambia el puerto en `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Error al importar módulos

Asegúrate de estar en el directorio raíz del proyecto al ejecutar `app.py`.
