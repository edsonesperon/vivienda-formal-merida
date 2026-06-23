"""Parseo de los pivotes HTML del cubo SNIIV (Infonavit, Sedatu) a formato tidy.

Los archivos del cubo se descargan con extensión ``.xls`` pero en realidad son
tablas HTML (PivotTable.js). Cada celda numérica lleva el valor crudo en el
atributo ``data-value`` —sin separador de miles ni símbolo de moneda—, que es
lo que leemos. La fila y la columna de "Total" se ignoran: se recalculan aguas
abajo si hacen falta.

Uso típico
----------
>>> from ingesta_sniiv import cargar_sniiv
>>> df = cargar_sniiv("data/raw/infonavit_acciones-....xls",
...                    "data/raw/infonavit_monto-....xls")
>>> df.columns.tolist()
['anio', 'segmento', 'acciones', 'monto']
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


def _leer_pivote(ruta: str | Path) -> pd.DataFrame:
    """Lee un ``.xls``-HTML del cubo y devuelve la matriz año × segmento.

    Parameters
    ----------
    ruta : str | Path
        Ruta al archivo descargado del cubo (una sola métrica).

    Returns
    -------
    pd.DataFrame
        Índice = ``anio`` (int, ascendente); columnas = segmento de valor;
        valores = ``data-value`` (float). Excluye la fila/columna de totales.
    """
    html = Path(ruta).read_bytes().decode("latin-1")
    soup = BeautifulSoup(html, "html.parser")

    segmentos = [th.get_text(strip=True) for th in soup.select("th.pvtColLabel")]
    if not segmentos:
        raise ValueError(f"No se encontraron columnas de segmento en {ruta!s}")

    filas: dict[int, dict[str, float]] = {}
    for tr in soup.select("tbody tr"):
        etiqueta = tr.find("th", class_="pvtRowLabel")
        if etiqueta is None:  # fila de totales (no tiene pvtRowLabel)
            continue
        anio = int(etiqueta.get_text(strip=True))
        valores = [float(td["data-value"]) for td in tr.select("td.pvtVal")]
        filas[anio] = dict(zip(segmentos, valores))

    matriz = pd.DataFrame.from_dict(filas, orient="index").sort_index()
    matriz.index.name = "anio"
    matriz.columns.name = "segmento"
    return matriz


def cargar_metrica(ruta: str | Path, metrica: str) -> pd.DataFrame:
    """Carga un archivo del cubo y lo devuelve en formato tidy (largo).

    Parameters
    ----------
    ruta : str | Path
        Ruta al ``.xls``-HTML (contiene una sola métrica).
    metrica : str
        Nombre de la métrica del archivo: ``"acciones"`` o ``"monto"``.

    Returns
    -------
    pd.DataFrame
        Columnas ``['anio', 'segmento', <metrica>]``; una fila por año × segmento.
    """
    matriz = _leer_pivote(ruta)
    return (
        matriz.reset_index()
        .melt(id_vars="anio", var_name="segmento", value_name=metrica)
        .sort_values(["anio", "segmento"])
        .reset_index(drop=True)
    )


def cargar_sniiv(ruta_acciones: str | Path, ruta_monto: str | Path) -> pd.DataFrame:
    """Une los archivos de acciones y monto en un solo DataFrame tidy.

    Parameters
    ----------
    ruta_acciones : str | Path
        ``.xls``-HTML con la métrica de acciones (conteo de créditos).
    ruta_monto : str | Path
        ``.xls``-HTML con la métrica de monto (pesos de crédito financiado).

    Returns
    -------
    pd.DataFrame
        Columnas ``['anio', 'segmento', 'acciones', 'monto']``; una fila por
        año × segmento, ordenada por año y segmento.
    """
    acciones = cargar_metrica(ruta_acciones, "acciones")
    monto = cargar_metrica(ruta_monto, "monto")
    df = (
        acciones.merge(monto, on=["anio", "segmento"], how="outer")
        .sort_values(["anio", "segmento"])
        .reset_index(drop=True)
    )
    df["acciones"] = df["acciones"].astype("Int64")  # conteo de créditos
    return df
