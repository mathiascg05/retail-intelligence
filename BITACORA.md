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
- **Aceptamos** comprobar las cifras del enunciado. Fue clave: ninguna coincide del todo. El ticket promedio baja 1,9%, no 8%; las devoluciones rondan el 14%, pero no suben; y la conversión cae a la mitad, pero desde 11%, no desde 22%. Esto cambia cómo empieza la presentación.
- **Aceptamos** no borrar filas y marcar los casos raros. Comprobamos que los datos limpios tienen las mismas filas que los originales.
- **Cambiamos de plan:** al principio íbamos a esperar al profesor para cerrar estas decisiones. Preferimos cerrarlas nosotros para no frenar A2, A3 y A4, y llevárselas ya justificadas. Si pide cambios, los umbrales están en un solo lugar de `carga.py`.
- **Aceptamos** usar la marca de conversión para comparar tasas y solo las conversiones confirmadas para calcular dinero. Si usáramos solo las confirmadas para todo, la conversión bajaría al 2% y ya no se podría comparar con lo que reporta la empresa.
- **Falta validar:** las reglas del segmento calculado (180 días, 8 compras, el 10% que más gasta) son criterio nuestro. Los 180 días salen de los datos: cuando un cliente vuelve a comprar, 9 de cada 10 veces lo hace en menos de 162 días.

---

## 22 de septiembre: modelo estrella y código de carga

**Qué le pedimos:** ayuda para estructurar el modelo estrella y para escribir las funciones que cargan y limpian los datos.

**Qué propuso para el modelo:**
- Poner las ventas como tabla central, con clientes, productos y fechas alrededor.
- Conectar las devoluciones con una venta concreta.
- Conectar las campañas y la atención al cliente solo con el cliente, porque los datos no traen ninguna columna que las una a una venta.
- Crear una tabla de fechas a partir de las fechas de las demás tablas, porque no viene en los archivos.
- Dibujar el diagrama en Mermaid (`docs/modelo.md`), que GitHub muestra directamente, y exportarlo como imagen para la presentación.

**Qué propuso para el código (`src/carga.py`):**
- `cargar_crudo()`: lee los 6 archivos tal como vienen, con las fechas ya convertidas.
- `cargar_limpio()`: aplica las 7 decisiones de `DECISIONES.md`. Agrega columnas que marcan los casos raros, calcula el margen de cada venta y el segmento calculado de cada cliente, y busca la compra que confirma cada conversión. Guarda el resultado en `data/clean/` para no recalcularlo cada vez.
- Los umbrales (30, 90 y 180 días, y 8 compras) como constantes al principio del archivo.

**Qué hicimos:**
- **Aceptamos** la estructura del modelo. En el notebook comprobamos las relaciones: cada venta tiene como máximo una devolución, y el cliente de cada devolución coincide siempre con el de la venta.
- **Aceptamos** el código de carga. Comprobamos que los datos limpios tienen las mismas filas que los originales, que los conteos de cada marca coinciden con los del notebook (711 ventas bajo costo, 392 clientes sin compras, 179 conversiones confirmadas) y que las columnas nuevas son las que lista `DECISIONES.md`.
- **Falta:** que cada integrante lea `src/carga.py` y pueda explicar qué hace cada paso. El profesor puede preguntarlo en la defensa.

---

## 24 de septiembre: revisión de los textos

**Qué le pedimos:** revisar que cada cifra de `DECISIONES.md` saliera realmente del notebook.

**Qué encontró:** tres afirmaciones que no eran exactas:
- Decía que las conversiones sin compra confirmada afectaban "por igual" a todas las campañas. No es así: van de 17% a 25% según el tipo.
- Decía que 255 clientes sin compras recibían campañas. En realidad son 242. El 255 era otra cifra (cuántos de ellos están marcados como "Inactivo").
- Decía que los montos fuera de lo normal eran "casi todos" de Electrónica. Son dos tercios.

**Qué hicimos:** **corregimos** las tres frases y agregamos al notebook los cálculos que faltaban, para que cada cifra del documento se pueda comprobar.

---

## 24 de septiembre: revisión de coherencia entre documentos

**Qué le pedimos:** comprobar que todos los documentos digan lo mismo y que cada cifra salga del notebook.

**Qué encontró:**
- Todas las cifras de los documentos aparecen en la salida del notebook, y la lista de columnas de `DECISIONES.md` coincide con la que genera `cargar_limpio()`.
- Una afirmación era falsa: decíamos que un cliente con más de 180 días sin comprar "lo normal es que ya no vuelva". Al medirlo, el 52% vuelve en los 180 días siguientes.
- La definición de "oportunidad" del notebook no coincidía con lo que calcula el código.
- La bitácora decía "el 90% de los clientes" cuando se trata del 90% de las veces que un cliente vuelve a comprar.
- Algunos textos decían que las cifras del enunciado "no aparecen" en los datos, cuando en devoluciones y conversión coinciden en parte.

**Qué hicimos:**
- **Corregimos** todo lo anterior y agregamos al notebook el cálculo del 52%.
- **Cambiamos** el significado del segmento "Inactivo" calculado: ahora es "en riesgo", no "perdido". Esto afecta a cómo se define el cliente perdido en A3.

---

## 25 de septiembre: A2, rentabilidad

**Qué le pedimos:** hacer A2 siguiendo el enunciado al pie de la letra y, donde el enunciado no dice cómo hacer algo, proponer un método y dejarlo anotado para confirmarlo con el profesor.

**Qué propuso:**
- Revisar los datos antes de decidir el método. Encontró que las devoluciones reembolsan el 100% de la venta, que los descuentos no parecen cambiar las unidades por compra y que la estacionalidad es débil.
- Tres opciones para el margen neto (el producto devuelto siempre se revende, nunca se revende, o depende del motivo) y dos para el CLV (horizonte fijo de 3 años o fórmula con tasa de descuento).
- Comprobar cada hallazgo con una prueba (intervalos de confianza, regresión, repetición entre años) para no presentar correlaciones como causas, que la rúbrica penaliza.

**Qué hicimos:**
- **Elegimos** el margen neto según el motivo: se revende salvo defectuoso o fraude. Nos pareció el supuesto más realista.
- **Elegimos** el CLV con horizonte de 3 años, sin tasa de descuento, porque en Venezuela justificar una tasa es muy discutible.
- **Ajustamos** el CLV para calcularlo por semestres en vez de por años. Con 2 años de datos solo hay un paso anual, y así no se puede ver si un segmento cae. La versión anual queda en el notebook como comprobación y da el mismo orden.
- **Aceptamos** usar el margen bruto como medida principal, porque es lo que pide el enunciado, y el neto como complemento.
- **Aceptamos** nombrar los picos y valles de cada categoría y canal (lo pide el enunciado) y además comprobar si se repiten. No se repiten.
- **Dejamos anotado** para el profesor todo lo que el enunciado no especifica (`FEEDBACK_PROFESOR.md`, semana 3).

**Errores que encontramos al revisar lo que generó la IA:**
- El primer cálculo del margen a precio de lista estaba mal planteado. Lo reescribimos como 1 − costo / (cantidad × precio de lista).
- El resumen decía que con más de 20% de descuento había que vender "el doble" para compensar. Con los números del notebook (207% de volumen extra) es el triple.
- Una frase mezclaba la tendencia de ventas de Electrónica con la de su margen. La separamos.

**Falta:** que Mikel Muñoz, responsable de A2, revise el notebook 02 y pueda explicar el CLV, el *bootstrap* y la regresión sin ayuda.

---

## 8 de octubre: A3, fugas de ingresos

**Qué le pedimos:** hacer A3 con el mismo criterio que A2: seguir el enunciado, comprobar cada hallazgo con una prueba y dejar anotado para el profesor todo lo que el enunciado no especifica.

**Qué propuso:**
- Llamar "anómala" a una tasa de devolución solo si sobrevive a la corrección por número de pruebas, y simular cuántas devoluciones por cliente serían normales antes de hablar de clientes "recurrentes".
- Medir el efecto de las quejas comparando el cambio en compras de las quejas sin resolver con el de las resueltas (antes y después de la queja), no solo el "después".
- No tratar como perdido a todo cliente con más de 180 días sin comprar, sino estimar su probabilidad de volver con una foto pasada de los datos, y probar esa estimación hacia atrás.

**Qué hicimos:**
- **Aceptamos** el plan de las cuatro partes y el umbral de 180 días de A1 para "en riesgo".
- **Aceptamos** dar las fugas por separado (clientes, devoluciones, quejas) y no solo un total.
- **Dejamos anotado** para el profesor todo lo que el enunciado no especifica (`DECISIONES.md`, A3.1 a A3.5, y `FEEDBACK_PROFESOR.md`).

**Errores y ajustes al revisar los resultados:**
- Comparando cada producto con la tasa global salían 51 productos "anómalos". Al compararlos con su propia categoría no quedó ninguno: eran el reflejo de Ropa y Electrónica. Cambiamos la referencia.
- La primera fórmula de ingresos perdidos (probabilidad de no volver × gasto semestral, con un modelo logístico) dio problemas: el modelo no convergía con el segmento "Inactivo", porque ninguno vuelve. La cambiamos por proporciones simples por segmento y tramo.
- La versión que multiplicaba el gasto por cuánto gastan los que vuelven fallaba un 19% en la prueba hacia atrás, y un 12% después de corregirla. Por eso la cifra principal usa el gasto que el cliente venía teniendo, y esa versión queda solo como tope del rango.
- Al cruzar el resumen con las salidas del notebook, una cifra del intervalo estaba mal copiada (153.684 en vez de 153.683) y otra mal redondeada. Las corregimos y ahora el notebook imprime todas las cifras del resumen.

**Lo que no esperábamos:** las quejas sin resolver no cambian las compras posteriores, aunque el enunciado lo sugiere. Lo presentamos tal cual, con el intervalo de confianza.

**Falta:** que Federico Celis, responsable de A3, revise el notebook 03 y pueda explicar la simulación de devoluciones, la diferencia en diferencias y la prueba hacia atrás sin ayuda.

---

## 8 de octubre: A4, efectividad del marketing

**Qué le pedimos:** hacer A4 con el mismo criterio que A2 y A3: seguir el enunciado, comprobar cada hallazgo con una prueba y anotar para el profesor lo que el enunciado no especifica.

**Qué propuso:**
- Comprobar primero cómo se repartió el descuento. Como no depende del segmento, del tipo, del canal ni del año, el efecto del descuento se puede leer como en un experimento.
- No quedarse con la marca de conversión: repetir el análisis con las compras reales del cliente en los 30 días antes y después de cada envío.
- Probar cada hipótesis sobre el segmento que no convierte (quejas, quejas sin resolver, devoluciones) con una regresión, en vez de solo comparar promedios.
- Dar el ROI de tres formas: el del enunciado (sobre ventas), sobre margen e incremental.

**Qué hicimos:**
- **Aceptamos** el análisis con compras reales. Es lo que más cambia la historia: el descuento dobla la conversión marcada, pero no cambia las compras.
- **Aceptamos** presentar ese resultado como limitación de los datos (no sabemos qué registra la marca de conversión), no como prueba de que el marketing no sirve.
- **Dejamos anotado** para el profesor todo lo que el enunciado no especifica (`DECISIONES.md`, A4.1 a A4.5, y `FEEDBACK_PROFESOR.md`).

**Errores y ajustes al revisar los resultados:**
- La devolución previa parecía bajar la conversión (odds ratio 0,71, muy significativa). Al tener en cuenta cuántas compras llevaba el cliente y la fecha del envío, el efecto desapareció. Habría sido una correlación presentada como causa.
- El ROI sobre ventas resultó ser casi una función del descuento medio, (1 − d) / d. Por eso agregamos el ROI sobre margen y el incremental.
- Tipo de campaña y canal resultaron ser lo mismo (cada tipo sale por un solo canal). Lo dejamos explicado en vez de presentarlos como dos hallazgos separados.

**Falta:** que Fernando Álvarez, responsable de A4, revise el notebook 04 y pueda explicar por qué el descuento se puede tratar como un experimento, la comparación con las compras reales y las tres versiones del ROI sin ayuda.
