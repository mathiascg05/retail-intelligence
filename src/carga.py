"""Carga de datos del proyecto.

Los notebooks no leen los CSV por su cuenta: usan cargar_crudo() para ver los
datos tal como vinieron y cargar_limpio() para el análisis (A2 en adelante).
Así todas las cifras salen de la misma versión de los datos.

Lo que hace cargar_limpio() está explicado en DECISIONES.md. Resumen: no se
borra ninguna fila; los casos raros se marcan con columnas booleanas para que
cada análisis decida si los usa o no.
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

# Umbrales (ver DECISIONES.md)
VENTANA_CONVERSION = 30   # días después del envío para aceptar una compra como respaldo (#2)
DIAS_INACTIVO = 180       # ~p90 del tiempo entre compras (162 d), redondeado (#4)
DIAS_NUEVO = 90           # primera compra en los últimos 90 días (#4)
COMPRAS_FRECUENTE = 8     # (#4)


def cargar_crudo(nombre=None):
    """Una tabla (si se pasa nombre) o un dict con las 6, con las fechas ya convertidas."""
    if nombre is not None:
        return pd.read_csv(RAW / f"{nombre}.csv", parse_dates=FECHAS[nombre])
    return {n: cargar_crudo(n) for n in TABLAS}


def _iqr_alto(s):
    q1, q3 = s.quantile([0.25, 0.75])
    return s > q3 + 1.5 * (q3 - q1)


def _limpiar(d):
    cli = d["clientes"].copy()
    trx = d["transacciones"].copy()
    prd = d["productos"].copy()
    dev = d["devoluciones"].copy()
    crm = d["interacciones_crm"].copy()
    cam = d["campanas_marketing"].copy()

    # Hoy no hay duplicados (esto elimina 0 filas); está por si el profesor cambia los archivos
    for t, id_ in [(cli, "cliente_id"), (trx, "transaccion_id"), (prd, "producto_id"),
                   (dev, "devolucion_id"), (crm, "interaccion_id"), (cam, "campana_id")]:
        t.drop_duplicates(subset=id_, inplace=True)

    # --- transacciones: margen por línea y marcas (#3, #7)
    trx = trx.merge(prd[["producto_id", "categoria", "subcategoria", "costo"]], on="producto_id", how="left")
    trx["costo_total"] = (trx["costo"] * trx["cantidad"]).round(2)
    trx["margen_bruto"] = trx["monto_neto"] - trx["costo_total"]
    trx["bajo_costo"] = trx["margen_bruto"] < 0
    trx["outlier_cat"] = trx.groupby("categoria")["monto_neto"].transform(_iqr_alto)
    trx["devuelta"] = trx["transaccion_id"].isin(dev["transaccion_id"])
    trx["mes"] = trx["fecha"].dt.to_period("M").dt.to_timestamp()
    trx["trimestre"] = trx["fecha"].dt.to_period("Q").astype(str)
    trx = trx.drop(columns="costo")

    # --- clientes: comportamiento real además del segmento declarado (#1, #4, #5)
    fin = trx["fecha"].max()
    resumen = trx.groupby("cliente_id").agg(
        primera_compra=("fecha", "min"),
        ultima_compra=("fecha", "max"),
        n_compras=("transaccion_id", "size"),
        gasto_total=("monto_neto", "sum"),
        margen_total=("margen_bruto", "sum"),
    )
    cli = cli.merge(resumen, on="cliente_id", how="left")
    cli["sin_compras"] = cli["n_compras"].isna()
    cli["n_compras"] = cli["n_compras"].fillna(0).astype(int)
    cli[["gasto_total", "margen_total"]] = cli[["gasto_total", "margen_total"]].fillna(0)
    cli["dias_sin_comprar"] = (fin - cli["ultima_compra"]).dt.days

    corte_premium = cli.loc[~cli["sin_compras"], "gasto_total"].quantile(0.9)
    seg = pd.Series("Esporádico", index=cli.index)
    seg[(fin - cli["primera_compra"]).dt.days <= DIAS_NUEVO] = "Nuevo"
    seg[cli["n_compras"] >= COMPRAS_FRECUENTE] = "Frecuente"
    seg[cli["gasto_total"] >= corte_premium] = "Premium"
    seg[cli["dias_sin_comprar"] > DIAS_INACTIVO] = "Inactivo"
    seg[cli["sin_compras"]] = "Sin compras"
    cli["segmento_rfm"] = seg

    # --- devoluciones
    dev = dev.merge(trx[["transaccion_id", "fecha", "producto_id", "categoria", "canal", "monto_neto"]],
                    on="transaccion_id", how="left").rename(columns={"fecha": "fecha_compra"})
    dev["dias_a_devolucion"] = (dev["fecha_devolucion"] - dev["fecha_compra"]).dt.days
    # #8: el último día acumula las devoluciones que en realidad pasaron después del cierre
    dev["fecha_dev_recortada"] = dev["fecha_devolucion"] == fin

    # --- CRM (#6)
    crm["respuesta_atipica"] = _iqr_alto(crm["tiempo_respuesta_hrs"])

    # --- campañas (#2): ¿hay una compra del cliente en los 30 días siguientes al envío?
    pares = cam[["campana_id", "cliente_id", "fecha_envio"]].merge(
        trx[["cliente_id", "fecha", "monto_neto"]], on="cliente_id")
    dias = (pares["fecha"] - pares["fecha_envio"]).dt.days
    pares = pares[dias.between(0, VENTANA_CONVERSION)].sort_values("fecha")
    primera = pares.drop_duplicates("campana_id").set_index("campana_id")
    cam["compra_en_ventana"] = cam["campana_id"].isin(primera.index)
    cam["conversion_respaldada"] = (cam["convertido"] == 1) & cam["compra_en_ventana"]
    cam["monto_respaldado"] = cam["campana_id"].map(primera["monto_neto"]).where(cam["conversion_respaldada"], 0.0)

    return {"clientes": cli, "transacciones": trx, "productos": prd, "devoluciones": dev,
            "interacciones_crm": crm, "campanas_marketing": cam}


def _cache_viejo():
    """True si falta algún parquet o si carga.py o los CSV cambiaron después de generarlo
    (por ejemplo, al cambiar de rama)."""
    archivos = [CLEAN / f"{n}.parquet" for n in TABLAS]
    if not all(a.exists() for a in archivos):
        return True
    generado = min(a.stat().st_mtime for a in archivos)
    fuentes = [Path(__file__)] + [RAW / f"{n}.csv" for n in TABLAS]
    return any(f.stat().st_mtime > generado for f in fuentes)


def cargar_limpio(nombre=None, recalcular=False):
    """Tablas con las decisiones de DECISIONES.md aplicadas.

    La primera vez se calculan y se guardan en data/clean/ como parquet; después
    se leen de ahí. Si cambia este archivo o algún CSV, se vuelven a calcular solas.
    """
    if recalcular or _cache_viejo():
        CLEAN.mkdir(exist_ok=True)
        for n, t in _limpiar(cargar_crudo()).items():
            t.to_parquet(CLEAN / f"{n}.parquet", index=False)
    if nombre is not None:
        return pd.read_parquet(CLEAN / f"{nombre}.parquet")
    return {n: pd.read_parquet(CLEAN / f"{n}.parquet") for n in TABLAS}
