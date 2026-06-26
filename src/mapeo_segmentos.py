"""Mapeo de los segmentos de vivienda a rangos de valor en pesos, por año.

Los segmentos del SNIIV (económica … residencial plus) son una clasificación
estándar —consenso Infonavit / SHF / CONAVI / AHM— definida en **múltiplos** de
una referencia mensual: salario mínimo hasta 2015 y UMA desde 2016. Como la UMA
sube cada año, la frontera **en pesos** de cada segmento se recorre año con año;
por eso el mapeo es por año, no una tabla fija.

Fuentes de los umbrales (múltiplos)
-----------------------------------
- **200 y 350 UMA — OFICIAL.** Infonavit, Plan Estratégico y Financiero 2026
  (cita INEGI y RUV): económica-popular hasta 200 UMA; tradicional 200–350 UMA.
  Delimitan popular / tradicional / media (el grueso del volumen de Mérida).
- **118, 750 y 1500 — convención RUV/AHM (confianza media).** Afectan económica
  y residencial / residencial plus, segmentos de bajo volumen. El RUV sugiere
  el corte de económica en ~128 (subniveles popular 128/158/200); se documenta
  como aproximado.

Fuente de la referencia mensual
-------------------------------
- **UMA diaria 2016–2025: INEGI (DOF).** Mensual = diaria × 30.4.
- **2015: salario mínimo general (pre-UMA), $70.10 diarios** (aprox.; en 2015
  hubo zonas salariales parte del año).

Limitación (ver `docs/decisiones.md`)
-------------------------------------
El Infonavit reconoce que el alza de precios por encima de la inflación afecta la
comparabilidad intertemporal de esta clasificación: parte del "corrimiento al
alza" 2015–2025 puede ser artefacto de que los umbrales no siguen el ritmo de los
precios, no solo mercado real.
"""

from __future__ import annotations

import pandas as pd

# Umbrales de cada segmento, en múltiplos de la referencia (límite inferior
# incluido, superior excluido). None = sin límite superior.
SEGMENTOS_UMA: dict[str, tuple[float, float | None]] = {
    "Económica":        (0,    118),
    "Popular":          (118,  200),
    "Tradicional":      (200,  350),
    "Media":            (350,  750),
    "Residencial":      (750,  1500),
    "Residencial plus": (1500, None),
}

# Referencia diaria por año (pesos). UMA oficial (INEGI); 2015 = salario mínimo.
_REF_DIARIA: dict[int, float] = {
    2015: 70.10,
    2016: 73.04, 2017: 75.49, 2018: 80.60, 2019: 84.49, 2020: 86.88,
    2021: 89.62, 2022: 96.22, 2023: 103.74, 2024: 108.57, 2025: 113.14,
}
_DIAS_MES = 30.4  # factor oficial para mensualizar la UMA


def referencia_mensual() -> dict[int, float]:
    """Valor mensual de referencia (UMA/SM) por año, en pesos."""
    return {anio: round(d * _DIAS_MES, 2) for anio, d in _REF_DIARIA.items()}


def tabla_segmento_valor() -> pd.DataFrame:
    """Construye la tabla tidy segmento × año → rango de valor en pesos.

    Returns
    -------
    pd.DataFrame
        Columnas ``['anio', 'segmento', 'uma_inf', 'uma_sup', 'valor_inf',
        'valor_sup']``. ``uma_sup`` y ``valor_sup`` son nulos en el segmento
        abierto (residencial plus). No incluye "No disponible" (sin rango).
    """
    ref = referencia_mensual()
    filas = []
    for anio, r in ref.items():
        for seg, (inf, sup) in SEGMENTOS_UMA.items():
            filas.append(
                {
                    "anio": anio,
                    "segmento": seg,
                    "uma_inf": inf,
                    "uma_sup": sup,
                    "valor_inf": round(inf * r, 2),
                    "valor_sup": round(sup * r, 2) if sup is not None else None,
                }
            )
    df = pd.DataFrame(filas)
    df["valor_sup"] = df["valor_sup"].astype("Float64")
    return df.sort_values(["anio", "uma_inf"]).reset_index(drop=True)
