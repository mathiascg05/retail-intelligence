# Decisiones sobre los datos

Todo sale de `notebooks/01_calidad.ipynb` y está implementado en `src/carga.py` (`cargar_limpio`).

Criterio general: **no borramos filas**. Los datos no traen nulos, duplicados ni claves huérfanas, así que los problemas que hay son de interpretación, no de formato. Los casos raros se marcan con una columna booleana y cada análisis decide qué hacer con ellos.

## Lo que encontramos

- 0 celdas vacías y 0 duplicados en las 6 tablas. Todas las claves foráneas existen.
- Montos, precios y márgenes cuadran aritméticamente en el 100% de las filas.
- `genero = "No especificado"` en 433 clientes: es un nulo disfrazado.
- 318 productos (el enunciado dice 320).
- Las cifras del contexto del caso no aparecen en los datos: el ticket cae 1,9% (no 8%), las devoluciones se mantienen entre 13,0% y 13,8% (no suben al 14%) y la conversión cae de 11,3% a 5,6% (no de 22% a 11%). Hay un tercer canal, `app_movil`, que el enunciado no menciona.

## Decisiones

**1. Compras anteriores a `fecha_registro`** (24.972 transacciones, 50%)
Las dejamos. Pasa igual en los tres canales (49–50%) y la fecha de registro no tiene relación con la primera compra (correlación 0,009). La empresa tiene 12 años, pero todos los registros son de 2023–2024, así que lo más razonable es que `fecha_registro` sea el alta en la plataforma actual, no el inicio de la relación. No la usamos para medir antigüedad; para eso usamos la fecha de la primera compra (`clientes.primera_compra`).

**2. Conversiones de campaña sin compra que las respalde** (618 de 797)
No hay ninguna llave entre campaña y transacción. Buscamos una compra del mismo cliente en los 30 días siguientes al envío: solo aparece en 179 casos, y en 102 la única compra cercana es anterior al envío (el caso de "campañas con fechas posteriores a la compra" del enunciado).
- Para **tasas de conversión** (comparar tipos, canales y segmentos) usamos `convertido` tal cual, porque es lo que registra la empresa. El % de conversiones respaldadas es parecido entre años (22–23%) y entre tipos de campaña, aunque no idéntico: va de 17% (`social_ads`) a 25% (emails). Por eso las diferencias pequeñas entre tipos hay que tomarlas con cuidado en A4.
- Para **montos y ROI** solo contamos las conversiones con compra en la ventana (`conversion_respaldada`, `monto_respaldado`). Esto hay que decirlo como limitación en la presentación.

**3. Ventas por debajo del costo** (711)
Las dejamos y las marcamos (`bajo_costo`). 633 son de Electrónica, que tiene el margen de lista más bajo (18,6%): con descuentos entre 9% y 34,5% el margen se vuelve negativo. No es un error, es un hallazgo para A2.

**4. Segmento declarado vs comportamiento** (108 "Inactivos" con compras en los últimos 90 días)
Dejamos `segmento` como viene, porque el enunciado pide el análisis por segmento. Agregamos `segmento_rfm`, calculado con reglas simples sobre el comportamiento, para contrastar:
- Sin compras: nunca compró.
- Inactivo: más de 180 días sin comprar (el p90 del tiempo entre compras es 162 días).
- Premium: gasto total en el 10% más alto.
- Frecuente: 8 compras o más.
- Nuevo: primera compra en los últimos 90 días.
- Esporádico: el resto.

**5. Clientes sin compras** (392)
Los dejamos con `sin_compras = True`. No entran en CLV ni en churn (no se puede perder a quien nunca compró), pero sí en el análisis de campañas: 242 de los 392 reciben campañas. Por segmento declarado, 255 son "Inactivo", 94 "Nuevo" y 43 "Esporádico".

**6. Tiempos de respuesta del CRM muy altos** (352 por encima de 48,9 h según IQR; 15 de más de una semana)
Los dejamos y los marcamos (`respuesta_atipica`). Un tiempo de respuesta alto es justamente lo que queremos medir en A3, no ruido. En los resúmenes usamos la mediana.

**7. Montos de venta "atípicos"**
Con un IQR global salían 4.138 outliers, dos tercios de ellos (2.672) de Electrónica, simplemente porque es la categoría más cara. Calculamos el IQR por categoría (`outlier_cat`, 3.420 filas) y no eliminamos nada: son ventas reales con montos coherentes.

## Columnas que agrega `cargar_limpio`

| Tabla | Columnas nuevas |
|---|---|
| transacciones | `categoria`, `subcategoria`, `costo_total`, `margen_bruto`, `bajo_costo`, `outlier_cat`, `devuelta`, `mes`, `trimestre` |
| clientes | `primera_compra`, `ultima_compra`, `n_compras`, `gasto_total`, `margen_total`, `sin_compras`, `dias_sin_comprar`, `segmento_rfm` |
| devoluciones | `fecha_compra`, `producto_id`, `categoria`, `canal`, `monto_neto`, `dias_a_devolucion` |
| interacciones_crm | `respuesta_atipica` |
| campanas_marketing | `compra_en_ventana`, `conversion_respaldada`, `monto_respaldado` |

Los umbrales (30, 180, 90 días y 8 compras) están arriba en `src/carga.py`, para cambiarlos en un solo lugar si el profesor pide otra cosa.
