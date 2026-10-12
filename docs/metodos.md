# Los métodos, explicados para la defensa

La rúbrica evalúa que **todos** puedan responder preguntas técnicas sin mirar las diapositivas. Aquí está cada método que usamos, con tres cosas:
- qué pregunta responde;
- qué pasaría si no lo usáramos;
- un ejemplo con nuestras cifras.

Si te preguntan por un método, la respuesta corta es la primera línea de su apartado.

---

## Regla del rango intercuartílico (IQR), para encontrar valores raros

**En una frase:** un valor es raro si está muy por encima o muy por debajo de la mitad central de los datos.

- **Cómo funciona:** se toma el valor que deja abajo al 25% de los datos (Q1) y el que deja abajo al 75% (Q3). La distancia entre ellos es el IQR. Es raro todo lo que esté a más de 1,5 IQR por fuera de ese rango.
- **Sin él:** tendríamos que elegir un límite a ojo ("más de 1.000 es raro"), y cambiaría según quién mire.
- **Ejemplo:** con todas las ventas juntas salen 4.138 montos raros, dos tercios de Electrónica, solo porque sus productos son caros. Por eso lo aplicamos dentro de cada categoría: 3.420 (A1.7).

## Intervalo de confianza del 95%

**En una frase:** el rango en el que probablemente está el valor real, teniendo en cuenta que trabajamos con una muestra.

- **Sin él:** no sabríamos si una diferencia es real o casualidad.
- **Ejemplo:** Ropa devuelve el 21,8% (IC 95%: 20,9% a 22,7%). El resto devuelve alrededor del 10%. Los intervalos no se tocan, así que la diferencia es real (A3.1).
- **Wilson:** es la forma de calcular el intervalo para porcentajes que funciona bien aunque el porcentaje sea pequeño.

## Bootstrap (remuestreo)

**En una frase:** para saber cuánto podría variar una cifra, la recalculamos 1.000 veces con muestras sacadas al azar de nuestros propios datos.

- **Cómo funciona:** se sacan clientes al azar, con reposición, hasta tener tantos como en los datos. Se calcula la cifra y se repite 1.000 veces. El 95% central de esos resultados es el intervalo de confianza.
- **Sin él:** el CLV o la fuga de clientes no tienen una fórmula sencilla para su intervalo; daríamos un número sin saber cuánto puede variar.
- **Ejemplo:** el CLV de los Frecuentes cambió +0,7% de 2023 a 2024, con un IC de −10% a +12%. Como incluye el 0, no podemos decir que haya caído (A2.3).

## Prueba binomial con corrección de Benjamini-Hochberg

**En una frase:** comprobar si la tasa de devolución de un producto se aleja de lo normal sin que nos engañen las casualidades de probar muchos productos a la vez.

- **Prueba binomial:** ¿es normal que un producto con 150 ventas tenga 40 devoluciones si su categoría devuelve el 21,8%? Da un valor p: la probabilidad de ver algo así por azar.
- **El problema:** con 318 productos y un límite de p < 0,05, unos 16 saldrían "anómalos" por pura suerte.
- **Benjamini-Hochberg:** ajusta el límite según cuántas pruebas se hacen, para que casi ninguno de los "anómalos" sea un falso positivo.
- **Ejemplo:** comparando con la media global salían 51 productos anómalos, pero eran solo reflejo de su categoría. Comparando con su propia categoría y corrigiendo, ninguno (A3.1).

## Simulación (para los "devolvedores habituales")

**En una frase:** comparar lo que vemos con lo que daría el azar.

- **Cómo funciona:** simulamos 1.000 veces las devoluciones de cada cliente, con sus compras reales y la tasa de su categoría.
- **Sin ella:** el que más compra parecería "devolvedor" solo por comprar mucho.
- **Ejemplo:** 793 clientes tienen 3 o más devoluciones; el azar da 785. No hay devolvedores habituales (A3.2).

## Diferencia en diferencias (quejas sin resolver)

**En una frase:** comparar el **cambio** de un grupo con el **cambio** de otro, para descontar lo que le pasa a todos.

- **Cómo funciona:** tras una queja sin resolver, el cliente pasa de 0,98 a 0,92 compras en 90 días (−0,06). Pero tras una queja resuelta también baja, de 0,97 a 0,95 (−0,02). El efecto de no resolver es la diferencia entre los dos cambios: −0,03.
- **Sin ella:** atribuiríamos a la queja sin resolver una caída que en parte es normal.
- **Resultado:** IC de −0,21 a +0,13. Incluye el 0: no se detecta efecto. Pero el peor caso compatible con los datos costaría como mucho 19.159 en 6 meses (A3.3).

## Kruskal-Wallis (estacionalidad)

**En una frase:** comprobar si algún mes vende distinto a los demás.

- **Cómo funciona:** es la versión de "comparar varios grupos" que no necesita que los datos tengan forma de campana. Si p es mayor que 0,05, no hay evidencia de que algún mes sea distinto.
- **Sin ella:** cualquier serie de 24 meses tiene un mes más alto y uno más bajo; diríamos "marzo es el pico" aunque sea casualidad.
- **Ejemplo:** p = 0,63 para las ventas diarias por mes. Además, el patrón de 2023 no se repite en 2024. Con solo dos años, la conclusión es "no hay estacionalidad marcada" (A2.4).

## Regresión con efectos fijos (descuentos)

**En una frase:** medir el efecto del descuento dejando fijas las otras cosas que también cambian las ventas.

- **Cómo funciona:** se estima cuánto cambian las unidades por compra cuando sube el descuento, comparando solo ventas de la misma categoría, el mismo canal y el mismo segmento.
- **Sin ella:** si online da más descuento y además vende distinto, confundiríamos el efecto del canal con el del descuento.
- **Ejemplo:** +10 puntos de descuento → +0,004 unidades (IC: −0,012 a +0,020). Es decir, nada (A2.5).

## Comparar a cada cliente consigo mismo (recompra)

**En una frase:** para saber si el descuento hace volver al cliente, comparamos las compras de **un mismo cliente** con más y con menos descuento.

- **Sin ella:** comparando clientes distintos, más descuento parece *bajar* la recompra (−2,5 puntos por cada 10). Pero es mezcla: los que más compran (Premium) reciben menos descuento. Controlar por el segmento del archivo tampoco sirve, porque el segmento es circular.
- **Ejemplo:** cada cliente contra sí mismo, +0,0 puntos de recompra por cada 10 de descuento (IC: −0,6 a +0,7); solo online, +1,0 (IC: −0,2 a +2,1) (A2.5).

## Prueba de permutación (¿hay promociones?)

**En una frase:** comprobar si un patrón es más fuerte que el que saldría mezclando los datos al azar.

- **Cómo funciona:** si hubiera promociones (un producto rebajado un mes entero), el descuento de cada producto variaría mucho entre meses. Mezclamos 200 veces los descuentos de cada producto entre sus ventas y medimos cuánto variaría por azar.
- **Ejemplo:** la variación real es igual a la del azar (p = 0,3). No hay promociones; el descuento cambia venta a venta (A2.5).

## Regresión logística y odds ratio (marketing)

**En una frase:** la regresión para resultados de sí o no (convirtió o no), y su forma de expresar el efecto.

- **Odds ratio:** 1 es "sin efecto"; menos de 1, "convierte menos".
- **Ejemplo:** haber devuelto algo antes de recibir la campaña da 0,71: parecía que la devolución espantaba. Al tener en cuenta cuántas compras llevaba el cliente y la fecha, sube a 0,85 y deja de ser significativo (p = 0,15). Era una correlación, no una causa: quien devuelve es quien más compra (A4.4).

## El descuento de las campañas como experimento

**En una frase:** si algo se reparte como en un sorteo, la diferencia de resultados se puede atribuir a eso.

- **Cómo lo comprobamos:** los seis niveles de descuento (0% a 25%) tienen casi los mismos envíos y no dependen del segmento (p = 0,46), del tipo (p = 0,19), del canal (p = 0,20) ni del año.
- **Por eso podemos decir "causa":** el descuento sube la conversión *registrada* (+2,7 puntos por cada 10). Pero no las compras reales (A4.2 y A4.3).

## Prueba hacia atrás (clientes en riesgo)

**En una frase:** antes de usar un método para predecir el futuro, comprobar si habría acertado en el pasado.

- **Cómo funciona:** con lo que sabíamos el 31-dic-2023, predecimos qué parte de los clientes en riesgo volvió en el primer semestre de 2024 y lo comparamos con lo que pasó.
- **Resultado:** agrupando solo por "recurrente o no" y días sin comprar, con los recurrentes previmos 58% y volvió el 56%. Versiones más complejas (todas las compras, compras de 12 meses, calibración, regresión logística) no la mejoraban, así que nos quedamos con la que se explica en una frase (A3.4).
- **Por qué no usamos el segmento del archivo para esto:** con él la prueba "acierta" (41% y 41%), pero solo porque el segmento se definió con las compras de los 24 meses, incluidas las posteriores. Es como predecir un partido sabiendo el resultado.

---

## Preguntas difíciles que nos pueden hacer

| Pregunta | Respuesta corta | Dónde |
|---|---|---|
| ¿Cómo era "Inactivo" un cliente en enero de 2023 si la etiqueta depende de lo que compró hasta 2024? | No lo era: la etiqueta usa información posterior. Por eso no la usamos para predecir. | A1.4, A3.4 |
| Si bajan el descuento online, ¿cómo saben que los clientes no se van? | No lo sabemos del todo: solo vemos las ventas que ocurrieron. Ni las unidades ni la recompra (cada cliente contra sí mismo) cambian con el descuento. En el peor caso compatible con los datos se perdería un 1,2% de las recompras, y R1 compensa hasta que online pierda el 16% de sus ventas. Aun así, es un piloto. | A2.5, A5.3 |
| Si nada empeora, ¿qué explica la presión en el margen? | El margen no baja, pero lleva dos años perdiendo lo mismo en tres sitios: descuento online, devoluciones de dos categorías y un marketing sin medir. | A1, A5.1 |
| ¿Qué tamaño de efecto podían detectar en las quejas? | Caídas de más de 0,21 compras en 90 días. Como mucho, 19.159 en 6 meses. | A3.3 |
| ¿Recorto el presupuesto de marketing? | No se puede saber con estos datos. Primero hay que medir con grupo de control (R3). Lo que sí: ningún descuento de campaña por encima de 5% (R4). | A4, A5.5 |
| Si lo devuelto se revende, ¿por qué los reembolsos son ingresos perdidos? | No los sumamos como fuga. Son un costo estructural y van aparte; la cifra principal solo incluye lo que Ropa y Electrónica devuelven por encima de lo normal. | A3.5 |
| ¿Por qué controlaban por segmento en la recompra? | Fue un error: el segmento es circular. Lo cambiamos por comparar a cada cliente consigo mismo, y la conclusión se mantiene (+0,0 puntos). | A2.5, bitácora |
| ¿Cómo saben que la estimación de la vuelta funciona? | La probamos hacia atrás: con los recurrentes, 58% previsto contra 56% real. Con los de una sola compra falla más, pero no entran en la cifra principal. | A3.4 |
| R2 a R4 suman poco: ¿son recomendaciones o notas al pie? | R1 trae el dinero. R2 y R3 sirven para medir antes de gastar: R2 tiene un techo de hasta 161.647 de margen si el diagnóstico encuentra la causa, y R3 permitirá saber por fin si el marketing funciona. R4 evita regalar descuento sin retorno. | A5.2 |
| ¿Por qué dicen "evitable" si no conocen la causa? | Ya no lo decimos: es "por encima de lo normal". Solo la parte de la talla tiene causa conocida. | A3.5, A5.4 |
| ¿En qué moneda está el CLV? ¿Por qué sin tasa de descuento? | En unidades monetarias del archivo. Con 10% y 20% de tasa los valores bajan, pero el orden no cambia. | A2.2 |
| ¿Por qué llaman estrella a un modelo con cuatro hechos? | Es una constelación de hechos: cuatro hechos que comparten dimensiones. | `docs/modelo.md` |
