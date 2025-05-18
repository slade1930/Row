document.addEventListener('DOMContentLoaded', function() {
    // Configurar botones de ejemplo
    setupExampleButtons();
    
    // Configurar validación de matriz
    setupMatrixValidation();
});

// Función para configurar los botones de ejemplo
function setupExampleButtons() {
    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // Insertar matriz
            document.getElementById('id_matriz_a').value = this.getAttribute('data-matrix');
            
            // Insertar vector
            document.getElementById('id_vector_b').value = this.getAttribute('data-vector');
            
            // Mostrar mensaje de éxito
            showValidationMessage('Ejemplo cargado correctamente', 'success');
        });
    });
}

// Función para configurar la validación de matriz
function setupMatrixValidation() {
    const validateBtn = document.getElementById('validate-matrix');
    if (validateBtn) {
        validateBtn.addEventListener('click', validateMatrix);
    }
}

// Función para validar la matriz y vector
function validateMatrix() {
    const matrixInput = document.getElementById('id_matriz_a');
    const vectorInput = document.getElementById('id_vector_b');
    const validationPanel = document.getElementById('validation-result');
    
    try {
        // Validar formato JSON
        const matrix = JSON.parse(matrixInput.value);
        const vector = JSON.parse(vectorInput.value);
        
        // Validar que la matriz sea cuadrada
        const rows = matrix.length;
        if (rows === 0) {
            throw new Error('La matriz no puede estar vacía');
        }
        
        const cols = matrix[0].length;
        for (let i = 0; i < rows; i++) {
            if (matrix[i].length !== cols) {
                throw new Error('Todas las filas deben tener la misma cantidad de columnas');
            }
        }
        
        if (rows !== cols) {
            throw new Error('La matriz debe ser cuadrada (mismo número de filas que de columnas)');
        }
        
        // Validar que el vector tenga la dimensión correcta
        if (vector.length !== rows) {
            throw new Error(`El vector debe tener ${rows} elementos (uno por cada ecuación)`);
        }
        
        // Mostrar mensaje de éxito
        showValidationMessage('La matriz y vector son válidos', 'success');
        
    } catch (error) {
        // Mostrar mensaje de error
        showValidationMessage(`Error: ${error.message}`, 'error');
    }
}

// Función para mostrar mensajes de validación
function showValidationMessage(message, type) {
    const validationPanel = document.getElementById('validation-result');
    const validationMsg = document.getElementById('validation-message');
    
    validationPanel.classList.remove('hidden');
    
    if (type === 'success') {
        validationPanel.classList.remove('bg-red-50', 'text-red-800');
        validationPanel.classList.add('bg-green-50', 'text-green-800');
        validationMsg.innerHTML = `<i class="fas fa-check-circle mr-2"></i>${message}`;
    } else {
        validationPanel.classList.remove('bg-green-50', 'text-green-800');
        validationPanel.classList.add('bg-red-50', 'text-red-800');
        validationMsg.innerHTML = `<i class="fas fa-exclamation-circle mr-2"></i>${message}`;
    }
    
    // Desplazarse al panel de validación
    validationPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Opcional: Validación en tiempo real mientras se escribe
document.getElementById('id_matriz_a')?.addEventListener('input', function() {
    // Puedes agregar validación básica mientras se escribe
});

document.getElementById('id_vector_b')?.addEventListener('input', function() {
    // Puedes agregar validación básica mientras se escribe
});