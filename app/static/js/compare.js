let algorithms = {};
let timeChart = null;
let memoryChart = null;

document.addEventListener('DOMContentLoaded', function() {
    loadAlgorithms();
});

async function loadAlgorithms() {
    try {
        const response = await fetch('/api/algorithms');
        const data = await response.json();
        
        if (data.success) {
            algorithms = data.algorithms;
            const container = document.getElementById('algorithmCheckboxes');
            container.innerHTML = '';
            
            for (const [key, algo] of Object.entries(algorithms)) {
                const div = document.createElement('div');
                div.className = 'form-check mb-2';
                div.innerHTML = `
                    <input class="form-check-input" type="checkbox" value="${key}" id="algo_${key}">
                    <label class="form-check-label" for="algo_${key}">
                        ${algo.name} - ${algo.description}
                    </label>
                `;
                container.appendChild(div);
            }
        }
    } catch (error) {
        console.error('Error cargando algoritmos:', error);
        showError('Error al cargar los algoritmos disponibles');
    }
}

async function generateCompareData(type) {
    const size = parseInt(document.getElementById('compareDataSize').value) || 100;
    
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
            document.getElementById('compareDataInput').value = JSON.stringify(data.data);
        } else {
            showError(data.error || 'Error generando datos');
        }
    } catch (error) {
        console.error('Error generando datos:', error);
        showError('Error al generar datos');
    }
}

async function compareAlgorithms() {
    const checkboxes = document.querySelectorAll('#algorithmCheckboxes input[type="checkbox"]:checked');
    const selectedAlgorithms = Array.from(checkboxes).map(cb => cb.value);
    
    if (selectedAlgorithms.length === 0) {
        showError('Por favor seleccione al menos un algoritmo');
        return;
    }
    
    const dataInput = document.getElementById('compareDataInput').value;
    const targetInput = document.getElementById('compareTargetInput').value;
    
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
    
    // Mostrar/ocultar campo target según si hay algoritmos de búsqueda
    const hasSearchAlgorithms = selectedAlgorithms.some(name => name.includes('search'));
    document.getElementById('compareTargetContainer').style.display = hasSearchAlgorithms ? 'block' : 'none';
    
    const requestBody = {
        algorithms: selectedAlgorithms,
        data: inputData
    };
    
    if (targetInput && hasSearchAlgorithms) {
        requestBody.target = parseFloat(targetInput) || parseInt(targetInput);
    }
    
    // Mostrar loading
    const resultsCard = document.getElementById('compareResultsCard');
    const resultsContent = document.getElementById('compareResultsContent');
    resultsCard.style.display = 'block';
    resultsContent.innerHTML = '<div class="loading">Comparando algoritmos...</div>';
    
    try {
        const response = await fetch('/api/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayCompareResults(data.results);
            updateCompareCharts(data.results);
        } else {
            showError(data.error || 'Error comparando algoritmos');
        }
    } catch (error) {
        console.error('Error comparando algoritmos:', error);
        showError('Error al comparar algoritmos');
    }
}

function displayCompareResults(results) {
    const resultsContent = document.getElementById('compareResultsContent');
    let html = '';
    
    for (const [algoName, result] of Object.entries(results)) {
        if (result.error) {
            html += `<div class="algorithm-result border-danger">`;
            html += `<h6>${algorithms[algoName]?.name || algoName}</h6>`;
            html += `<div class="error-message">${result.error}</div>`;
            html += `</div>`;
        } else {
            html += `<div class="algorithm-result">`;
            html += `<h6>${algorithms[algoName]?.name || algoName}</h6>`;
            html += `<pre class="bg-light p-2 rounded small">${JSON.stringify(result.result, null, 2)}</pre>`;
            html += `<div class="mt-2">`;
            html += `<span class="metric-badge">Tiempo: ${result.metadata.execution_time_ms} ms</span>`;
            html += `<span class="metric-badge">Memoria: ${result.metadata.memory_used_kb} KB</span>`;
            html += `<span class="metric-badge">Comparaciones: ${result.metadata.comparisons}</span>`;
            html += `</div>`;
            html += `</div>`;
        }
    }
    
    resultsContent.innerHTML = html;
}

function updateCompareCharts(results) {
    const algorithmNames = [];
    const times = [];
    const memories = [];
    
    for (const [algoName, result] of Object.entries(results)) {
        if (!result.error) {
            algorithmNames.push(algorithms[algoName]?.name || algoName);
            times.push(result.metadata.execution_time_ms);
            memories.push(result.metadata.memory_used_kb);
        }
    }
    
    // Gráfico de tiempo
    const timeCtx = document.getElementById('timeChart').getContext('2d');
    if (timeChart) {
        timeChart.destroy();
    }
    timeChart = new Chart(timeCtx, {
        type: 'bar',
        data: {
            labels: algorithmNames,
            datasets: [{
                label: 'Tiempo de Ejecución (ms)',
                data: times,
                backgroundColor: 'rgba(54, 162, 235, 0.6)'
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
    
    // Gráfico de memoria
    const memoryCtx = document.getElementById('memoryChart').getContext('2d');
    if (memoryChart) {
        memoryChart.destroy();
    }
    memoryChart = new Chart(memoryCtx, {
        type: 'bar',
        data: {
            labels: algorithmNames,
            datasets: [{
                label: 'Memoria Usada (KB)',
                data: memories,
                backgroundColor: 'rgba(255, 99, 132, 0.6)'
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
    const resultsCard = document.getElementById('compareResultsCard');
    const resultsContent = document.getElementById('compareResultsContent');
    resultsCard.style.display = 'block';
    resultsContent.innerHTML = `<div class="error-message">${message}</div>`;
}
