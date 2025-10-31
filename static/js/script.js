function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('collapsed');
}




document.addEventListener('DOMContentLoaded', () => {

    let openMenus = [];

    try {
        const storedMenus = localStorage.getItem('openSubmenus');
        if (storedMenus) {
        openMenus = JSON.parse(storedMenus);
        }
    } catch (e) {
        console.warn('Error leyendo openSubmenus de localStorage:', e);
        localStorage.removeItem('openSubmenus');  // Lo limpio para evitar futuros errores
    }

    // Restaurar submenús abiertos
    openMenus.forEach(menuId => {
        const submenu = document.getElementById(menuId);
        if (submenu) {
        submenu.classList.add('show');
        const trigger = document.querySelector(`[href="#${menuId}"]`);
        if (trigger) {
            trigger.setAttribute('aria-expanded', 'true');
        }
        }
    });

    // Escuchar clics para guardar el estado
    document.querySelectorAll('[data-bs-toggle="collapse"]').forEach(toggle => {
        toggle.addEventListener('click', function () {
        const menuId = this.getAttribute('href').replace('#', '');
        const index = openMenus.indexOf(menuId);

        if (index > -1) {
            openMenus.splice(index, 1); // Cerrar
        } else {
            openMenus.push(menuId); // Abrir
        }

        localStorage.setItem('openSubmenus', JSON.stringify(openMenus));
        });
    });
});



function graficarCanvas(datosGraficoTipo, datosGraficoDestino) {

    // Logica para los graficos estadisticos
    // Paso 1: Obtener los datos JSON que Django nos envió
    // const datosGraficoTipo = JSON.parse('{{ datos_grafico_tipo_json|escapejs }}');
    // const datosGraficoDestino = JSON.parse('{{ datos_grafico_destino_json|escapejs }}');

    // Función para crear un gráfico de dona. Ahora siempre compara contra un total.
    function createDoughnutChart(canvasId, mainLabel, dataValue, backgroundColor, borderColor, totalCompareValue) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        // El "resto" ahora siempre será el total de comparación menos el valor principal
        const remainingValue = totalCompareValue - dataValue;


        // Plugin para ver los numeros estadisticos
        const centerLabelPlugin = {
            id: 'centerLabel',
            beforeDraw(chart) {
                const { width, height, ctx } = chart;
                const dataset = chart.data.datasets[0];
                const value = dataset.data[0];

                ctx.save();
                ctx.font = 'bold 22px sans-serif';
                ctx.fillStyle = '#333';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';

                // centrado perfecto en canvas
                ctx.fillText(value, width / 2, height / 2);
                ctx.restore();
            }
        };



        new Chart(ctx, {
            type: 'doughnut',
            data: {
                // Las etiquetas serán el nombre del segmento principal y 'Resto'
                labels: [mainLabel, 'Resto'],
                datasets: [{
                    label: 'Cantidad',
                    data: [dataValue, remainingValue], // Aquí se calcula el resto
                    backgroundColor: [backgroundColor, 'rgba(200, 200, 200, 0.98)'], // Color para el valor y un gris para el resto
                    borderColor: [borderColor, 'rgba(158, 158, 158, 1)'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: false }, // El título ya está en el H2
                    legend: {
                        display: true,
                        position: 'bottom' // Posición de la leyenda
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                let label = tooltipItem.label || '';
                                if (label === 'Resto') { // Si es el segmento "Resto"
                                    return `Resto: ${tooltipItem.raw}`;
                                }
                                // Si es el segmento principal
                                const value = tooltipItem.raw;
                                const total = totalCompareValue; // Usamos el total de comparación
                                const percentage = total > 0 ? ((value / total) * 100).toFixed(2) : 0;
                                return `${mainLabel}: ${value} (${percentage}%)`; // Texto como "Equipos Nuevos: 2 (20.00%)"
                            }
                        }
                    }
                }
            },
            plugins: [centerLabelPlugin]
        });
    }


    // --- GRÁFICOS DEL PRIMER GRUPO (Tipo/Estado General) ---
    // Todos estos se comparan contra 'datosGraficoTipo.total_activas'
    const totalOrdenesActivas = datosGraficoTipo.total_activas; // Guardamos en una variable para mayor claridad

    // Gráfico 1: Total de Órdenes Activas
    createDoughnutChart(
        'totalOrdenesActivasChart',
        'Total Activas', // Etiqueta principal
        totalOrdenesActivas, // Valor del segmento principal
        'rgba(247, 57, 57, 0.8)',
        'rgba(177, 30, 30, 1)',
        totalOrdenesActivas // El total de comparación es el mismo valor para este gráfico
    );

    // Gráfico 2: Órdenes Pendientes de Revisión Activas
    createDoughnutChart(
        'pendientesRevisionActivasChart',
        'Pendientes',
        datosGraficoTipo.pendientes_revision_activas,
        'rgba(20, 88, 198, 0.84)',
        'rgba(6, 56, 255, 0.91)',
        totalOrdenesActivas // El total de comparación es el total de órdenes activas
    );

    // Gráfico 3: Órdenes Revisadas/Palletizadas Activas
    createDoughnutChart(
        'revisadasPalletizadasActivasChart',
        'Revisados',
        datosGraficoTipo.revisadas_activas,
        'rgba(12, 161, 25, 0.9)',
        'rgba(16, 76, 20, 1)',
        totalOrdenesActivas // El total de comparación es el total de órdenes activas
    );

    // --- GRÁFICOS DEL SEGUNDO GRUPO (Por Destino) ---
    // Ahora, estos también se comparan contra 'totalOrdenesActivas'
    // Asegúrate de que 'totalOrdenesActivas' está definida antes de usarse aquí.

    createDoughnutChart(
        'destinoNuevoActivasChart',
        'Nuevos', // Etiqueta más descriptiva
        datosGraficoDestino.destino_nuevo_activas,
        'rgba(255, 208, 0, 0.95)',
        'rgba(255, 183, 0, 1)',
        totalOrdenesActivas // ¡Aquí está el cambio clave! Se compara con el total de órdenes activas.
    );

    createDoughnutChart(
        'destinoAveriaActivasChart',
        'Avería',
        datosGraficoDestino.destino_averia_activas,
        'rgba(247, 57, 57, 0.8)',
        'rgba(177, 30, 30, 1)',
        totalOrdenesActivas // ¡Aquí está el cambio clave!
    );

    createDoughnutChart(
        'destinoDestruccionActivasChart',
        'Destrucción',
        datosGraficoDestino.destino_destruccion_activas,
        'rgba(20, 88, 198, 0.84)',
        'rgba(6, 56, 255, 0.91)',
        totalOrdenesActivas // ¡Aquí está el cambio clave!
    );

}