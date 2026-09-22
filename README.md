# Retail Intelligence — RetailVenture C.A.

Proyecto 01 de **Tópicos Especiales para la Gestión de Datos** (UCAB, Prof. Armen Djenanian).
Análisis exploratorio y storytelling con datos para explicar la caída de márgenes,
el aumento de devoluciones y la pérdida de efectividad del marketing.

**Entrega y defensa: semana 6** (el PDF del enunciado dice semana 15; la fecha real
fue indicada por el profesor — anotar aquí la fuente de la confirmación: ______).

## Equipo y responsabilidades

| Integrante | Dueño de | Segundo de |
|---|---|---|
| Integrante 1 | A1 Calidad de datos + `src/carga.py` (integrador) | A5 |
| Integrante 2 | A2 Rentabilidad | A3 |
| Integrante 3 | A3 Fugas de ingresos | A4 |
| Integrante 4 | A4 Marketing | A2 |
| Integrante 5 | A5 Storytelling + bitácora de IA | A1 |

## Calendario

| Semana | Objetivo |
|---|---|
| 2 | Cerrar A1 e implementar `cargar_limpio()` en `main` |
| 3 | A2, A3 y A4 en paralelo |
| 4 | Terminar A2–A4, revisión cruzada, borrador del relato |
| 5 | A5 completo; **cifras congeladas el viernes** |
| 6 | Ensayos, entrega y defensa |

## Estructura

```
data/raw/        CSV originales + enunciado (NUNCA se modifican)
data/clean/      salidas de A1 (no versionadas, se regeneran)
src/carga.py     única puerta de entrada a los datos
notebooks/       un notebook por fase (01_calidad … 05_visualizaciones)
figures/         gráficos finales para la presentación
DECISIONES.md    decisiones de limpieza y metodológicas
BITACORA.md      bitácora de uso de IA (criterio 5 de la rúbrica)
FEEDBACK_PROFESOR.md  reuniones semanales con el profesor
```

## Cómo empezar

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
nbstripout --install --attributes .gitattributes    # quita las salidas de los notebooks al commitear
jupyter lab
```

## Reglas de trabajo

1. Nadie lee los CSV directamente: siempre `from src.carga import cargar_crudo, cargar_limpio`.
2. Una rama por fase (`a2-rentabilidad`, `a3-fugas`, …). A `main` solo se entra por PR.
3. Cada PR lo revisa **el segundo** de esa fase, que debe poder explicar cada cifra.
4. Cada notebook tiene un solo dueño a la vez; los demás aportan por PR.
5. Toda sugerencia de IA que se use o se descarte se registra en `BITACORA.md` con link al commit.
6. Después del viernes de la semana 5 no cambia ninguna cifra, salvo que sea un error real.
