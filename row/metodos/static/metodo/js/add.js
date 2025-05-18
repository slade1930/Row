// Mostrar/ocultar ejemplos
document.getElementById('show-examples').addEventListener('click', function() {
    const panel = document.getElementById('examples-panel');
    panel.classList.toggle('hidden');
    this.textContent = panel.classList.contains('hidden') ? 'Ver ejemplos' : 'Ocultar ejemplos';
});

// Insertar ejemplos
document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.getElementById('id_funcion').value = this.getAttribute('data-example');
    });
});

// Validación de función (simplificada)
document.getElementById('validate-function').addEventListener('click', function() {
    const funcInput = document.getElementById('id_funcion');
    const validationPanel = document.getElementById('validation-result');
    const validationMsg = document.getElementById('validation-message');
    
    if (funcInput.value.includes('x')) {
        validationPanel.classList.remove('hidden', 'bg-red-50', 'text-red-800');
        validationPanel.classList.add('bg-green-50', 'text-green-800');
        validationMsg.innerHTML = '<i class="fas fa-check-circle mr-1"></i> La función parece válida';
    } else {
        validationPanel.classList.remove('hidden', 'bg-green-50', 'text-green-800');
        validationPanel.classList.add('bg-red-50', 'text-red-800');
        validationMsg.innerHTML = '<i class="fas fa-exclamation-circle mr-1"></i> La función debe contener la variable x';
    }
});

// Validación en tiempo real del intervalo
document.getElementById('id_x0').addEventListener('input', checkInterval);
document.getElementById('id_x1').addEventListener('input', checkInterval);

function checkInterval() {
    const x0 = parseFloat(document.getElementById('id_x0').value);
    const x1 = parseFloat(document.getElementById('id_x1').value);
    
    if (!isNaN(x0) && !isNaN(x1)) {
        if (x0 >= x1) {
            // Mostrar advertencia
        }
    }
}