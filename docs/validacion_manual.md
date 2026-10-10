# Validación a mano de los montos y márgenes

La bitácora (22 de septiembre) dice que alguien del equipo tiene que comprobar a mano que los montos y márgenes de los datos cuadran. Esta hoja es para hacerlo. **La tiene que completar una persona del equipo, no la IA**, y anotar su nombre en `BITACORA.md`.

Las filas se eligieron al azar (`random_state=20261009`) de `data/raw/transacciones.csv` y `data/raw/productos.csv`. Abre los CSV en Excel, busca cada fila por su código y comprueba que los datos de la tabla coinciden. Después haz las cuentas con calculadora.

## 1. Ventas

Fórmulas:
- **Monto neto** = cantidad × precio unitario × (1 − descuento). Compáralo con la columna `monto_neto` del CSV.
- **Margen bruto** = monto neto − costo × cantidad.

| transaccion_id | producto_id | cantidad | precio unitario | descuento | costo | monto neto (tu cuenta) | ¿coincide con el CSV? | margen bruto (tu cuenta) |
|---|---|---|---|---|---|---|---|---|
| TRX0029187 | PRD0213 | 1 | 64.0 | 0.049 | 37.7 | | | |
| TRX0033609 | PRD0038 | 2 | 476.98 | 0.053 | 406.39 | | | |
| TRX0002325 | PRD0029 | 1 | 372.58 | 0.085 | 286.14 | | | |
| TRX0014423 | PRD0304 | 2 | 13.56 | 0.114 | 9.74 | | | |
| TRX0010592 | PRD0001 | 1 | 1186.64 | 0.143 | 936.26 | | | |

## 2. Productos

Fórmula: **margen bruto %** = (precio de lista − costo) / precio de lista × 100. Compáralo con la columna `margen_bruto_pct`.

| producto_id | costo | precio de lista | margen_bruto_pct (CSV) | tu cuenta | ¿coincide (±0,15)? |
|---|---|---|---|---|---|
| PRD0213 | 37.7 | 64.0 | 41.1 | | |
| PRD0038 | 406.39 | 476.98 | 14.8 | | |
| PRD0029 | 286.14 | 372.58 | 23.2 | | |
| PRD0304 | 9.74 | 13.56 | 28.2 | | |
| PRD0001 | 936.26 | 1186.64 | 21.1 | | |

## 3. Cuando termines

Anota en `BITACORA.md`, en la entrada del 22 de septiembre, debajo de "Falta validar":
- quién lo hizo y en qué fecha;
- si todo cuadró, o qué fila no cuadró y por cuánto.
