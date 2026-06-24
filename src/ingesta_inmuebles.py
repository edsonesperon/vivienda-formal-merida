"""Carga del dataset de listados de Inmuebles24 (proyecto previo) a un DataFrame
tipado.

`propiedades.csv` trae 15 columnas tal como se capturaron del anuncio. La carga
es **fiel**: no filtra filas ni deriva variables (eso queda para fases
posteriores); solo lee el CSV y asigna tipos correctos —fecha, booleano de
preventa y enteros nullables donde hay faltantes—.

Recordatorio: `precio` es **precio de lista**, no de cierre (ver
`docs/decisiones.md`).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def cargar_inmuebles(ruta: str | Path) -> pd.DataFrame:
    """Carga ``propiedades.csv`` y devuelve un DataFrame tipado.

    Transformaciones aplicadas:

    - ``fecha_registro`` -> ``datetime``
    - ``es_preventa`` ("si"/"no") -> booleano nullable
    - ``estacionamientos`` y ``antigüedad`` -> entero nullable (``Int64``;
      ambos tienen faltantes y por eso pandas los lee como flotantes)

    Parameters
    ----------
    ruta : str | Path
        Ruta al archivo ``propiedades.csv``.

    Returns
    -------
    pd.DataFrame
        Listados con tipos corregidos. Una fila por anuncio.
    """
    df = pd.read_csv(ruta)

    df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])
    df["es_preventa"] = (
        df["es_preventa"].map({"si": True, "no": False}).astype("boolean")
    )
    for col in ("estacionamientos", "antigüedad"):
        df[col] = df[col].astype("Int64")

    return df
