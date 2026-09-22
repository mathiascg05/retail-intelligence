# Bitácora de uso de IA

Usamos Claude (Anthropic) como apoyo para programar y para discutir decisiones. Aquí anotamos qué le pedimos, qué propuso y qué hicimos con eso. La idea es que cualquiera del equipo pueda explicar el código y las cifras sin depender de la IA.

---

### 22-sep – Arranque del proyecto

**Qué pedimos:** le pasamos el enunciado y le pedimos una primera revisión de los 6 CSV, un plan hasta la semana 6 y la estructura del repo.

**Qué propuso:** un perfil de cada tabla y chequeos entre tablas (claves huérfanas, aritmética de precios, fechas), usar Python con notebooks para A1–A4 y diapositivas para A5, y un repo privado con los datos originales separados de los limpios.

**Qué hicimos:**
- *Aceptado:* la estructura del repo y que todos carguen los datos desde `src/carga.py`. Tiene sentido para que las cifras de A2–A5 no dependan de quién corrió qué.
- *Aceptado:* el calendario de 4 semanas (A1 → A2–A4 en paralelo → A5 → ensayos). Lo armamos sobre la semana 6 que dijo el profesor, no sobre la semana 15 del PDF.
- *Por validar (equipo):* los chequeos del notebook dan 0 errores en montos y márgenes. Falta que alguien recalcule a mano unas cuantas filas para confirmar que el 0 es real y no un filtro mal escrito. Anotar aquí quién lo hizo.
- *Decidido:* Power BI queda fuera como entregable principal. Los gráficos salen de los notebooks, así se pueden regenerar si cambia algún dato.

---

### 22-sep – Cierre de A1

**Qué pedimos:** revisar el repo contra el enunciado para ver qué faltaba en A1 y proponer qué hacer con cada problema de `DECISIONES.md`.

**Qué propuso:**
- Faltaban tres cosas que el enunciado pide explícitamente: las métricas de calidad por dataset (completitud, consistencia, unicidad, oportunidad), el modelo relacional y el chequeo de campañas con fechas posteriores a la compra.
- Una propuesta para cada una de las 7 decisiones (ver `DECISIONES.md`).
- Comprobar las cifras del enunciado con los datos antes de usarlas en el relato.

**Qué hicimos:**
- *Aceptado:* comprobar las cifras del enunciado. Resultó clave: dos de las tres no aparecen en los datos (el ticket cae 1,9%, no 8%; las devoluciones no suben). Cambia el inicio de la presentación.
- *Aceptado:* no borrar filas y marcar los casos raros con columnas. Comprobamos que `cargar_limpio` devuelve el mismo número de filas que los CSV.
- *Cambio de plan:* en la primera sesión habíamos quedado en esperar al profesor para cerrar las decisiones. Decidimos cerrarlas nosotros para no frenar A2–A4 y llevárselas ya justificadas; si pide cambios, los umbrales están en un solo lugar de `carga.py`.
- *Aceptado:* para las conversiones, usar `convertido` en las tasas y solo las respaldadas en los montos. Lo revisamos porque la alternativa (usar solo las respaldadas en todo) bajaría la conversión al 2% y dejaría de ser comparable con lo que reporta la empresa.
- *Pendiente de validar:* las reglas de `segmento_rfm` (180 días, 8 compras, top 10%) son criterio nuestro; el 180 sale del p90 del tiempo entre compras, que comprobamos en el notebook.
