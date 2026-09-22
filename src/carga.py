"""Carga única de datos para todo el proyecto.

REGLA DEL EQUIPO: ningún notebook lee los CSV directamente ni limpia por su cuenta.
Todos usan cargar_crudo() o cargar_limpio() desde aquí, para que las cifras
de A2–A5 salgan siempre de la misma versión de los datos.
"""
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
CLEAN = RAIZ / "data" / "clean"

FECHAS = {
    "clientes": ["fecha_registro"],
    "transacciones": ["fecha"],
    "productos": [],
    "devoluciones": ["fecha_devolucion"],
    "interacciones_crm": ["fecha"],
    "campanas_marketing": ["fecha_envio"],
}
TABLAS = list(FECHAS)


def cargar_crudo(nombre=None):
    """Devuelve un DataFrame (si se pasa nombre) o un dict con las 6 tablas originales, fechas ya convertidas."""
    if nombre is not None:
        return pd.read_csv(RAW / f"{nombre}.csv", parse_dates=FECHAS[nombre])
    return {n: cargar_crudo(n) for n in TABLAS}


def cargar_limpio(nombre=None):
    """Tablas tras aplicar las decisiones de DECISIONES.md.

    PENDIENTE: se implementa al cerrar A1 (semana 2), una vez validadas las
    decisiones con el profesor. Hasta entonces, nadie debe empezar A2–A4.
    """
    raise NotImplementedError("A1 aún no está cerrada: ver DECISIONES.md")
