# Decisiones sobre los datos

Este documento explica qué problemas encontramos en los datos y qué hicimos con cada uno.
Las cifras salen de `notebooks/01_calidad.ipynb`. Los cambios están aplicados en `src/carga.py`, en la función `cargar_limpio()`.

## Regla general: no borramos filas

Los datos vienen limpios en la forma: no hay celdas vacías, filas repetidas ni códigos que apunten a registros inexistentes. Los problemas están en lo que significan algunos datos.

Por eso no eliminamos nada. (El código descarta filas repetidas por si en el futuro llegan archivos nuevos con duplicados; hoy no elimina ninguna.) Cuando un registro es raro, le agregamos una columna que lo marca (verdadero/falso). Así cada análisis decide si lo incluye o no.

## Lo que encontramos

- No hay celdas vacías ni filas repetidas en ninguna de las 6 tablas.
- Todos los códigos de cliente, producto y transacción existen en su tabla.
- Los montos, precios y márgenes cuadran en el 100% de las filas.
- 433 clientes tienen el género como "No especificado". Es un dato faltante escrito como texto.
- Ningún valor numérico es imposible. Revisamos todos los campos numéricos con la regla del rango intercuartílico (tabla en la sección 1 del notebook). Lo que sale "fuera de lo normal" son productos caros (Electrónica) y compras de 4 o 5 unidades, que son posibles.
- 158 devoluciones están fechadas el 31-dic-2024, contra 9 en un día normal (decisión A1.8).
- Los montos no dicen en qué moneda están. Hablamos de "unidades monetarias" (u. m.).
- Hay 318 productos. El enunciado dice 320.
- Hay un tercer canal de venta, la app móvil, que el enunciado no menciona.
- Las cifras del enunciado no coinciden con los datos (sección 5 del notebook). Así medimos cada una:
  - **Ticket promedio:** total vendido dividido entre el número de compras.
  - **Devoluciones:** de cada 100 ventas de un trimestre, cuántas se devolvieron. También lo medimos sumando dinero (monto devuelto / monto vendido) y por fecha de devolución en vez de fecha de compra.
  - **Margen bruto:** (ventas − costo) / ventas. El enunciado habla de "presión en los márgenes", así que también lo comprobamos.
  - **Conversión:** de cada 100 campañas enviadas en un trimestre, cuántas quedaron marcadas como convertidas.

| Métrica | Qué dice el enunciado | Qué muestran los datos | ¿Coincide? |
|---|---|---|---|
| Ticket promedio | Bajó 8% en un año | Bajó 1,9% (de 351 en 2023 a 344 en 2024). Comparando solo el último trimestre de cada año, bajó 0,2% | **No** |
| Devoluciones | Subieron hasta 14% en el último trimestre | Contando ventas: siempre entre 13,0% y 13,8%. Sumando dinero: siempre entre 13% y 16% (14,6% de media), que es el "14%" del enunciado. Por fecha de devolución, el último trimestre sube a 15,8%, pero solo por las 158 devoluciones fechadas el 31-dic (sin ellas, 13,3%) | **El nivel sí, la subida no** |
| Conversión de campañas | Bajó de 22% a 11% en 18 meses | Bajó de 11,3% a 5,6% entre el primer trimestre de 2023 y el último de 2024 | **En parte:** se cayó a la mitad, pero empezó en 11%, no en 22% |
| Margen bruto | "Presión creciente en los márgenes" | 24,7% en 2023 y 24,9% en 2024, con ventas casi iguales (8,71 y 8,68 millones) | **No:** el margen no cae |

**Qué significa:** la empresa no está empeorando. El margen, el ticket y las devoluciones están estables desde hace dos años; lo único que cae es la conversión registrada de las campañas. El problema no es una caída, sino un nivel: la empresa lleva dos años perdiendo margen siempre en los mismos sitios. Así lo contamos en el relato (A5).

## Decisiones

### 1. Compras hechas antes de la fecha de registro del cliente

**Qué pasa:** la mitad de las compras (24.972) tiene una fecha anterior a la fecha en que el cliente se registró.

**Qué hicimos:** conservamos esas compras. Tratamos la fecha de registro como un campo sin información y no la usamos. Para medir cuánto tiempo lleva alguien como cliente usamos la fecha de su primera compra.

**Por qué:** el problema aparece igual en los tres canales, y la fecha de registro no tiene ninguna relación con la fecha de la primera compra. Además, la empresa tiene 12 años, pero todos los registros son de 2023 y 2024. Pensamos primero que era el alta en un sistema nuevo, pero entonces casi todas las altas estarían al principio, y no es así: están repartidas en los 24 meses (con más en el último trimestre de 2024). No sabemos qué mide esta fecha, así que no la usamos para nada.

En las métricas de calidad, la consistencia de ventas baja a 50% solo por esta regla. Damos también la cifra sin ella: 100%.

### 2. Campañas marcadas como convertidas sin una compra que lo confirme

**Qué pasa:** hay 797 envíos de campaña marcados como convertidos. Los datos no dicen qué compra generó cada campaña, así que buscamos una compra del mismo cliente en los 30 días siguientes al envío. Solo la encontramos en 179 casos. En otros 102, la única compra cercana es anterior al envío.

**Qué hicimos:**
- Para comparar tasas de conversión entre tipos de campaña, canales y segmentos, usamos la marca de conversión tal como viene.
- Para calcular cuánto dinero trajo una campaña (y su retorno), solo contamos las 179 conversiones con compra confirmada.

**Por qué:** la marca de conversión es lo que registra la empresa. El porcentaje de conversiones confirmadas es casi igual en 2023 y 2024 (22% y 23%), así que la tendencia sigue siendo válida. Pero varía entre tipos de campaña: 17% en redes sociales y 25% en emails. Por eso, en A4, las diferencias pequeñas entre tipos de campaña no son concluyentes.

Esto hay que mencionarlo como limitación en la presentación.

### 3. Ventas por debajo del costo

**Qué pasa:** en 711 ventas, el cliente pagó menos de lo que le costó el producto a la empresa.

**Qué hicimos:** las conservamos y las marcamos.

**Por qué:** no es un error. 633 son de Electrónica, la categoría con menos margen: un producto típico de Electrónica deja 18,6% de su precio de lista. Con descuentos de entre 9% y 34,5%, la venta termina en pérdida. Es un hallazgo para A2.

### 4. Qué mide el segmento del cliente

**Qué pasa:** el segmento que trae el archivo es una franja del número de compras del cliente en los **24 meses completos**: "Inactivo" tiene 0 o 1 compra, "Nuevo" hasta 3, "Esporádico" hasta 6, y "Frecuente" (1 a 24) y "Premium" (4 a 34) tienen más. Coincide con el comportamiento en frecuencia, pero no en recencia: 108 clientes "Inactivo" compraron en los últimos 90 días, y muchos "Esporádico" y "Nuevo" llevan más de 180 días sin comprar.

Como el segmento se asignó mirando lo que el cliente hizo hasta el final de los datos, es un **resultado** del comportamiento, no algo que se supiera de antemano.

**Qué hicimos:** usamos el segmento original solo para **describir** (el enunciado pide resultados por segmento), nunca para **predecir**. Decir "los Inactivo nunca vuelven" sería una tautología: se llaman Inactivo justamente por no haber vuelto. Para predecir (por ejemplo, la probabilidad de que un cliente vuelva, en A3) usamos solo datos conocidos en la fecha de corte. Además agregamos un segundo segmento, calculado según cómo compra cada cliente en realidad:

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

### 5. Clientes que nunca compraron

**Qué pasa:** 392 clientes no tienen ninguna compra.

**Qué hicimos:** los conservamos y los marcamos. No entran en el cálculo del valor del cliente ni en el de clientes perdidos, pero sí en el análisis de campañas.

**Por qué:** no se puede perder a un cliente que nunca compró. Pero 242 de ellos reciben campañas, y eso cuenta para medir si el marketing funciona.

### 6. Tiempos de respuesta muy altos en atención al cliente

**Qué pasa:** 352 contactos tardaron más de 48,9 horas en recibir respuesta, y 15 tardaron más de una semana. Las 48,9 horas son el límite a partir del cual un valor se considera fuera de lo normal en estos datos (regla del rango intercuartílico).

**Qué hicimos:** los conservamos y los marcamos. En los resúmenes usamos la mediana (el valor del medio), que no se deja arrastrar por los casos extremos.

**Por qué:** una respuesta lenta no es un error de los datos. Es justo lo que queremos estudiar en A3.

### 7. Ventas con montos muy altos

**Qué pasa:** si buscamos montos fuera de lo normal mirando todas las ventas juntas, salen 4.138. Dos tercios (2.672) son de Electrónica.

**Qué hicimos:** buscamos los montos fuera de lo normal dentro de cada categoría (salen 3.420) y los marcamos. No eliminamos ninguno.

**Por qué:** Electrónica sale "fuera de lo normal" solo porque sus productos son más caros. Es más justo comparar cada venta con las de su propia categoría. Y aun así son ventas reales, con montos que cuadran.

### 8. Devoluciones fechadas el último día

**Qué pasa:** el 31 de diciembre de 2024 tiene 158 devoluciones; un día normal tiene 9. Son compras de diciembre (mediana: 8 días antes) cuya devolución llegó después del cierre de los datos y quedó fechada el último día disponible.

**Qué hicimos:** las conservamos y las marcamos (`fecha_dev_recortada`). Las tasas de devolución las medimos por **fecha de compra**, no de devolución.

**Por qué:** por fecha de devolución, estas 158 hacen que el último trimestre suba de 13,3% a 15,8%. Parece un empeoramiento, pero es un efecto del corte de los datos. Por fecha de compra, cada devolución cuenta en el trimestre de su venta y el corte no la mueve.

## Columnas que agrega `cargar_limpio()`

| Tabla | Columnas nuevas |
|---|---|
| transacciones | `categoria`, `subcategoria`, `costo_total`, `margen_bruto`, `bajo_costo`, `outlier_cat`, `devuelta`, `mes`, `trimestre` |
| clientes | `primera_compra`, `ultima_compra`, `n_compras`, `gasto_total`, `margen_total`, `sin_compras`, `dias_sin_comprar`, `segmento_rfm` |
| devoluciones | `fecha_compra`, `producto_id`, `categoria`, `canal`, `monto_neto`, `dias_a_devolucion`, `fecha_dev_recortada` |
| interacciones_crm | `respuesta_atipica` |
| campanas_marketing | `compra_en_ventana`, `conversion_respaldada`, `monto_respaldado` |

Los umbrales (30, 90 y 180 días, y 8 compras) están al principio de `src/carga.py`. Si el profesor pide otros valores, se cambian ahí.
