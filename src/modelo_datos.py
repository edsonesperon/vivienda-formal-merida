"""Ensamblado del modelo de datos en una base SQLite ligera.

Escribe tres tablas normalizadas para el análisis de la Fase 4:

- ``sniiv``:          anio, segmento, acciones, monto (originación Infonavit).
- ``segmento_valor``: anio, segmento, rango de valor en pesos (mapeo por año).
- ``inmuebles``:      listados de Inmuebles24 (oferta).

El enriquecimiento (créditos + rango de valor) se resuelve por consulta, con un
JOIN por ``anio`` + ``segmento``. "No disponible" no tiene rango y queda con
nulos, como se decidió en ``docs/decisiones.md``.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

TABLAS = ("sniiv", "segmento_valor", "inmuebles")


def construir_sqlite(
    ruta_db: str | Path,
    sniiv: pd.DataFrame,
    segmento_valor: pd.DataFrame,
    inmuebles: pd.DataFrame,
) -> Path:
    """Escribe las tres tablas en una base SQLite (reemplaza si existen).

    Parameters
    ----------
    ruta_db : str | Path
        Ruta del archivo ``.db`` a crear (p. ej. ``data/processed/vivienda.db``).
    sniiv, segmento_valor, inmuebles : pd.DataFrame
        Las tres tablas ya limpias.

    Returns
    -------
    Path
        La ruta de la base creada.
    """
    ruta_db = Path(ruta_db)
    ruta_db.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(ruta_db)
    try:
        sniiv.to_sql("sniiv", con, if_exists="replace", index=False)
        segmento_valor.to_sql("segmento_valor", con, if_exists="replace", index=False)
        inmuebles.to_sql("inmuebles", con, if_exists="replace", index=False)
    finally:
        con.close()

    return ruta_db
