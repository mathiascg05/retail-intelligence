# Bitácora de uso de IA

Usamos Claude (de Anthropic) para ayudarnos a programar y para discutir decisiones. Aquí anotamos qué le pedimos, qué propuso y qué hicimos con su propuesta.

La regla es simple: no aceptamos nada que no podamos explicar nosotros mismos.

**Sobre los prompts:** hasta el 8 de octubre, "Qué le pedimos" es un resumen de lo que pedimos, no el texto exacto. Desde el 9 de octubre, el prompt va copiado tal cual.

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
- **Decidimos** no usar Power BI como entrega principal. Los gráficos salen de los notebooks, así se pueden regenerar si cambia algún dato. *(Nota del 9 de octubre: esto cambió. El 8 de octubre el profesor pidió un dashboard de Power BI y un informe escrito. Ver las entradas del 8 y el 9 de octubre.)*
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

---

## 8 de octubre: A5, recomendaciones y datos para Power BI

**Qué le pedimos:** cuantificar al menos tres recomendaciones en el formato del enunciado y preparar los datos para el dashboard de Power BI. El profesor pide un dashboard de Power BI y un informe escrito, así que no hicimos diapositivas.

**Qué propuso:**
- Cuatro recomendaciones, cada una apoyada en un hallazgo de A2–A4: bajar el descuento online, reducir el exceso de devoluciones de Ropa y Electrónica, una campaña de reactivación con grupo de control y un tope al descuento de las campañas.
- Dar cada una con su supuesto, un escenario central y un rango, en ingresos y en margen.
- Exportar el modelo estrella a CSV y guardar desde cada notebook las tablas de resultados, para que el dashboard muestre las mismas cifras que el informe. Y una guía (`docs/dashboard.md`) con las relaciones, las medidas DAX y las 10 visualizaciones.

**Qué hicimos:**
- **Aceptamos** las cuatro recomendaciones y ordenarlas por margen.
- **Aceptamos** guardar los CSV de Power BI en el repositorio, para que quien arme el dashboard no tenga que correr Python.
- **Dejamos fuera del dashboard** las quejas y el ROI por tipo de campaña (no muestran diferencias) para no pasar de 10 visualizaciones. Van en el informe.

**Errores y ajustes al revisar los resultados:**
- R4 se presentaba solo como ahorro. Al calcular los ingresos, con menos descuento hay menos conversiones y los ingresos registrados bajan (−21.737) aunque el margen suba (+7.197). Ahora se dan las dos cifras.
- La etiqueta de R1 redondeaba el tope a 5%; es 4,7%.
- Al agregar la exportación a los notebooks 02, 03 y 04 los volvimos a ejecutar y comprobamos que todas sus salidas siguen siendo idénticas.

**Falta:** armar el dashboard en Power BI siguiendo `docs/dashboard.md`, escribir el informe y que Leonardo Reyes, responsable de A5, pueda explicar de dónde sale cada cifra de las recomendaciones y de qué supuesto depende.

---

## 9 de octubre: revisión externa de todo el trabajo y correcciones

**Qué le pedimos:** antes de escribir el informe, pedimos a otra sesión de Claude (en claude.ai) una revisión crítica de A1–A5. Le dimos el PDF del enunciado, un resumen de todo lo hecho y acceso al repositorio. Este es el prompt, tal cual:

> Te adjunto dos archivos de un proyecto universitario de análisis de datos:
> 1. Proyecto_01_Retail_Intelligence.pdf: el enunciado del profesor, con la rúbrica.
> 2. REVISION_retail_intelligence.md: el resumen de todo lo que hizo mi equipo (fases A1 a A5), con decisiones, cifras y recomendaciones.
> (Si también ves el repositorio, el trabajo está en la rama a5-storytelling. Úsalo para comprobar que el resumen dice la verdad.)
>
> Antes de escribir el informe final, necesito una revisión crítica, no una confirmación. Actúa como el profesor más exigente posible, buscando por qué este trabajo no merece la nota máxima según la rúbrica.
>
> Revisa, en este orden:
> 1. Cobertura: compara punto por punto lo que pide el enunciado (A1–A5 y los 5 criterios de la rúbrica) con lo que hicimos. Señala lo que falta o está a medias.
> 2. Solidez: ¿qué conclusión no se sostiene con la evidencia descrita? ¿Dónde presentamos correlación como causalidad?
> 3. Coherencia: ¿hay contradicciones entre fases o cifras que no cuadran entre sí?
> 4. Decisiones: de las marcadas "A confirmar", ¿cuál cambiarías y por qué?
> 5. Relato: ¿funciona como historia (situación actual → hallazgos → recomendaciones) para una gerencia que no sabe estadística?
> 6. Los 11 puntos débiles de la sección 4 del resumen: para cada uno, dime si es grave, menor o no es problema, y qué harías.
> 7. Defensa oral: las 10 preguntas más difíciles que haría el profesor, y cuáles nos costaría responder.
>
> Reglas:
> - Ordena los problemas por impacto en la nota, del más grave al menos grave.
> - Si algo está bien, dilo en una línea y sigue.
> - No puedes recalcular las cifras: dalas por buenas, pero marca cualquiera que te parezca inverosímil o incoherente con otra.
> - Sé concreto: en vez de "falta profundidad", di qué análisis falta y cómo se haría.
> - Responde en español.

**Qué encontró (lo más grave):**
1. **El segmento del archivo es circular.** Es una franja del número de compras de los 24 meses (Inactivo 0–1, Premium 4–34). Lo usábamos para predecir la vuelta de los clientes y el CLV, así que "los Inactivo nunca vuelven" era una tautología.
2. **Las 179 conversiones "confirmadas" son coincidencias:** el 22,5% de las conversiones tiene una compra en 30 días, casi igual que cualquier envío.
3. **El margen no cae** (24,7% → 24,9%) y no lo decíamos. El relato no explicaba "por qué".
4. Sumábamos todos los reembolsos como "ingresos perdidos", lo que contradecía A2.1.
5. R1 era casi todo el beneficio y se apoyaba en una prueba débil. R2 suponía una causa en Electrónica que los datos no muestran. R3 anualizaba mal.
6. Faltaban: atípicos en todos los campos, las 158 devoluciones del 31-dic y decir "no detectable" en vez de "no hay efecto".

**Cómo lo comprobamos:** antes de cambiar nada, recalculamos cada afirmación marcada como comprobada sobre nuestros datos:
- los rangos de compras por segmento;
- el margen por año;
- las 158 devoluciones del 31-dic;
- la tasa de las coincidencias (22,5% contra 20,3%);
- la permutación del descuento;
- la recompra a 90 días.

Todas se confirmaron. *(Nota de la ronda 2: las cifras se confirmaron, pero una de esas comprobaciones, la recompra a 90 días, controlaba por el segmento del archivo, que es circular. Ver la entrada de la ronda 2.)*

**Qué hicimos:**
- **Aceptamos** casi todo. Los cambios están en `DECISIONES.md` (A1.1, A1.4, A1.8, A2.1–A2.5, A3.3–A3.5, A4.3–A4.5 y A5.1–A5.5).
- **Ajustamos** la estimación de la vuelta de los clientes. La revisión proponía estimarla con datos conocidos en la fecha de corte. Lo hicimos, pero esa versión predice peor en la prueba hacia atrás: 49% previsto contra 41% real. La causa es que el archivo tiene clientes fijos y los de una sola compra son cada vez más los que no vuelven. No lo escondimos: damos la versión tal cual y una calibrada con ese error. También probamos una regresión logística con el ritmo de compra y la antigüedad, y no mejoró. La descartamos por ser más difícil de explicar sin ganar nada.
- **Ajustamos** la lectura de las devoluciones. La revisión decía que por fecha de devolución el último trimestre sube a 15,8%. Comprobamos que esa subida se debe solo a las 158 devoluciones fechadas el 31-dic (sin ellas, 13,3%). Así que "no hubo subida" se mantiene, midiendo por fecha de compra.
- **Ajustamos** la fecha de registro. La revisión decía que el registro es casi uniforme. Hay un pico en el último trimestre de 2024 (1.538 altas), pero la conclusión es la misma: no es un alta en un sistema nuevo y no la usamos.
- **Ajustamos** la recomendación para Electrónica. En vez de crear una recomendación aparte, sumamos a R1 que ninguna venta quede bajo costo (+5.093 al año). Casi la mitad del beneficio de R1 viene de Electrónica.
- **Rechazamos** cambiar el ticket con el que R4 valora las conversiones. La revisión decía que usa el ticket de las 179 coincidencias, pero ese ticket (355) es casi el de cualquier compra (344), así que el resultado no cambia.

**Cómo cambiaron las cifras principales:**

| Cifra | Antes | Ahora |
|---|---|---|
| Fugas a 6 meses | 1.011.458 (todo sumado) | 372.680 evitables (350.773 a 446.562); reembolsos aparte |
| Segmento de mayor valor en riesgo | Esporádico, 169.772 | Esporádico, 148.811 (solo clientes recurrentes) |
| Recomendaciones (margen central) | 237.544 al año, 11% | 163.329, 7,6% (R1 es el 89%) |
| CLV en el dashboard | Premium 13 veces Esporádico (segmento circular) | Quien compra 4–6 veces por semestre, 13 veces quien compra una (grupos conocidos de antemano) |

**Falta, y lo tiene que hacer el equipo (no la IA):**
- Revisar estos cambios en los PR de cada fase.
- Cerrar los "Falta validar" del 22 de septiembre: recalcular a mano unas filas de montos y márgenes y anotar quién lo hizo.
- Que cada responsable pueda explicar sin ayuda los métodos de su fase. Para eso está `docs/metodos.md`.

---

## 9 de octubre: segunda revisión externa

**Qué le pedimos:** a la misma sesión de Claude en claude.ai, que comprobara en el repositorio si las correcciones de la primera ronda estaban bien hechas y buscara problemas nuevos. Le dimos un resumen de lo corregido, de dónde no le hicimos caso y por qué. Este es el prompt, tal cual:

> Segunda ronda de revisión del mismo proyecto. Te adjunto:
> 1. Proyecto_01_Retail_Intelligence.pdf: el enunciado con la rúbrica.
> 2. REVISION_retail_v2.md: qué corregimos tras tu revisión anterior, dónde no te hicimos caso (y por qué) y las cifras actuales.
> El repositorio actualizado está en la rama a5-storytelling (mathiascg05/retail-intelligence). Úsalo para comprobar lo que dice el resumen.
>
> Sigue actuando como el profesor más exigente posible. Esta vez quiero:
> 1. Verificación: para cada corrección de la sección 1 del resumen, dime si quedó bien resuelta, a medias o mal. Compruébalo en el repo (notebooks, DECISIONES.md, docs/dashboard.md), no solo en el resumen.
> 2. Desacuerdos: en los puntos de la sección 2 donde no seguimos tu recomendación, ¿nuestro argumento se sostiene?
> 3. Problemas nuevos: ¿las correcciones introdujeron errores, incoherencias entre fases o cifras que no cuadran?
> 4. Nuestras dudas (sección 4): respóndelas una por una.
> 5. Lo que falta para la nota máxima en cada criterio de la rúbrica, pensando ya en el entregable final: informe escrito + dashboard de Power BI de 10 visuales + defensa oral.
>
> Reglas:
> - Ordena todo por impacto en la nota, del más grave al menos grave.
> - Si algo está bien, dilo en una línea y sigue.
> - Sé concreto: qué cambiar, dónde y cómo.
> - Si algo te parece ya suficiente, dilo: no busques problemas donde no los hay.
> - Responde en español.

**Qué encontró (lo más importante):**
1. **La recompra a 90 días que nos sugirió en la primera ronda controlaba por el segmento del archivo,** justo la circularidad que nos había criticado. La conclusión aguanta, pero la cifra estaba mal planteada.
2. **El descuento no es aleatorio entre clientes:** los Premium reciben menos.
3. **La estimación de la vuelta de los clientes podía mejorar** contando las compras de los últimos 12 meses en vez de todas.
4. **La calibración usaba el factor de todos los clientes**, cuando la cifra principal solo incluye a los recurrentes.
5. **Llamábamos "evitable" a un exceso de devoluciones sin causa conocida.**
6. **El dashboard tenía 15 gráficos, no 10.**
7. **Faltaba una tabla que uniera las pérdidas con las recomendaciones.**

**Cómo lo comprobamos:** recalculamos sobre nuestros datos cada cifra que nos dio:
- la recompra comparando a cada cliente consigo mismo (+0,0 puntos; online +1,0);
- el descuento por segmento y canal (Premium 6,3% online contra 8,1–8,4%);
- la prueba hacia atrás con 12 meses (45% previsto contra 41% real);
- el factor de calibración con los recurrentes.

Todo se confirmó.

**Qué hicimos:**
- **Aceptamos y rechazamos nuestra propia versión anterior** de la recompra. Usamos la comparación de cada cliente consigo mismo, que no depende del segmento. Fue un error nuestro haber aceptado sin más el control por segmento en la primera ronda: lo habíamos marcado como "confirmado" porque la cifra salía igual, sin revisar el método.
- **Aceptamos** la ventana de 12 meses y calibrar solo con los recurrentes. Al hacerlo, la calibración cambió de dirección: con los recurrentes la estimación se queda corta (49% previsto, 56% real), así que la versión calibrada da menos fuga que la sin calibrar (232.487 contra 264.897).
- **Aceptamos:**
  - cambiar "evitables" por "fugas identificadas" y "por encima de lo normal";
  - dejar el dashboard en 10 objetos (gráficos combinados y un índice);
  - la tabla de pérdidas (A5.6);
  - la sensibilidad de R1;
  - no sumar R3 (6 meses) con las cifras anuales;
  - los títulos 5 y 10;
  - unificar el modelo con Power BI y regenerar el diagrama.
- **No hicimos** dos cosas que pedía:
  - "Pegar los prompts reales de cada entrada": las entradas anteriores quedan como resumen, con una nota que lo dice. No las reescribimos después.
  - "Cerrar los 'Falta' con nombre": eso solo lo puede hacer una persona del equipo. Dejamos preparada la hoja `docs/validacion_manual.md`.

**Errores nuestros al aplicar los cambios, y cómo los encontramos:**
- **El promedio para el grupo "ninguna compra en 12 meses".** Ese grupo no existe en la foto de 2023, y el primer cálculo usó un promedio sin ponderar. Daba un 68% de vuelta, inflado por los grupos pequeños que vuelven casi siempre. Lo vimos porque la prueba hacia atrás salía peor que antes (53%). Con el promedio ponderado por clientes, 45%.
- **El peor caso de la recompra para R1.** Al principio usamos la cota baja del intervalo, cuando bajar el descuento es peligroso si el descuento ayuda, es decir, en la cota alta. Corregido: en el peor caso se perdería un 1,2% de las recompras.

**Cómo cambiaron las cifras principales:**

| Cifra | Ronda 1 | Ronda 2 |
|---|---|---|
| Prueba hacia atrás de la vuelta | 49% previsto, 41% real | 45% previsto, 41% real |
| Fugas a 6 meses (cifra principal) | 372.680 | 417.569 (397.117 a 470.712) |
| Fuga de Esporádicos recurrentes | 148.811 | 172.819 |
| Recompra según el descuento | +0,2 (control por segmento) | +0,0 (cada cliente consigo mismo) |
| Margen de las recomendaciones | 163.329 (sumando R3) | 158.657 al año + 5.790 de R3 en 6 meses |

**Falta, y lo tiene que hacer el equipo:**
- Completar `docs/validacion_manual.md` y anotar aquí quién lo hizo.
- Que cada responsable repase `docs/metodos.md` para su fase.
- Revisar los cambios en los PR.

