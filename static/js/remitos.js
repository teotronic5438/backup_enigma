    document.addEventListener('DOMContentLoaded', function() {
        const productosTableEl = document.getElementById('productosTable');
        if (!productosTableEl) return;  // Sale si no existe (no estamos en nuevo remito)
        
        const addRowBtn = document.getElementById('addRow');
        const productosTable = document.getElementById('productosTable').getElementsByTagName('tbody')[0];
        const totalForms = document.getElementById('id_remitoproducto_set-TOTAL_FORMS');

        addRowBtn.addEventListener('click', function() {
            const formCount = parseInt(totalForms.value);
            const lastRow = document.querySelector('.producto-form:last-child');
            const newRow = lastRow.cloneNode(true);

            // Actualiza todos los inputs/selects de la fila
            newRow.querySelectorAll('input, select').forEach(function(el) {
                // Actualizar el índice
                if (el.name) {
                    el.name = el.name.replace(/-\d+-/, `-${formCount}-`);
                    el.id = el.id.replace(/-\d+-/, `-${formCount}-`);

                    // Limpiar valores de campos
                    if (el.type === 'text' || el.type === 'number') {
                        el.value = '';
                    }

                    // Desmarcar checkbox DELETE
                    if (el.type === 'checkbox') {
                        el.checked = false;
                    }

                    // Reiniciar select
                    if (el.tagName.toLowerCase() === 'select') {
                        el.selectedIndex = 0;
                    }
                }
            });

            productosTable.appendChild(newRow);
            totalForms.value = formCount + 1;

            // Reagregar evento al nuevo botón eliminar
            addRemoveListener(newRow.querySelector('.remove-row'));
        });

        function addRemoveListener(btn) {
            btn.addEventListener('click', function() {
                const row = btn.closest('tr');
                const checkbox = row.querySelector('input[type="checkbox"][name$="DELETE"]');

                if (checkbox) {
                    // Si el formulario ya existe en la BD, marcarlo para eliminar
                    checkbox.checked = true;
                    row.style.display = 'none';
                } else {
                    // Si es un formulario nuevo (sin ID), se puede eliminar del DOM
                    row.remove();

                    // Recalcular totalForms
                    const currentForms = document.querySelectorAll('.producto-form').length;
                    totalForms.value = currentForms;

                    // Reindexar
                    document.querySelectorAll('.producto-form').forEach((row, index) => {
                        row.querySelectorAll('input, select').forEach(input => {
                            if (input.name) {
                                input.name = input.name.replace(/-\d+-/, `-${index}-`);
                                input.id = input.id.replace(/-\d+-/, `-${index}-`);
                            }
                        });
                    });
                }
            });
        }

        // Agregar evento a los botones "Eliminar" existentes
        document.querySelectorAll('.remove-row').forEach(btn => addRemoveListener(btn));
    });