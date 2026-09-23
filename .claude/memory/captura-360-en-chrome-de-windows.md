---
name: captura-360-en-chrome-de-windows
description: Chrome sin interfaz en Windows no baja de unos 500 px de ancho; para capturar a 360 px, meter la página en un iframe de 360
metadata:
  type: reference
---

En WSL no hay Chromium; se usa `/mnt/c/Program Files/Google/Chrome/Application/chrome.exe --headless=new --screenshot=… --window-size=…` con rutas de `wslpath -w`. En s5.7 (2026-09-23), `--window-size=360,…` maquetó la página a unos 500 px y recortó la captura a 360, y el contenido parecía desbordarse cuando no era así. Lo que funciona: una página contenedora con `<iframe src="pagina.html" style="width:360px;height:2600px;border:0">` y la ventana a 500 px.

Para las páginas con sesión: iniciar sesión con `curl` y un cookie jar, guardar el HTML y reescribir `/static/identidad/identidad.css` y las fotos a archivos locales del scratchpad. Al cargar datos de ejemplo con `curl`, el texto con acentos va con `--data-urlencode`, porque `-d` con bytes crudos guarda "dÃa". Ver [[pkill-f-mata-su-propio-comando]] para apagar `uvicorn` por PID.
