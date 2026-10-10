# Dashboard de Power BI

El enunciado pide un dashboard con **máximo 10 visualizaciones**, cada una con un título que diga el hallazgo (no que describa el gráfico). Aquí está todo lo necesario para armarlo: qué archivos cargar, cómo relacionarlos, las medidas DAX y las 10 visualizaciones.

Todas las cifras salen de los notebooks, así que el dashboard y el informe dicen lo mismo. Los montos están en unidades monetarias (u. m.): los datos no dicen la moneda.

## 1. Los datos

Todo está en `data/powerbi/`. No hace falta correr Python para armar el dashboard: los archivos están en el repositorio.

| Archivo | Qué es |
|---|---|
| `dim_fecha`, `dim_cliente`, `dim_producto` | Dimensiones: describen quién, qué y cuándo (ver `docs/modelo.md`) |
| `fact_ventas`, `fact_devoluciones`, `fact_crm`, `fact_campanas` | Tablas de hechos, ya limpias y con las columnas que agrega `cargar_limpio()` (`DECISIONES.md`) |
| `resultado_*` | Resultados de los notebooks que no se pueden calcular con DAX de forma sencilla (CLV, probabilidad de volver, compras reales tras una campaña, recomendaciones) |

**Si cambian los datos o el código:** desde la raíz del proyecto, `python -m src.powerbi` regenera las tablas dim_* y fact_*. Los `resultado_*` se regeneran al ejecutar los notebooks 02 a 05, en ese orden (el 05 lee un resultado del 03).

## 2. Cargar en Power BI

1. **Obtener datos → Texto/CSV** y cargar los 22 archivos.
2. **Ojo con los decimales:** los CSV usan punto decimal. Si Power BI está en español, lee `0.25` como 25. Antes de cargar: **Archivo → Opciones → Configuración regional (archivo actual) → Inglés (Estados Unidos)**. Otra opción: en Power Query, "Cambiar tipo → Usando configuración regional".
3. Revisar en Power Query que las columnas de fecha sean de tipo fecha y que `devuelta`, `convertido`, `abierto`, etc. sean números o verdadero/falso.

## 3. Relaciones

Es una constelación de hechos: cuatro tablas de hechos que comparten las dimensiones (ver `docs/modelo.md`). En la vista de modelo, todas de uno a varios y con filtro en una sola dirección:

| Desde (uno) | Hacia (varios) | Activa |
|---|---|---|
| `dim_cliente[cliente_id]` | `fact_ventas`, `fact_devoluciones`, `fact_crm`, `fact_campanas`, `resultado_a3_clientes_en_riesgo` | sí |
| `dim_producto[producto_id]` | `fact_ventas[producto_id]`, `fact_devoluciones[producto_id]` | sí |
| `dim_fecha[fecha]` | `fact_ventas[fecha]` | sí |
| `dim_fecha[fecha]` | `fact_devoluciones[fecha_devolucion]`, `fact_crm[fecha]`, `fact_campanas[fecha_envio]` | no (usar `USERELATIONSHIP` si hace falta) |

Las tablas `resultado_*` (salvo la de clientes en riesgo) van sueltas, sin relaciones: ya vienen resumidas.

`fact_devoluciones` se relaciona directamente con cliente y producto (tiene las dos columnas). Coinciden siempre con las de la venta devuelta, como explica `docs/modelo.md`.

Usar siempre `dim_producto[categoria]` y `dim_cliente[segmento]` en los gráficos, no las columnas repetidas dentro de las tablas de hechos.

## 4. Medidas DAX

Crear una tabla vacía `Medidas` y agregar:

```dax
Ventas = SUM ( fact_ventas[monto_neto] )
Margen bruto = SUM ( fact_ventas[margen_bruto] )
Margen neto = SUM ( fact_ventas[margen_neto] )
Margen bruto % = DIVIDE ( [Margen bruto], [Ventas] )
% de las ventas = DIVIDE ( [Ventas], CALCULATE ( [Ventas], ALL ( dim_producto[categoria] ) ) )
% del margen neto = DIVIDE ( [Margen neto], CALCULATE ( [Margen neto], ALL ( dim_producto[categoria] ) ) )
Unidades por compra = AVERAGE ( fact_ventas[cantidad] )
Descuento medio = AVERAGE ( fact_ventas[descuento] )
Tasa de devolución = DIVIDE ( CALCULATE ( COUNTROWS ( fact_ventas ), fact_ventas[devuelta] = TRUE () ), COUNTROWS ( fact_ventas ) )
```

## 5. Las 10 visualizaciones

**Son 10 objetos visuales, no más.** Un profesor estricto cuenta gráficos, no ideas. Por eso cada visual es un solo objeto de Power BI: los que comparan dos medidas usan el gráfico combinado (columnas + línea) y no dos gráficos.

El orden sigue el relato del informe: **inicio** (qué cambia y qué no), **nudo** (dónde se va el margen, quién se va, qué pasa con el marketing) y **desenlace** (qué hacer). Los títulos son los mismos de los gráficos de `figures/`.

| # | Parte | Título (insight) | Objeto de Power BI | Datos |
|---|---|---|---|---|
| 1 | Inicio | El margen, el ticket y las devoluciones no se mueven en dos años; solo cae la conversión registrada | Gráfico de líneas | `resultado_a5_situacion_trimestre`: eje `trimestre`, valor `índice (2023 T1 = 100)`, leyenda `métrica`. Información sobre herramientas: `valor` |
| 2 | Nudo: margen | Electrónica es el 44% de las ventas, pero solo el 16% del margen neto | Barras agrupadas horizontales | Eje: `dim_producto[categoria]`. Valores: `% de las ventas`, `% del margen neto` |
| 3 | Nudo: margen | Online descuenta el doble (7,5% contra 3,7%) y tiene el menor margen | Gráfico combinado de columnas y líneas | Eje: `fact_ventas[canal]`. Columnas: `Descuento medio`. Línea: `Margen bruto %`. Filtro: año 2024 |
| 4 | Nudo: margen | Con más descuento el margen cae de 29% a 7%, pero la gente compra las mismas unidades | Gráfico combinado de columnas y líneas | Eje: `fact_ventas[banda_descuento]` (ordenar por banda). Columnas: `Margen bruto %`. Línea: `Unidades por compra` |
| 5 | Nudo: clientes | Pasar de 1 a 2–3 compras por semestre multiplica por 4 el valor del cliente en 3 años | Barras horizontales | `resultado_a2_clv_grupos`: eje `grupo`, valor `CLV 2024` |
| 6 | Nudo: fugas | Ropa devuelve el doble que el resto de categorías y Electrónica, 1,7 veces | Barras horizontales con línea de referencia en la media (13,4%) | Eje: `dim_producto[categoria]`. Valor: `Tasa de devolución` |
| 7 | Nudo: fugas | Tras 6 meses sin comprar, vuelve el 37% de quien compró una vez en el último año y el 91% de quien compró de 4 a 6 veces | Gráfico de líneas | `resultado_a3_retorno_compras_tramo`: eje `tramo`, valor `vuelve`, leyenda `compras` (compras en los 12 meses anteriores) |
| 8 | Nudo: fugas | Los Esporádicos recurrentes concentran la mayor fuga: 172.819 en 6 meses | Barras horizontales | `resultado_a3_fuga_segmento`: eje `segmento`, valor `calibrado`; información sobre herramientas: `en_riesgo`, `ingreso_perdido` (sin calibrar) |
| 9 | Nudo: marketing | El descuento dobla la conversión registrada, pero no cambia las compras reales | Gráfico de líneas (dos series) | `resultado_a4_descuento_marcada_vs_real`: eje `descuento_ofrecido`, valores `conversion_marcada` y `compra_despues` |
| 10 | Desenlace | Bajar el descuento online recuperaría 146.161 de margen al año; las otras tres medidas sirven sobre todo para medir | Barras horizontales | `resultado_a5_recomendaciones`: eje `qué hacemos`, valor `margen (central)`; información sobre herramientas: `periodo`, `ingresos (central)`, `desde`, `hasta`. Ojo: R3 es a 6 meses y una sola vez; las demás, al año. Va dicho en la etiqueta |

**Formato:**
- Porcentajes con un decimal y miles con punto (configurar la región del informe en español al terminar, o el formato de cada medida).
- Un solo color de acento para lo que importa en cada gráfico y gris para el resto. Por ejemplo: la conversión en el 1, online en el 3, Ropa y Electrónica en el 6, Esporádico en el 8. Es la misma paleta de `figures/` (acento `#eb6834`, azul `#2a78d6`, gris `#8a8984`).
- En el visual 10, la etiqueta de R3 debe decir "(6 meses, una vez)".

**Segmentadores (año, canal, segmento):** se pueden agregar y no cuentan como visualizaciones.
- **Responden a los filtros:** los visuales 2, 3, 4 y 6, porque se calculan con DAX sobre las tablas de hechos.
- **No responden:** los visuales 1, 5, 7, 8, 9 y 10, porque usan tablas ya resumidas por los notebooks. Hay que decirlo en una nota del dashboard ("cifras calculadas en el análisis; no cambian con los filtros").
- **Si se quiere que el 1 responda a los filtros,** se puede armar con estas medidas en vez de con la tabla resumida, y con `dim_fecha[trimestre]` en el eje:

```dax
Ticket promedio = DIVIDE ( [Ventas], COUNTROWS ( fact_ventas ) )
Índice margen = DIVIDE ( [Margen bruto %], CALCULATE ( [Margen bruto %], REMOVEFILTERS ( dim_fecha ), dim_fecha[anio] = 2023, dim_fecha[trimestre] = 1 ) ) * 100
```

(y lo mismo para el ticket y la tasa de devolución). La conversión depende de `fact_campanas`, que se une a la fecha con una relación inactiva: hay que usar `USERELATIONSHIP`.

**Lo que queda fuera a propósito** (está en el informe, no en el dashboard), para no pasar de 10 visualizaciones:
- **La tabla de pérdidas** (`resultado_a5_tabla_perdidas`): es el eje del informe, pero una tabla también cuenta como visual.
- **Las quejas sin resolver:** no se detecta efecto (`resultado_a3_quejas`).
- **El ROI por tipo de campaña:** son pocas compras y ningún tipo es claramente mejor (`resultado_a4_roi_tipo`, anexo).
- **La caída de la conversión por trimestre** (`resultado_a4_trimestre`): ya aparece en el visual 1, y el visual 9 muestra que no se refleja en las compras.
- **La conversión por segmento:** el segmento del archivo es una franja de compras, así que solo describe a quién le funciona la marca (A1.4).
