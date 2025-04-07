# Idealista Scraper - Valencia

Este proyecto es un scraper en Python que extrae información de viviendas en venta en la ciudad de Valencia desde el portal de Idealista.

Utiliza Selenium y WebDriver Manager para automatizar la navegación por el sitio y recopilar datos como título, precio, número de habitaciones, metros cuadrados, planta, agencia comercializadora y si incluye garaje.

---

## ¿Qué hace este scraper?

- Recorre automáticamente las primeras 60 páginas de resultados de Idealista en Valencia.  
- Extrae datos de cada anuncio.  
- Los guarda en un archivo CSV.  
- Simula el comportamiento humano para evitar bloqueos.

---

## Autores

- Nuria Heredia Heredia
- Miguel Ángel Huet Muñóz

---

## Advertencia legal
Este scraper es solo con fines educativos. Idealista tiene términos de uso que pueden prohibir el web scraping automatizado. Úsalo bajo tu propia responsabilidad y respeta siempre la legalidad y los recursos del sitio web.

---

## Requisitos

Este scrapper necesita:

- Python 3.8 o superior  
- Google Chrome instalado 
- Las siguientes librerías de Python:

```bash
pip install selenium webdriver-manager pandas


