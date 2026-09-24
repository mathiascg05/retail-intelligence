# Bitácora de uso de IA

Usamos Claude (de Anthropic) para ayudarnos a programar y para discutir decisiones. Aquí anotamos qué le pedimos, qué propuso y qué hicimos con su propuesta.

La regla es simple: no aceptamos nada que no podamos explicar nosotros mismos.

---

## 22 de septiembre: arranque del proyecto

**Qué le pedimos:** que revisara los 6 archivos de datos, propusiera un plan hasta la semana 6 y armara la estructura del repositorio.

**Qué propuso:**
- Revisar cada tabla y cruzarlas entre sí: buscar códigos que no existen, precios que no cuadran y fechas imposibles.
- Usar Python con notebooks para el análisis y diapositivas para la presentación.
- Un repositorio privado, con los datos originales separados de los datos limpios.

**Qué hicimos:**
- **Aceptamos** la estructura del repositorio y que todos carguen los datos desde `src/carga.py`. Así las cifras no dependen de quién corrió el código.
- **Aceptamos** el calendario de 4 semanas. Lo armamos para la semana 6, que es la fecha que dio el profesor, no para la semana 15 del PDF.
- **Decidimos** no usar Power BI como entrega principal. Los gráficos salen de los notebooks, así se pueden regenerar si cambia algún dato.
- **Falta validar:** la revisión dice que no hay errores en montos ni márgenes. Alguien del equipo tiene que recalcular a mano unas cuantas filas para confirmarlo. Anotar aquí quién lo hizo y qué encontró.

---

## 22 de septiembre: cierre de A1

**Qué le pedimos:** comparar lo que teníamos con lo que pide el enunciado para A1, y proponer qué hacer con cada problema de los datos.

**Qué propuso:**
- Agregar tres cosas que el enunciado pide y no teníamos: las métricas de calidad de cada tabla, el diagrama de cómo se relacionan las tablas y la revisión de campañas enviadas después de la compra.
- Una solución para cada uno de los 7 problemas (ver `DECISIONES.md`).
- Comprobar las cifras del enunciado con los datos antes de usarlas.

**Qué hicimos:**
- **Aceptamos** comprobar las cifras del enunciado. Fue clave: dos de las tres no aparecen en los datos. El ticket promedio baja 1,9%, no 8%, y las devoluciones no suben. Esto cambia cómo empieza la presentación.
- **Aceptamos** no borrar filas y marcar los casos raros. Comprobamos que los datos limpios tienen las mismas filas que los originales.
- **Cambiamos de plan:** al principio íbamos a esperar al profesor para cerrar estas decisiones. Preferimos cerrarlas nosotros para no frenar A2, A3 y A4, y llevárselas ya justificadas. Si pide cambios, los umbrales están en un solo lugar de `carga.py`.
- **Aceptamos** usar la marca de conversión para comparar tasas y solo las conversiones confirmadas para calcular dinero. Si usáramos solo las confirmadas para todo, la conversión bajaría al 2% y ya no se podría comparar con lo que reporta la empresa.
- **Falta validar:** las reglas del segmento calculado (180 días, 8 compras, el 10% que más gasta) son criterio nuestro. Los 180 días salen de los datos: el 90% de los clientes vuelve a comprar en menos de 162 días.

---

## 24 de septiembre: revisión de los textos

**Qué le pedimos:** revisar que cada cifra de `DECISIONES.md` saliera realmente del notebook.

**Qué encontró:** tres afirmaciones que no eran exactas:
- Decía que las conversiones sin compra confirmada afectaban "por igual" a todas las campañas. No es así: van de 17% a 25% según el tipo.
- Decía que 255 clientes sin compras recibían campañas. En realidad son 242. El 255 era otra cifra (cuántos de ellos están marcados como "Inactivo").
- Decía que los montos fuera de lo normal eran "casi todos" de Electrónica. Son dos tercios.

**Qué hicimos:** **corregimos** las tres frases y agregamos al notebook los cálculos que faltaban, para que cada cifra del documento se pueda comprobar.
