# Dashboard de Power BI

El enunciado pide un dashboard con **máximo 10 visualizaciones**, cada una con un título que diga el hallazgo (no que describa el gráfico). Aquí está todo lo necesario para armarlo: qué archivos cargar, cómo relacionarlos, las medidas DAX y las 10 visualizaciones.

Todas las cifras salen de los notebooks, así que el dashboard y el informe dicen lo mismo.

## 1. Los datos

Todo está en `data/powerbi/`. No hace falta correr Python para armar el dashboard: los archivos están en el repositorio.

| Archivo | Qué es |
|---|---|
| `dim_fecha`, `dim_cliente`, `dim_producto` | Tablas que describen las ventas (esquema estrella, ver `docs/modelo.md`) |
| `fact_ventas`, `fact_devoluciones`, `fact_crm`, `fact_campanas` | Tablas de hechos, ya limpias y con las columnas que agrega `cargar_limpio()` (`DECISIONES.md`) |
| `resultado_*` | Resultados de los notebooks que no se pueden calcular con DAX de forma sencilla (CLV, probabilidad de volver, compras reales tras una campaña, recomendaciones) |

**Si cambian los datos o el código:** desde la raíz del proyecto, `python -m src.powerbi` regenera las tablas dim_* y fact_*. Los `resultado_*` se regeneran al ejecutar los notebooks 02 a 05.

## 2. Cargar en Power BI

1. **Obtener datos → Texto/CSV** y cargar los 17 archivos.
2. **Ojo con los decimales:** los CSV usan punto decimal. Si Power BI está en español, lee `0.25` como 25. Antes de cargar: **Archivo → Opciones → Configuración regional (archivo actual) → Inglés (Estados Unidos)**. Otra opción: en Power Query, "Cambiar tipo → Usando configuración regional".
3. Revisar en Power Query que las columnas de fecha sean de tipo fecha y que `devuelta`, `convertido`, `abierto`, etc. sean números o verdadero/falso.

## 3. Relaciones

En la vista de modelo, todas de uno a varios y con filtro en una sola dirección:

| Desde (uno) | Hacia (varios) | Activa |
|---|---|---|
| `dim_cliente[cliente_id]` | `fact_ventas`, `fact_devoluciones`, `fact_crm`, `fact_campanas`, `resultado_a3_clientes_en_riesgo` | sí |
| `dim_producto[producto_id]` | `fact_ventas[producto_id]`, `fact_devoluciones[producto_id]` | sí |
| `dim_fecha[fecha]` | `fact_ventas[fecha]` | sí |
| `dim_fecha[fecha]` | `fact_devoluciones[fecha_devolucion]`, `fact_crm[fecha]`, `fact_campanas[fecha_envio]` | no (usar `USERELATIONSHIP` si hace falta) |

Las tablas `resultado_*` (salvo la de clientes en riesgo) van sueltas, sin relaciones: ya vienen resumidas.

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
Tasa de devolución = DIVIDE ( CALCULATE ( COUNTROWS ( fact_ventas ), fact_ventas[devuelta] = TRUE () ), COUNTROWS ( fact_ventas ) )
Conversión = AVERAGE ( fact_campanas[convertido] )
```

## 5. Las 10 visualizaciones

El orden sigue el relato del informe: primero dónde se gana y se pierde margen (A2), después dónde se escapa el dinero (A3), qué pasa con el marketing (A4) y qué hacer (A5). Los títulos son los mismos de los gráficos de `figures/`.

| # | Título (insight) | Tipo de gráfico | Datos |
|---|---|---|---|
| 1 | Electrónica es el 44% de las ventas, pero solo el 16% del margen neto | Barras agrupadas horizontales | Eje: `dim_producto[categoria]`. Valores: `% de las ventas`, `% del margen neto` |
| 2 | Un cliente Premium deja 13 veces más margen en 3 años que uno Esporádico | Barras horizontales | `resultado_a2_clv_segmento`: eje `segmento`, valor `CLV 2024 (S1→S2)` |
| 3 | Con más descuento el margen cae de 29% a 7%, pero la gente compra las mismas unidades | Dos gráficos de columnas uno al lado del otro (o columnas + línea) | Eje: `fact_ventas[banda_descuento]` (ordenar por banda). Valores: `Margen bruto %` y `Unidades por compra` |
| 4 | Ropa devuelve el doble que el resto de categorías y Electrónica, 1,7 veces | Barras horizontales con línea de referencia en la media (13,4%) | Eje: `dim_producto[categoria]`. Valor: `Tasa de devolución` |
| 5 | Los Frecuentes y Premium casi siempre vuelven; los 'Inactivo', nunca | Líneas | `resultado_a3_retorno_segmento_tramo`: eje `tramo`, valor `vuelve`, leyenda `segmento` |
| 6 | Los Esporádicos concentran la mayor fuga: 169.772 en 6 meses | Barras horizontales | `resultado_a3_fuga_segmento`: eje `segmento`, valor `ingreso_perdido`; información sobre herramientas: `en_riesgo`, `p_vuelve` |
| 7 | Premium convierte 2,5 veces más que Inactivo; el tipo de campaña casi no importa | Barras horizontales | Eje: `dim_cliente[segmento]`. Valor: `Conversión` |
| 8 | El descuento dobla la conversión registrada, pero no cambia las compras reales | Líneas (dos series) | `resultado_a4_descuento_marcada_vs_real`: eje `descuento_ofrecido`, valores `conversion_marcada` y `compra_despues` |
| 9 | La conversión registrada cae a la mitad en 2024; las compras tras una campaña, no | Líneas (dos series) | `resultado_a4_trimestre`: eje `trimestre`, valores `conversion` y `compra real 30 d` |
| 10 | Cuatro medidas recuperan 237.544 de margen al año, el 11% del margen bruto | Barras horizontales | `resultado_a5_recomendaciones`: eje `qué hacemos`, valor `margen al año (central)`; información sobre herramientas: `ingresos al año (central)`, `desde`, `hasta` |

**Formato:**
- Porcentajes con un decimal y miles con punto (configurar la región del informe en español al terminar, o el formato de cada medida).
- Un solo color de acento para lo que importa en cada gráfico (por ejemplo, Ropa y Electrónica en el 4, Esporádico en el 6) y gris para el resto. Es la misma paleta de `figures/` (acento `#eb6834`, azul `#2a78d6`, gris `#8a8984`).
- Segmentadores (año, canal, segmento) se pueden agregar: no cuentan como visualizaciones. Ojo: los gráficos 2, 5, 6, 8, 9 y 10 usan tablas ya resumidas y no responden a los segmentadores.

**Lo que queda fuera a propósito** (está en el informe, no en el dashboard): las quejas sin resolver (no tienen efecto, `resultado_a3_quejas`) y el ROI por tipo de campaña (ningún tipo es claramente mejor, `resultado_a4_roi_tipo`). Así no se pasa de 10 visualizaciones.
