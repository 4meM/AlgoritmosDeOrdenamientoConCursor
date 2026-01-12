let algorithms = {};
let metricsChart = null;

// Cargar algoritmos disponibles al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    loadAlgorithms();
    
    const algorithmSelect = document.getElementById('algorithmSelect');
    algorithmSelect.addEventListener('change', function() {
        const selectedAlgorithm = this.value;
        const isSearchAlgorithm = selectedAlgorithm.includes('search');
        document.getElementById('targetInputContainer').style.display = isSearchAlgorithm ? 'block' : 'none';
    });
});

async function loadAlgorithms() {
    try {
        const response = await fetch('/api/algorithms');
        const data = await response.json();
        
        if (data.success) {
            algorithms = data.algorithms;
            const select = document.getElementById('algorithmSelect');
            select.innerHTML = '<option value="">Seleccione un algoritmo...</option>';
            
            for (const [key, algo] of Object.entries(algorithms)) {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = `${algo.name} - ${algo.description}`;
                select.appendChild(option);
            }
        }
    } catch (error) {
        console.error('Error cargando algoritmos:', error);
        showError('Error al cargar los algoritmos disponibles');
    }
}

async function generateData(type) {
    const size = parseInt(document.getElementById('dataSize').value) || 100;
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: type,
                size: size
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('dataInput').value = JSON.stringify(data.data);
        } else {
            showError(data.error || 'Error generando datos');
        }
    } catch (error) {
        console.error('Error generando datos:', error);
        showError('Error al generar datos');
    }
}

async function runAlgorithm() {
    const algorithmName = document.getElementById('algorithmSelect').value;
    const dataInput = document.getElementById('dataInput').value;
    const targetInput = document.getElementById('targetInput').value;
    
    if (!algorithmName) {
        showError('Por favor seleccione un algoritmo');
        return;
    }
    
    if (!dataInput.trim()) {
        showError('Por favor ingrese o genere datos');
        return;
    }
    
    let inputData;
    try {
        inputData = JSON.parse(dataInput);
    } catch (e) {
        showError('Los datos deben ser un array JSON válido');
        return;
    }
    
    const requestBody = {
        algorithm: algorithmName,
        data: inputData
    };
    
    if (targetInput) {
        requestBody.target = parseFloat(targetInput) || parseInt(targetInput);
    }
    
    // Mostrar loading
    const resultsCard = document.getElementById('resultsCard');
    const resultsContent = document.getElementById('resultsContent');
    resultsCard.style.display = 'block';
    resultsContent.innerHTML = '<div class="loading">Ejecutando algoritmo...</div>';
    
    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.result);
            updateMetricsChart(data.result);
        } else {
            showError(data.error || 'Error ejecutando algoritmo');
        }
    } catch (error) {
        console.error('Error ejecutando algoritmo:', error);
        showError('Error al ejecutar el algoritmo');
    }
}

function displayResults(result) {
    const resultsContent = document.getElementById('resultsContent');
    
    let html = '<div class="algorithm-result">';
    html += `<h6>Resultado:</h6>`;
    html += `<pre class="bg-light p-3 rounded">${JSON.stringify(result.result, null, 2)}</pre>`;
    
    html += '<h6 class="mt-3">Métricas:</h6>';
    html += `<div class="metric-badge">Tiempo: ${result.metadata.execution_time_ms} ms</div>`;
    html += `<div class="metric-badge">Memoria: ${result.metadata.memory_used_kb} KB</div>`;
    html += `<div class="metric-badge">Memoria Pico: ${result.metadata.memory_peak_kb} KB</div>`;
    html += `<div class="metric-badge">Comparaciones: ${result.metadata.comparisons}</div>`;
    if (result.metadata.swaps !== undefined) {
        html += `<div class="metric-badge">Intercambios: ${result.metadata.swaps}</div>`;
    }
    html += `<div class="metric-badge">Tamaño Entrada: ${result.metadata.input_size}</div>`;
    
    html += '</div>';
    
    resultsContent.innerHTML = html;
}

function updateMetricsChart(result) {
    const ctx = document.getElementById('metricsChart').getContext('2d');
    
    if (metricsChart) {
        metricsChart.destroy();
    }
    
    metricsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Tiempo (ms)', 'Memoria (KB)', 'Memoria Pico (KB)', 'Comparaciones'],
            datasets: [{
                label: 'Métricas',
                data: [
                    result.metadata.execution_time_ms,
                    result.metadata.memory_used_kb,
                    result.metadata.memory_peak_kb,
                    result.metadata.comparisons / 10 // Escalar para visualización
                ],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)'
                ]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function showError(message) {
    const resultsCard = document.getElementById('resultsCard');
    const resultsContent = document.getElementById('resultsContent');
    resultsCard.style.display = 'block';
    resultsContent.innerHTML = `<div class="error-message">${message}</div>`;
}
