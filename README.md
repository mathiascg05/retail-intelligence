# Retail Intelligence – RetailVenture C.A.

Proyecto 01 de Tópicos Especiales para la Gestión de Datos (UCAB, prof. Armen Djenanian).

Tenemos 24 meses de datos de una cadena de retail (ventas, clientes, productos, devoluciones, CRM y campañas) y hay que explicar por qué caen los márgenes y qué hacer al respecto. El enunciado completo está en `data/raw/Proyecto_01_Retail_Intelligence.pdf`.

Entrega y defensa: **semana 6** (el PDF dice semana 15, pero el profesor lo movió en clase).

## Fases y responsables

| Fase | Qué es | Responsable | Estado |
|---|---|---|---|
| A1 | Calidad de datos y limpieza | Mathias Carstens | lista |
| A2 | Rentabilidad y comportamiento de compra | Mikel Muñoz | pendiente |
| A3 | Fugas de ingresos (devoluciones, churn, CRM) | Federico Celis | pendiente |
| A4 | Marketing (conversión, descuentos, ROI) | Fernando Álvarez | pendiente |
| A5 | Relato, visualizaciones y presentación | Leonardo Reyes | pendiente |

Plan: A1 en la semana 2; A2, A3 y A4 en paralelo en las semanas 3 y 4; A5 en la semana 5 (el viernes congelamos las cifras); la semana 6 es para ensayar.

## Organización del repo

```
data/raw/      archivos originales (no se tocan)
data/clean/    tablas limpias en parquet (se generan solas, no se suben)
src/carga.py   carga y limpieza de datos
notebooks/     un notebook por fase
docs/          modelo relacional
figures/       gráficos para la presentación
```

- `DECISIONES.md`: qué hicimos con cada problema de los datos y por qué.
- `BITACORA.md`: uso de IA (lo pide la rúbrica).
- `FEEDBACK_PROFESOR.md`: lo que vamos hablando con el profesor.

## Para correrlo

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
nbstripout --install --attributes .gitattributes
jupyter lab
```

En los notebooks los datos se cargan con `from src.carga import cargar_limpio` en vez de leer los CSV directamente, para que todos trabajemos con las mismas tablas. Cada fase va en su propia rama (`a2-rentabilidad`, `a3-fugas`, …) y entra a `main` con un PR que revisa otra persona del equipo.
