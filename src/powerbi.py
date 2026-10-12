"""Datos para el dashboard de Power BI.

Dos tipos de archivos en data/powerbi/:
- El modelo estrella (dim_* y fact_*), que sale de cargar_limpio(). Se genera con
  `python -m src.powerbi` desde la raíz del proyecto.
- Las tablas de resultados (resultado_*), que guarda cada notebook al final con
  guardar(). Son las cifras que no se pueden calcular con DAX de forma sencilla
  (CLV, probabilidad de volver, compras reales tras una campaña...). Así el
  dashboard muestra exactamente lo mismo que los notebooks y el informe.

Cómo cargarlo en Power BI: docs/dashboard.md.
"""
import pandas as pd

from src.carga import RAIZ, cargar_limpio

SALIDA = RAIZ / "data" / "powerbi"


def guardar(df, nombre, index=False):
    """CSV en UTF-8 con BOM (Power BI y Excel leen bien las tildes) y punto decimal."""
    SALIDA.mkdir(parents=True, exist_ok=True)
    df.to_csv(SALIDA / f"{nombre}.csv", index=index, encoding="utf-8-sig")


def exportar_modelo():
    d = cargar_limpio()
    trx = d["transacciones"].copy()
    trx["banda_descuento"] = pd.cut(trx.descuento, [-0.001, 0, 0.05, 0.10, 0.20, 0.35],
                                    labels=["sin descuento", "hasta 5%", "5% a 10%", "10% a 20%", "más de 20%"])
    fechas = pd.date_range(trx.fecha.min(), trx.fecha.max(), freq="D")
    dim_fecha = pd.DataFrame({"fecha": fechas, "anio": fechas.year, "semestre": (fechas.month > 6) + 1,
                              "trimestre": fechas.quarter, "mes": fechas.month})

    guardar(dim_fecha, "dim_fecha")
    guardar(d["clientes"], "dim_cliente")
    guardar(d["productos"], "dim_producto")
    guardar(trx.drop(columns=["mes", "trimestre"]), "fact_ventas")
    guardar(d["devoluciones"], "fact_devoluciones")
    guardar(d["interacciones_crm"], "fact_crm")
    guardar(d["campanas_marketing"], "fact_campanas")


if __name__ == "__main__":
    exportar_modelo()
    print("Modelo exportado en", SALIDA)
