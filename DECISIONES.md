# Decisiones de limpieza y metodología

Estado: **P** = propuesta · **V** = validada con el profesor · **A** = aplicada en `carga.py`

## Resumen de la auditoría inicial (notebooks/01_calidad.ipynb)

- 0 nulos y 0 duplicados (exactos y por ID) en las 6 tablas.
- 0 claves huérfanas; montos, precios y márgenes cuadran aritméticamente en el 100% de las filas.
- 318 productos (el enunciado dice 320).

## Decisiones pendientes

| # | Problema | Registros afectados | Propuesta | Justificación | Estado |
|---|---|---|---|---|---|
| 1 | Transacciones anteriores a `fecha_registro` | 24.972 trx (50%), 5.803 clientes | _por decidir_ | Ocurre por igual en los 3 canales; correlación registro vs 1ª compra = 0,009 | P |
| 2 | Conversiones sin compra que las respalde | 618 de 797 (ventana 30 d) | _por decidir_ | No existe llave campaña→transacción | P |
| 3 | Ventas con precio neto bajo costo | 711 trx (633 Electrónica) | Conservar: es un hallazgo de negocio, no un error | Descuentos del 9% al 34,5% | P |
| 4 | Segmento "Inactivo" con compras recientes | 108 clientes | _por decidir_ | Segmento declarado ≠ comportamiento | P |
| 5 | Clientes sin transacciones | 392 | _por decidir_ | Afectan denominadores de CLV y churn | P |
| 6 | Outliers de `tiempo_respuesta_hrs` | 352 > 48,9 h (IQR); 15 > 168 h | _por decidir_ | — | P |
| 7 | "Outliers" de `monto_neto` por IQR global | 4.138 | No tratar con IQR global; usar reglas por categoría | Sesgo natural por precio de Electrónica | P |
