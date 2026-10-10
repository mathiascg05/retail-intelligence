# Retail Intelligence – RetailVenture C.A.

Proyecto 01 de Tópicos Especiales para la Gestión de Datos (UCAB, prof. Armen Djenanian).

RetailVenture es una cadena de tiendas que está perdiendo margen. Tenemos 24 meses de sus datos: ventas, clientes, productos, devoluciones, atención al cliente y campañas de marketing. Nuestro trabajo es explicar qué está pasando, por qué, y qué debería hacer la empresa.

El enunciado completo está en `data/raw/Proyecto_01_Retail_Intelligence.pdf`.

**Entrega y defensa: semana 6.** El PDF dice semana 15, pero el profesor cambió la fecha en clase.

## Equipo

| Fase | Tema | Responsable | Estado |
|---|---|---|---|
| A1 | Calidad y limpieza de los datos | Mathias Carstens | en revisión (PR #2) |
| A2 | Qué productos, clientes y canales dejan más margen | Mikel Muñoz | en revisión (PR #3) |
| A3 | Dónde se pierde dinero: devoluciones, clientes que se van, quejas | Federico Celis | pendiente |
| A4 | Qué tan bien funcionan las campañas de marketing | Fernando Álvarez | pendiente |
| A5 | Historia final, gráficos y presentación | Leonardo Reyes | pendiente |

## Calendario

| Semana | Qué hacemos |
|---|---|
| 2 | Cerrar A1 |
| 3 y 4 | A2, A3 y A4 al mismo tiempo |
| 5 | A5. El viernes se congelan las cifras |
| 6 | Ensayos, entrega y defensa |

## Qué hay en cada carpeta

| Carpeta o archivo | Contenido |
|---|---|
| `data/raw/` | datos originales y enunciado. No se modifican |
| `data/clean/` | datos limpios. Se generan solos y no se suben al repo |
| `src/carga.py` | carga y limpieza de los datos |
| `notebooks/` | un notebook por fase |
| `docs/modelo.md` | cómo se relacionan las tablas |
| `figures/` | gráficos para la presentación |
| `DECISIONES.md` | qué hicimos con cada problema de los datos y por qué |
| `BITACORA.md` | cómo usamos la IA (lo pide la rúbrica) |
| `FEEDBACK_PROFESOR.md` | lo que hablamos con el profesor |

## Ver los resultados

Abre cualquier notebook de la carpeta `notebooks/` aquí en GitHub. Se ven los textos, las tablas y los gráficos, sin instalar nada. Los notebooks se suben ya ejecutados.

## Correrlo en tu computadora

La primera vez, crea el entorno e instala las librerías:

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Después, abre un notebook de dos formas:

- **VS Code:** abre la carpeta del proyecto, abre el notebook, elige el entorno `.venv` arriba a la derecha ("Select Kernel") y pulsa "Run All".
- **Jupyter:** con el entorno activado, corre `jupyter lab` y abre el notebook en el navegador. Menú "Run" → "Run All Cells".

Antes de subir un notebook, ejecútalo completo (Run All) para que los resultados que se ven en GitHub estén al día.

## Cómo trabajamos

- En los notebooks, los datos se cargan con `from src.carga import cargar_limpio`. Nadie lee los CSV por su cuenta. Así todos usamos exactamente los mismos datos.
- Cada fase se trabaja en su propia rama (`a2-rentabilidad`, `a3-fugas`, …).
- Para pasar a `main` se abre un PR, y otra persona del equipo lo revisa antes de aprobarlo.
