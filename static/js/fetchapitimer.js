function fetchTickerData() {
    fetch('https://dolarapi.com/v1/dolares')
        .then(response => response.json())
        .then(data => {
            const ticker = document.getElementById('ticker-api');

            // Verifico que los datos existan y sean un array
            if (data && Array.isArray(data)) {

                // Convierto cada item del array en un string HTML
                const items = data.map(item => {
                    return `<span class="ticker-item">
                                ${item.nombre}: Compra $${item.compra} / Venta $${item.venta}
                            </span>`;
                }).join('');

                // duplicamos el contenido para loop continuo
                ticker.innerHTML = items + items;

                // calcular velocidad dinámica
                const tickerContainer = ticker.parentElement;
                const contentWidth = ticker.scrollWidth / 2; // solo la mitad real
                const containerWidth = tickerContainer.offsetWidth;

                const duration = (contentWidth + containerWidth) / 50; // px/segundo
                ticker.style.animation = `scrollTicker ${duration}s linear infinite`;
            } else {
                ticker.innerHTML = 'Sin información disponible';
            }
        })
        .catch(error => {
            const ticker = document.getElementById('ticker-api');
            ticker.innerHTML = 'Error cargando info';
            console.error('Error API:', error);
        });
}

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', fetchTickerData);

// Actualizar cada 5 minutos (300000 ms)
setInterval(fetchTickerData, 300000);

