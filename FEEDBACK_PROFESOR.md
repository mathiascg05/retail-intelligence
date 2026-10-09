# Reuniones con el profesor

## Semana 2

**Qué le vamos a preguntar:**
- ¿Hay que entregar el código o solo la presentación?
- Las cifras del enunciado (ticket −8%, devoluciones al 14%, conversión de 22% a 11%) coinciden con los datos solo en parte. ¿Es a propósito? ¿Nos basamos en los datos?
- ¿Está de acuerdo con nuestras decisiones de limpieza (`DECISIONES.md`)? Sobre todo la 1 (fecha de registro) y la 2 (conversiones sin compra).

**Qué respondió:**

## Semana 3

**Qué le vamos a pedir que confirme (A2):** el enunciado no dice cómo hacer estas cosas, así que las hicimos así por ahora (detalle en `DECISIONES.md`, A2):
- **Margen neto (A2.1):** una venta devuelta se revende, salvo que el motivo sea producto defectuoso o fraude; en ese caso se pierde también el costo.
- **CLV (A2.2):** margen neto por semestre × (1 + r + … + r⁵), con r = retención semestral. Horizonte de 3 años, sin tasa de descuento.
- **Declive (A2.3):** un segmento está en declive si su CLV baja de 2023 a 2024 y el intervalo de confianza de la caída no incluye el 0. Usamos el segmento que trae el archivo.
- **Estacionalidad (A2.4):** además de nombrar picos y valles, comprobamos si se repiten entre años. Resultado: no se repiten. ¿Le parece suficiente decir que no hay estacionalidad?

**Qué le vamos a pedir que confirme (A3):** lo hicimos así por ahora (detalle en `DECISIONES.md`, A3):
- **Tasas anómalas (A3.1):** prueba binomial con corrección por número de pruebas; cada producto se compara con su categoría. Resultado: solo Ropa y Calzado y Electrónica se salen de lo normal.
- **Clientes recurrentes (A3.2):** comparamos con una simulación de lo que daría el azar. Resultado: no hay devolvedores habituales.
- **Quejas (A3.3):** compras 90 días antes y después, sin resolver contra resueltas. Resultado: no se detecta efecto (como mucho, 19.159 a 6 meses). ¿Le parece suficiente para decir que las quejas sin resolver no espantan clientes en estos datos?
- **En riesgo (A3.4):** más de 180 días sin comprar. La probabilidad de volver se estima con una foto pasada, agrupando solo con datos de esa fecha (compras y días sin comprar), no con el segmento del archivo, que se definió con datos posteriores. En la prueba hacia atrás la estimación se pasa (49% previsto, 41% real), así que damos también una versión calibrada.
- **Ingresos perdidos (A3.5):** cifra principal = clientes recurrentes que no vuelven + exceso de devoluciones de Ropa y Electrónica (372.680 a 6 meses). Los reembolsos totales (645.361) van aparte como costo estructural, y los clientes de una sola compra no cuentan como fuga. ¿Le parece bien así, o "ingresos perdidos" debe incluir todos los reembolsos?

**Qué le vamos a pedir que confirme (A4):** detalle en `DECISIONES.md`, A4:
- **Descuento (A4.2):** el descuento se repartió como en un sorteo (no depende del segmento, del tipo, del canal ni del año). ¿Podemos leer su efecto como causal?
- **Conversión contra compras reales (A4.3):** según la marca, el descuento dobla la conversión; según las transacciones, ni las campañas ni el descuento cambian las compras. ¿La conversión puede venir de compras que no están en `transacciones.csv`? ¿Cuál de las dos lecturas presentamos? (Las 179 compras "confirmadas" resultan ser coincidencias: cualquier envío tiene una compra en 30 días el 21% de las veces.)
- **ROI (A4.5):** damos tres versiones (sobre ventas, la del enunciado; sobre margen; e incremental). ¿Cuál presentamos como principal?

**Qué le vamos a pedir que confirme (A5):**
- **Recomendaciones (A5.1):** cada una con su supuesto, un escenario central y un rango, en ingresos y margen. ¿Le parece bien dar rangos como "impacto esperado"?
- **Informe:** ¿qué extensión y estructura espera? ¿El dashboard de Power BI se entrega como archivo .pbix?

**Qué respondió:**

## Semana 4

**Qué le vamos a mostrar:** las cifras principales de A2, A3 y A4, y la lista de gráficos con sus títulos.

**Qué respondió:**

## Semana 5

**Qué le vamos a mostrar:** un ensayo corto de la presentación. Le pedimos las preguntas que haría en la defensa.

**Qué respondió:**
