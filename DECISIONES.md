# Decisiones del proyecto

Este documento explica, fase por fase, qué decidimos y por qué. Las cifras salen de los notebooks de cada fase. Lo que cambia los datos está aplicado en `src/carga.py`, en la función `cargar_limpio()`.

Las decisiones marcadas **"A confirmar con el profesor"** son supuestos nuestros: el enunciado no dice cómo hacerlo. Las aplicamos así por ahora y están en la agenda de `FEEDBACK_PROFESOR.md`.

## A1 – Calidad de los datos

Cifras de `notebooks/01_calidad.ipynb`.

### Regla general: no borramos filas

Los datos vienen limpios en la forma: no hay celdas vacías, filas repetidas ni códigos que apunten a registros inexistentes. Los problemas están en lo que significan algunos datos.

Por eso no eliminamos nada. Cuando un registro es raro, le agregamos una columna que lo marca (verdadero/falso). Así cada análisis decide si lo incluye o no.

### Lo que encontramos

- No hay celdas vacías ni filas repetidas en ninguna de las 6 tablas.
- Todos los códigos de cliente, producto y transacción existen en su tabla.
- Los montos, precios y márgenes cuadran en el 100% de las filas.
- 433 clientes tienen el género como "No especificado". Es un dato faltante escrito como texto.
- Hay 318 productos. El enunciado dice 320.
- Hay un tercer canal de venta, la app móvil, que el enunciado no menciona.
- Las cifras del enunciado no coinciden con los datos (sección 5 del notebook). Así medimos cada una:
  - **Ticket promedio:** total vendido dividido entre el número de compras.
  - **Devoluciones:** de cada 100 ventas de un trimestre, cuántas se devolvieron.
  - **Conversión:** de cada 100 campañas enviadas en un trimestre, cuántas quedaron marcadas como convertidas.

| Métrica | Qué dice el enunciado | Qué muestran los datos | ¿Coincide? |
|---|---|---|---|
| Ticket promedio | Bajó 8% en un año | Bajó 1,9% (de 351 en 2023 a 344 en 2024). Comparando solo el último trimestre de cada año, bajó 0,2% | **No** |
| Devoluciones | Subieron hasta 14% en el último trimestre | 13,5% en el último trimestre, pero siempre entre 13,0% y 13,8% desde 2023 | **A medias:** el nivel se parece, pero no hubo subida |
| Conversión de campañas | Bajó de 22% a 11% en 18 meses | Bajó de 11,3% a 5,6% entre el primer trimestre de 2023 y el último de 2024 | **En parte:** se cayó a la mitad, pero empezó en 11%, no en 22% |

### Decisiones

#### A1.1 Compras hechas antes de la fecha de registro del cliente

**Qué pasa:** la mitad de las compras (24.972) tiene una fecha anterior a la fecha en que el cliente se registró.

**Qué hicimos:** conservamos esas compras. Para medir cuánto tiempo lleva alguien como cliente no usamos la fecha de registro, sino la fecha de su primera compra.

**Por qué:** el problema aparece igual en los tres canales, y la fecha de registro no tiene ninguna relación con la fecha de la primera compra. Además, la empresa tiene 12 años, pero todos los registros son de 2023 y 2024. Lo más probable es que esa fecha sea el alta en un sistema nuevo, no el día en que el cliente empezó a comprar.

#### A1.2 Campañas marcadas como convertidas sin una compra que lo confirme

**Qué pasa:** hay 797 envíos de campaña marcados como convertidos. Los datos no dicen qué compra generó cada campaña, así que buscamos una compra del mismo cliente en los 30 días siguientes al envío. Solo la encontramos en 179 casos. En otros 102, la única compra cercana es anterior al envío.

**Qué hicimos:**
- Para comparar tasas de conversión entre tipos de campaña, canales y segmentos, usamos la marca de conversión tal como viene.
- Para calcular cuánto dinero trajo una campaña (y su retorno), solo contamos las 179 conversiones con compra confirmada.

**Por qué:** la marca de conversión es lo que registra la empresa. El porcentaje de conversiones confirmadas es casi igual en 2023 y 2024 (22% y 23%), así que la tendencia sigue siendo válida. Pero varía entre tipos de campaña: 17% en redes sociales y 25% en emails. Por eso, en A4, las diferencias pequeñas entre tipos de campaña no son concluyentes.

Esto hay que mencionarlo como limitación en la presentación.

#### A1.3 Ventas por debajo del costo

**Qué pasa:** en 711 ventas, el cliente pagó menos de lo que le costó el producto a la empresa.

**Qué hicimos:** las conservamos y las marcamos.

**Por qué:** no es un error. 633 son de Electrónica, la categoría con menos margen: un producto típico de Electrónica deja 18,6% de su precio de lista. Con descuentos de entre 9% y 34,5%, la venta termina en pérdida. Es un hallazgo para A2.

#### A1.4 El segmento del cliente no coincide con su comportamiento

**Qué pasa:** 108 clientes marcados como "Inactivo" compraron en los últimos 90 días.

**Qué hicimos:** dejamos el segmento original, porque el enunciado pide analizar por segmento. Además agregamos un segundo segmento, calculado según cómo compra cada cliente en realidad:

| Segmento calculado | Regla |
|---|---|
| Sin compras | nunca compró |
| Inactivo | lleva más de 180 días sin comprar |
| Premium | está en el 10% de clientes que más gastó |
| Frecuente | tiene 8 compras o más |
| Nuevo | hizo su primera compra en los últimos 90 días |
| Esporádico | todos los demás |

Las reglas se aplican en ese orden: a cada cliente le toca la primera que cumpla, de arriba hacia abajo.

**Por qué 180 días:** cuando un cliente vuelve a comprar, 9 de cada 10 veces lo hace en menos de 162 días. Pasar de 180 días sin comprar es, por tanto, una ausencia fuera de lo normal.

**Ojo:** eso no significa que el cliente se haya perdido. De los clientes que llegan a 180 días sin comprar, el 52% vuelve en los 180 días siguientes. "Inactivo" quiere decir "en riesgo", no "perdido". En A3 hay que tenerlo en cuenta al definir qué es un cliente perdido.

#### A1.5 Clientes que nunca compraron

**Qué pasa:** 392 clientes no tienen ninguna compra.

**Qué hicimos:** los conservamos y los marcamos. No entran en el cálculo del valor del cliente ni en el de clientes perdidos, pero sí en el análisis de campañas.

**Por qué:** no se puede perder a un cliente que nunca compró. Pero 242 de ellos reciben campañas, y eso cuenta para medir si el marketing funciona.

#### A1.6 Tiempos de respuesta muy altos en atención al cliente

**Qué pasa:** 352 contactos tardaron más de 48,9 horas en recibir respuesta, y 15 tardaron más de una semana. Las 48,9 horas son el límite a partir del cual un valor se considera fuera de lo normal en estos datos (regla del rango intercuartílico).

**Qué hicimos:** los conservamos y los marcamos. En los resúmenes usamos la mediana (el valor del medio), que no se deja arrastrar por los casos extremos.

**Por qué:** una respuesta lenta no es un error de los datos. Es justo lo que queremos estudiar en A3.

#### A1.7 Ventas con montos muy altos

**Qué pasa:** si buscamos montos fuera de lo normal mirando todas las ventas juntas, salen 4.138. Dos tercios (2.672) son de Electrónica.

**Qué hicimos:** buscamos los montos fuera de lo normal dentro de cada categoría (salen 3.420) y los marcamos. No eliminamos ninguno.

**Por qué:** Electrónica sale "fuera de lo normal" solo porque sus productos son más caros. Es más justo comparar cada venta con las de su propia categoría. Y aun así son ventas reales, con montos que cuadran.

## A2 – Rentabilidad y comportamiento de compra

Cifras de `notebooks/02_rentabilidad.ipynb`.

### Qué pide el enunciado y cómo lo cubrimos

| Qué pide el enunciado | Cómo lo cubrimos | ¿El enunciado dice cómo hacerlo? |
|---|---|---|
| Segmentos, categorías y canales con mayor y menor contribución al **margen bruto** total | Tablas con el % de las ventas, del margen bruto y del margen neto de cada uno (sección 2) | Sí: pide margen bruto. El margen neto es un agregado nuestro |
| CLV estimado por segmento y qué segmentos están en declive | CLV a 3 años por segmento y comparación 2023 contra 2024 (sección 3) | No: ni la fórmula, ni el horizonte, ni qué es "declive" |
| Estacionalidad: picos, valles y tendencias por categoría y canal | Mes pico, mes valle y tendencia de cada categoría y canal, y pruebas de si se repiten (sección 4) | No dice el método |
| ¿Los descuentos generan volumen suficiente para compensar la pérdida de margen? | Volumen necesario contra volumen real y una regresión (sección 5) | No dice el método |

### Decisiones

#### A2.1 Margen neto: qué pasa con una venta devuelta

**Qué pasa:** el enunciado pide el margen bruto, pero las devoluciones reembolsan el 100% de la venta y se llevan una parte grande del margen. No hay ningún dato que diga si el producto devuelto se puede volver a vender.

**Qué hicimos:** el margen bruto es la medida principal, como pide el enunciado. Además calculamos un margen neto:
- Si la venta no se devolvió, el margen neto es igual al bruto.
- Si se devolvió y el producto vuelve bien (cambio de opinión, talla, no cumple expectativas, demora o error en el pedido), se revende: la venta se deshace y su margen neto es 0.
- Si se devolvió por producto defectuoso o fraude, no se puede revender: se pierde también lo que costó. El margen neto es el costo, en negativo.

**Por qué:** sin el margen neto no se ve el efecto de las devoluciones, que se llevan el 27,5% del margen bruto. Y separar por motivo es más realista que suponer que todo se revende (subestima la pérdida) o que todo se pierde (la exagera).

**A confirmar con el profesor:** si le parece bien este supuesto sobre qué se revende.

#### A2.2 Cómo calculamos el CLV

**Qué pasa:** el enunciado pide el CLV por segmento, pero no dice cómo calcularlo.

**Qué hicimos:** CLV = margen neto de un semestre × (1 + r + r² + … + r⁵).
- **Margen de un semestre:** margen neto promedio de los clientes del segmento que compraron en ese semestre.
- **r:** retención semestral, es decir, qué porcentaje de esos clientes vuelve a comprar el semestre siguiente.
- **Horizonte:** 3 años (6 semestres), sin tasa de descuento.

**Por qué:**
- Con un horizonte fijo, el CLV no se vuelve infinito en los segmentos que casi nunca se pierden (Premium retiene al 99%).
- No usamos tasa de descuento porque habría que justificar cuál, y en Venezuela, con inflación, es muy discutible.
- Usamos semestres y no años porque con 2 años de datos solo hay un paso de un año al siguiente, y así no se puede ver si el CLV cae. Con semestres hay tres. La versión anual (con el paso 2023 → 2024) da el mismo orden de segmentos.

**A confirmar con el profesor:** la fórmula, el horizonte de 3 años y no usar tasa de descuento.

#### A2.3 Cuándo decimos que un segmento está "en declive"

**Qué pasa:** el enunciado pide detectar los segmentos en declive, pero no dice qué cuenta como declive.

**Qué hicimos:** comparamos el CLV de 2023 (S1 → S2) con el de 2024 (S1 → S2). Solo hablamos de declive si el CLV baja y la caída se mantiene al remuestrear los clientes 1.000 veces (*bootstrap*), es decir, si el intervalo de confianza del 95% de la caída no incluye el 0.

**Por qué:** la rúbrica penaliza sacar conclusiones de diferencias que pueden ser casualidad. Con este criterio, ningún segmento está en declive: todos los cambios caben dentro de lo que podría ser azar.

**A confirmar con el profesor:** el criterio de declive y que se use el segmento que trae el archivo (el segmento calculado en A1 queda solo como contraste).

#### A2.4 Cómo comprobamos la estacionalidad

**Qué pasa:** el enunciado pide picos, valles y tendencias, pero cualquier serie de 24 meses tiene un mes más alto y uno más bajo, aunque sea por casualidad.

**Qué hicimos:** nombramos el mes pico, el mes valle y la tendencia de cada categoría y canal, como pide el enunciado. Además comprobamos si son reales:
- si el patrón mensual de 2023 se repite en 2024 (correlación entre los dos años),
- si algún mes vende distinto a los demás (prueba de Kruskal-Wallis),
- si el intervalo de confianza de la tendencia incluye el 0.

**Por qué:** decir "marzo es el pico de Ropa" sin comprobar que se repite sería presentar ruido como un hallazgo. Resultado: los picos y valles no se repiten entre años y no hay estacionalidad.

#### A2.5 Cómo medimos el efecto de los descuentos

**Qué pasa:** que las ventas con descuento tengan menos margen es obvio. La pregunta es si generan volumen suficiente para compensarlo.

**Qué hicimos:**
- Calculamos cuánto volumen extra haría falta para ganar lo mismo (d / (g − d), donde g es el margen a precio de lista y d el descuento) y lo comparamos con el volumen extra real.
- Hicimos una regresión de las unidades por compra según el descuento, dejando fijos la categoría, el canal y el segmento.
- Miramos si el mismo producto vende más en los meses con más descuento, y si los clientes con más descuento compran más veces.

**Por qué:** la rúbrica penaliza presentar correlaciones sin investigar la causa. Comparar el mismo producto en distintos meses y controlar categoría, canal y segmento descarta las explicaciones más obvias. Además, el margen de lista es igual en todas las bandas de descuento (34%), así que los descuentos no se reparten según el tipo de producto. Resultado: los descuentos no generan volumen.

**Límite:** no tenemos un experimento (un grupo con descuento y otro sin él elegidos al azar), así que no podemos descartar todas las explicaciones. Lo decimos así en la presentación.

## A3 – Fugas de ingresos

Cifras de `notebooks/03_fugas.ipynb`.

### Qué pide el enunciado y cómo lo cubrimos

| Qué pide el enunciado | Cómo lo cubrimos | ¿El enunciado dice cómo hacerlo? |
|---|---|---|
| Productos, categorías o segmentos con tasas de devolución anómalas, y clientes recurrentes en devoluciones | Tasa por categoría, subcategoría, producto, segmento, canal y medio de pago, con pruebas; simulación de cuántas devoluciones por cliente serían normales (sección 1) | No dice qué es "anómala" ni "recurrente" |
| ¿Los clientes con quejas no resueltas disminuyeron su frecuencia de compra? | Compras 90 días antes y después de cada queja, comparando quejas sin resolver con quejas resueltas (sección 2) | No dice el método |
| Una métrica de inactividad y el segmento de mayor valor en riesgo | Días sin comprar; probabilidad de volver estimada con la historia; valor en riesgo por segmento (sección 3) | Pide definir la métrica, no dice cuál |
| Impacto económico de las fugas en ingresos perdidos a 6 meses | Clientes que no vuelven + devoluciones + quejas, cada uno por separado (sección 4) | No dice el método |

### Decisiones

#### A3.1 Cuándo una tasa de devolución es "anómala"

**Qué pasa:** con 318 productos, algunos van a tener tasas altas o bajas por pura casualidad. Si probamos cada uno al 5%, unos 16 saldrían "anómalos" aunque no lo sean.

**Qué hicimos:** una tasa es anómala si una prueba binomial dice que se aleja de la tasa de referencia y sigue siéndolo después de corregir por el número de pruebas (Benjamini-Hochberg). Mostramos también el intervalo de confianza del 95% (Wilson). Para productos y subcategorías la referencia es la tasa **de su propia categoría**, no la global.

**Por qué:** comparando con la global salen 51 productos anómalos, pero son solo el reflejo de su categoría (32 son de ropa). Comparando con su categoría no queda ninguno. Así el hallazgo es claro: el problema está en Ropa y Calzado (21,8%) y en Electrónica (17,7%) completas, no en productos sueltos. Todos los productos tienen al menos 115 ventas, así que no hay grupos demasiado pequeños para probarlos.

**A confirmar con el profesor:** la corrección por número de pruebas y comparar los productos con su categoría.

#### A3.2 Qué es un cliente "recurrente en devoluciones"

**Qué pasa:** un cliente que compra mucho tiene más devoluciones aunque se comporte como cualquier otro. Contar devoluciones no basta.

**Qué hicimos:** simulamos 1.000 veces las devoluciones de cada cliente con sus compras reales y la tasa de devolución de la categoría de cada compra. Comparamos cuántos clientes tienen 0, 1, 2, 3… devoluciones en los datos y en las simulaciones.

**Por qué:** si hubiera "devolvedores" habituales, habría más clientes con muchas devoluciones de lo que da el azar. No los hay: 793 clientes tienen 3 o más, y por azar se esperarían 785. Todas las cifras caen dentro del rango simulado. Solo 5 clientes repiten fraude.

**A confirmar con el profesor:** el método. Es la forma de no confundir "compra mucho" con "devuelve mucho".

#### A3.3 Cómo medimos el efecto de las quejas sin resolver

**Qué pasa:** el enunciado pregunta si los clientes con quejas no resueltas compran menos después. Mirar solo el "después" no sirve: tras cualquier contacto podría haber una caída normal.

**Qué hicimos:**
- Para cada queja, las compras del cliente en los 90 días antes y en los 90 días después. Solo quejas con 90 días de datos a cada lado (1.517).
- Comparamos el cambio de las quejas sin resolver con el cambio de las resueltas (diferencia en diferencias), con intervalo de confianza *bootstrap* por cliente y con una regresión que deja fijo el segmento.
- Como comprobación, si el cliente vuelve a comprar en 180 días, y si influye el tiempo de respuesta.

**Por qué:** es la forma más directa de responder la pregunta que se puede hacer con estos datos, y descarta la caída "normal" tras cualquier contacto. Resultado: no hay efecto. Tras una queja sin resolver se pasa de 0,98 a 0,92 compras; tras una resuelta, de 0,97 a 0,95. La diferencia (−0,03) tiene un IC 95% de −0,21 a +0,13. A 180 días vuelve el 67% contra el 71% (p = 0,35).

**Límite:** no es un experimento; la resolución no se asigna al azar. Pero como no aparece ni siquiera una asociación, no hay nada que explicar con otras causas.

**A confirmar con el profesor:** la ventana de 90 días y la comparación con las quejas resueltas.

#### A3.4 Cuándo un cliente está en riesgo de fuga

**Qué pasa:** el enunciado pide definir una medida de inactividad. En A1.4 vimos que pasar de 180 días sin comprar es poco normal, pero que el 52% de los que llegan a 180 días vuelve. Llamar "perdido" a todo el que pasa de 180 días exageraría la fuga.

**Qué hicimos:**
- **Medida:** días sin comprar al cierre de los datos (31-dic-2024). **En riesgo:** más de 180 días, el mismo umbral de A1.4. Son 2.647 clientes, el 35% de los que alguna vez compraron.
- **Probabilidad de volver:** nos ponemos en una fecha pasada con 6 meses de datos por delante (30-jun-2024) y contamos qué parte de los clientes volvió en esos 6 meses, por segmento y por tramo de días sin comprar (91–180, 181–270, más de 270). Esa proporción es la probabilidad de volver de cada cliente en riesgo de hoy.
- **Prueba:** con la foto del 31-dic-2023 predijimos el primer semestre de 2024. Previmos que volvería el 41% de los clientes en riesgo, y volvió el 41%.

**Por qué:** la probabilidad depende sobre todo del segmento. Los Frecuentes y Premium en riesgo vuelven casi siempre (90% a 100%), los Esporádicos la mitad, los Nuevos el 18% y los "Inactivo" del archivo nunca (en el archivo, "Inactivo" son clientes con una compra como mucho). Usar una sola probabilidad para todos mezclaría grupos muy distintos.

**Nota sobre el 52% de A1:** el 52% cuenta cada vez que un cliente cumple 180 días sin comprar. Aquí miramos una foto en una fecha, y el grupo de "más de 180 días" incluye a clientes que llevan mucho más tiempo, que vuelven menos. Por eso en la foto vuelve el 41-45%.

**A confirmar con el profesor:** el umbral de 180 días y estimar la probabilidad de volver con una foto pasada.

#### A3.5 Cómo calculamos los ingresos perdidos a 6 meses

**Qué pasa:** el enunciado pide el impacto en "ingresos perdidos proyectados a 6 meses", pero no dice cómo proyectarlos.

**Qué hicimos:** cada fuga por separado:
- **Clientes en riesgo:** (1 − probabilidad de volver) × lo que el cliente venía gastando por semestre desde su primera compra. Total: 365.781 (8,4% de las ventas de un semestre). Rango: desde el IC 2,5% *bootstrap* de esa cifra hasta el IC 97,5% de una versión alta, en la que el cliente gastaría como los que sí vuelven (341.539 a 844.619).
- **Devoluciones:** la tasa y las ventas del último semestre (jul–dic 2024). 645.677 en ingresos reembolsados y 288.132 de margen perdido (regla de A2.1). Aparte damos el **exceso** de Ropa y Electrónica sobre la tasa de las otras categorías: 169.423 en ingresos, que es la parte que se podría recuperar.
- **Quejas sin resolver:** 0, porque en A3.3 no hay efecto.

**Por qué:**
- La cifra principal de clientes es prudente a propósito. En la prueba hacia atrás, los clientes que volvieron gastaron 1,41 veces lo que venían gastando, pero esa estimación fallaba un 12% en el gasto. Preferimos no inflar la cifra principal con ella y la dejamos como tope.
- No hay doble conteo: la fuga de clientes son ventas que no ocurren; las devoluciones son ventas que ocurren y se reembolsan.
- Total: 1.011.458 en 6 meses, el 23,2% de las ventas de un semestre.

**A confirmar con el profesor:** si "ingresos perdidos" debe incluir las devoluciones (nosotros las damos aparte) y el supuesto de gasto de los clientes que se van.

## A4 – Efectividad del marketing

Cifras de `notebooks/04_marketing.ipynb`.

### Qué pide el enunciado y cómo lo cubrimos

| Qué pide el enunciado | Cómo lo cubrimos | ¿El enunciado dice cómo hacerlo? |
|---|---|---|
| Conversión por tipo de campaña, canal y segmento, y las combinaciones con más retorno | Tasas con IC, prueba de si hay combinaciones especiales y dinero confirmado por cada 1.000 envíos (sección 1) | Sí para las tasas; no dice qué es "retorno" |
| Efecto del descuento sobre la conversión, controlando por segmento | Conversión por nivel de descuento y regresión con segmento y tipo; comprobación con compras reales (sección 2) | Pide controlar por segmento; no dice el método |
| Segmento que recibe campañas y no convierte, con hipótesis desde el CRM y las devoluciones | Perfil del segmento y prueba de cada hipótesis con regresión (sección 3) | No dice el método |
| ROI de cada tipo de campaña: monto convertido contra costo implícito del descuento | ROI sobre ventas (el del enunciado), sobre margen e incremental (sección 4) | Da la idea, no la fórmula exacta |

### Decisiones

#### A4.1 Tipo de campaña y canal se analizan juntos

**Qué pasa:** cada tipo de campaña sale siempre por el mismo canal (por ejemplo, `push_reactivacion` siempre por la app).

**Qué hicimos:** damos las dos tablas, como pide el enunciado, pero las combinaciones las buscamos entre tipo y segmento. Para saber si una combinación es "especial" comparamos una regresión con interacción tipo × segmento con otra sin ella.

**Por qué:** con los datos no se puede separar el efecto del tipo del efecto del canal. Resultado: no hay combinaciones especiales (p = 0,79); lo que cambia la conversión es el segmento.

#### A4.2 El efecto del descuento se puede leer como causal

**Qué pasa:** normalmente, comparar la conversión con y sin descuento solo da una correlación: la empresa podría dar más descuento a quien ya iba a comprar.

**Qué hicimos:** comprobamos cómo se repartió el descuento. Los seis niveles (0% a 25%) tienen casi los mismos envíos y no dependen del segmento (p = 0,46), del tipo (p = 0,19), del canal (p = 0,20) ni del año. Medimos el efecto con una regresión que controla segmento y tipo.

**Por qué:** si el descuento se reparte como en un sorteo, la diferencia de conversión entre niveles es efecto del descuento. Es lo más parecido a un experimento que tenemos, y responde a la rúbrica, que penaliza las correlaciones sin investigar la causa. Resultado: +2,7 puntos de conversión por cada 10 de descuento, hasta el 20%.

**A confirmar con el profesor:** que el reparto del descuento se puede tratar como aleatorio.

#### A4.3 Comprobamos la conversión con las compras reales

**Qué pasa:** en A1.2 vimos que solo 179 de las 797 conversiones tienen una compra detrás.

**Qué hicimos:** para cada envío miramos si el cliente compró en los 30 días después y en los 30 días antes (solo envíos con 30 días de datos a cada lado). Repetimos con eso el análisis del descuento y de la caída de la conversión.

**Por qué:** si las campañas funcionan, debería haber más compras después del envío que antes, y más con más descuento. No pasa ninguna de las dos cosas: 20,8% compra después y 21,4% antes; el descuento no cambia la compra real (+0,1 puntos por cada 10; IC 95%: −0,8 a 1,1). Y la conversión marcada cae a la mitad en 2024, mientras las compras tras una campaña se mantienen.

**Consecuencia:** con estos datos no se puede demostrar que las campañas generen ventas. O la marca de conversión registra algo que no está en el archivo de transacciones, o no es fiable. Lo presentamos como limitación, no como prueba de que el marketing no sirve.

**A confirmar con el profesor:** ¿la conversión puede venir de compras que no están en `transacciones.csv`? ¿Cuál de las dos lecturas usamos en la presentación?

#### A4.4 Cómo probamos las hipótesis sobre el segmento que no convierte

**Qué pasa:** el enunciado pide hipótesis basadas en el CRM y en las devoluciones para el segmento que no convierte (Inactivo: 5,5%).

**Qué hicimos:** para cada envío marcamos si el cliente había tenido antes una queja, una queja sin resolver o una devolución, y medimos su efecto en la conversión con una regresión. Primero controlando segmento y descuento; después agregando cuántas compras llevaba el cliente y la fecha.

**Por qué:** la devolución previa parece bajar la conversión (odds ratio 0,71), pero quien devolvió es quien más compra, y la conversión cae con el tiempo. Al controlarlo, el efecto desaparece (odds ratio 0,85; p = 0,15). Ninguna de las tres hipótesis se sostiene. Lo que sí distingue a los Inactivo es que compraron una vez como mucho y que solo convierten con descuentos grandes. Por eso proponemos otra hipótesis: son clientes poco fieles y sensibles al precio.

#### A4.5 Cómo calculamos el ROI

**Qué pasa:** el enunciado pide el ROI con el monto convertido contra el costo implícito del descuento, pero no da la fórmula.

**Qué hicimos:**
- **Monto convertido:** solo compras confirmadas (A1.2). **Costo del descuento:** descuento ofrecido × monto de esa compra.
- **ROI sobre ventas** = (monto − costo) / costo. Es el que pide el enunciado: 5,80 en total.
- **ROI sobre margen** = (margen bruto de esas compras − costo) / costo: 0,59 en total, con IC *bootstrap* por tipo.
- **ROI incremental:** el margen de las conversiones que no habría sin descuento (frente al 0%), contra el descuento que se regala a todas las conversiones. Valoramos cada conversión con el ticket medio (355) y el margen (23,4%) de las compras confirmadas. Resultado: −31%.

**Por qué:**
- El ROI sobre ventas sale casi igual a (1 − d) / d, con d = descuento medio. Mide el descuento, no la campaña. Por eso agregamos el de margen.
- Ninguno de los dos tiene en cuenta que esas compras quizá habrían ocurrido igual. El incremental sí, y es el que sirve para decidir: aunque aceptemos la marca de conversión, solo el descuento de 5% se paga solo.
- Usamos el descuento ofrecido y no el de la transacción porque es lo que pide el enunciado, y porque no coinciden (correlación de 0,04).

**A confirmar con el profesor:** las tres versiones del ROI y cuál presentar como principal.

## A5 – Recomendaciones

Cifras de `notebooks/05_recomendaciones.ipynb`. El entregable de A5 es un dashboard de Power BI (`docs/dashboard.md`) y un informe escrito.

### Decisiones

#### A5.1 Cómo cuantificamos las recomendaciones

**Qué pasa:** el enunciado pide cada recomendación como "Si hacemos X, esperamos Y% en Z, equivalente a [monto] en ingresos", pero el impacto de una medida que no se ha aplicado no se puede medir con los datos.

**Qué hicimos:** cada recomendación sale de un hallazgo de A2–A4 y depende de un supuesto explícito. Damos un escenario central y un rango, en cifras anuales con base 2024, y siempre ingresos **y** margen.

| | Qué hacemos | Supuesto | Ingresos al año | Margen al año |
|---|---|---|---|---|
| R1 | Tope de 4,7% al descuento por venta online (iguala el descuento medio de tienda y app) | Las unidades no cambian (A2.5) | +141.067 (72.232 a 141.067) | +141.067 |
| R2 | Guía de tallas en Ropa, mejores fichas en Electrónica, control de proveedores | Se recorta el 50% del exceso de devoluciones (25% a 75%) | +185.082 (92.541 a 277.623) | +80.824 |
| R3 | Campaña de reactivación a Esporádicos en riesgo, con 20% de grupo de control | Se recupera el 10% de lo que está en riesgo (5% a 20%) | +33.954 (16.977 a 67.909) | +8.456 |
| R4 | Tope de 5% al descuento de las campañas | Lectura de la marca de conversión (A4.5) | −21.737 | +7.197 |

Total central: 237.544 de margen al año, el 11,0% del margen bruto de 2024.

**Por qué:** dar un solo número sin decir de qué depende sería presentar una suposición como un hallazgo. Ordenamos por margen y no por ingresos porque el problema de la empresa es el margen.

**A confirmar con el profesor:** si los escenarios con rango son aceptables como "impacto esperado".

#### A5.2 R1: por qué creemos que el descuento online se puede bajar

**Qué pasa:** si al bajar el descuento online se vendiera menos, la cifra de R1 sería falsa.

**Qué hicimos:** nos apoyamos en A2.5 (el descuento no mueve las unidades, también comparando el mismo producto en distintos meses) y calculamos cuánto podría caer la venta online antes de que la medida deje de compensar: un 16%.

**Por qué:** A2.5 no es un experimento. Por eso recomendamos aplicar R1 primero en una parte de los productos y medir.

#### A5.3 R3: por qué la recomendación de reactivación lleva grupo de control

**Qué pasa:** en A4.3 vimos que no hay pruebas de que las campañas actuales generen compras. Recomendar "más campañas" sin poder medirlas no tendría base.

**Qué hicimos:** la recomendación incluye dejar un 20% de los clientes, elegidos al azar, sin la campaña. Las cifras son escenarios (5%, 10% y 20% de lo que está en riesgo), no una estimación.

**Por qué:** el valor seguro de R3 es que la empresa podrá saber, por primera vez, si una campaña genera ventas.

#### A5.4 R4: por qué una recomendación que baja los ingresos

**Qué pasa:** con la lectura más favorable al descuento (la marca de conversión), un tope de 5% hace que haya menos conversiones: los ingresos registrados bajan 21.737, pero el margen sube 7.197, porque se deja de regalar descuento que no se paga.

**Qué hicimos:** lo presentamos con las dos cifras y avisamos que la conversión registrada bajará (de 10,6% a 6,9% en esos envíos).

**Por qué:** el problema de la empresa es el margen. Con la lectura de las compras reales (A4.3), el beneficio sería mayor, porque el descuento de campaña no cambia las compras.

## Columnas que agrega `cargar_limpio()`

| Tabla | Columnas nuevas |
|---|---|
| transacciones | `categoria`, `subcategoria`, `costo_total`, `margen_bruto`, `bajo_costo`, `outlier_cat`, `devuelta`, `mes`, `trimestre` (A1); `costo_descuento`, `motivo_devolucion`, `margen_neto` (A2) |
| clientes | `primera_compra`, `ultima_compra`, `n_compras`, `gasto_total`, `margen_total`, `sin_compras`, `dias_sin_comprar`, `segmento_rfm` (A1); `margen_neto_total` (A2) |
| devoluciones | `fecha_compra`, `producto_id`, `categoria`, `canal`, `monto_neto`, `dias_a_devolucion` |
| interacciones_crm | `respuesta_atipica` |
| campanas_marketing | `compra_en_ventana`, `conversion_respaldada`, `monto_respaldado` |

Los umbrales (30, 90 y 180 días, y 8 compras) y los motivos de devolución en los que el producto se pierde están al principio de `src/carga.py`. Si el profesor pide otros valores, se cambian ahí.
