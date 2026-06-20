# Vivienda formal en Mérida: segmento, acceso y desajuste de mercado (2015–2025)

> Análisis reproducible del financiamiento de vivienda del Infonavit en Mérida, Yucatán: qué se financia por segmento de valor, cómo ha evolucionado el acceso y cómo contrasta con lo que ofrece el mercado.

## Fases

**Fase 0 — Andamiaje del repo (completada):** estructura del proyecto, entorno conda (`vivienda-merida`, Python 3.11), `.gitignore`, `README.md` y publicación del repositorio en GitHub. Convención de commits establecida (Conventional Commits + estilo Chris Beams).

**Fase 1 — Documentación base (completada):** tres documentos en `docs/`: `diccionario-variables.md` (variables por fuente y derivadas), `fuentes-y-procedencia.md` (de dónde sale cada fuente y cómo se extrae) y `decisiones.md` (bitácora de las trampas del dato y el criterio para resolverlas).

**Fase 2 — Ingesta y caracterización (en progreso):** parseo de los pivotes HTML del cubo SNIIV a DataFrames *tidy* (año × segmento, para acciones y monto), carga del dataset de Inmuebles24, y definición y descarga del corte de Datos Masivos. Salida prevista: notebook `01_ingesta` y parsers reutilizables en `src/`.

**Fase 3 — Limpieza y modelo de datos (pendiente):** formato largo, base de datos ligera (SQLite) y tabla de mapeo segmento ↔ rango de valor a partir de fuentes oficiales (CONAVI/Infonavit).

**Fase 4 — EDA y análisis (pendiente):** mezcla y tendencia de segmentos, montos promedio, el corrimiento al alza 2015–2025, y el contraste entre lo financiado (SNIIV) y lo listado (Inmuebles24).

**Fase 5 — Validación (pendiente):** chequeos de consistencia interna y contra referencias externas.

**Fase 6 — Síntesis y entregable (pendiente):** reporte con los hallazgos (y un tablero opcional).

---

## Contexto y motivación

El Infonavit es el principal originador de crédito hipotecario en México. Sus datos públicos permiten observar, por municipio y año, qué tipo de vivienda financian los trabajadores formales. Este proyecto usa esa información para responder una pregunta de relevancia social en Mérida: **¿se está corriendo fuera de alcance —o desajustando de la oferta— la compra de vivienda vía crédito formal?**

Complementa un proyecto previo centrado en **precios de lista** (anuncios de Inmuebles24): aquel describe la *oferta*; este describe la *demanda efectivamente financiada*. Juntos permiten contrastar "cuánto se pide" contra "qué se financia".

## Objetivos

**General.** Caracterizar e interpretar cómo evolucionó el financiamiento formal de vivienda en Mérida (2015–2025) —por segmento de valor, volumen de crédito y perfil del acreditado— y contrastarlo con lo que el mercado lista, para evaluar acceso y desajuste.

**Específicos.**

1. Construir un pipeline reproducible que ingiera, limpie e integre las fuentes, con manejo documentado de las trampas del dato.
2. Cuantificar la mezcla de segmentos de vivienda y su corrimiento 2015–2025, y la evolución del flujo de crédito.
3. Mapear los segmentos a rangos de valor y contrastar la distribución de lo financiado contra la de precios de lista.
4. Caracterizar al acreditado (ingreso en UMA, edad) y el contexto de calidad de vivienda.
5. Sintetizar los hallazgos en una lectura de acceso/asequibilidad para una audiencia definida, con sus reservas metodológicas.

## Alcance

**Dentro:** Mérida (municipio) como foco, con Yucatán y nacional como contexto; periodo 2015–2025; financiamiento Infonavit por segmento de valor y montos de crédito; perfil del acreditado y calidad de vivienda; precios de lista del dataset propio de Inmuebles24; mapeo segmento↔rango de pesos. Entregable: pipeline reproducible + reporte analítico (y, eventualmente, un tablero).

**Fuera (a propósito):**

- Predicción de precio vivienda por vivienda (el dato del Infonavit es agregado).
- Microdatos de transacciones individuales (no existen de forma pública).
- Precio exacto de la vivienda en pesos desde el Infonavit (solo hay segmento de valor + monto de crédito).
- Afirmaciones causales fuertes; el análisis es descriptivo/asociativo.
- Datos en tiempo real; se trabaja con extractos a fecha de corte.

## Fuentes de datos

| Fuente | Nivel | Qué aporta | Rol |
|---|---|---|---|
| **SNIIV — Cubo Infonavit** (Sedatu) | Municipio | Segmento de valor, acciones (créditos) y monto, 2015–2025 | Columna vertebral |
| **Datos Masivos — SII Infonavit** | Estatal | Ingreso (UMA), edad, calidad (Ecuve/SISEVIVE), subsidios, fiscal | Contexto + escala |
| **Inmuebles24** (dataset propio) | Propiedad | Precios de lista (segmento medio-alto) | Lado de la oferta |

La procedencia detallada (cómo y cuándo se extrajo cada cosa) se documenta en [`docs/fuentes-y-procedencia.md`](docs/fuentes-y-procedencia.md).

## Estructura del repositorio

```
vivienda-formal-merida/
├── README.md
├── data/
│   ├── raw/          # extractos tal cual (SNIIV .xls-HTML, Datos Masivos, Inmuebles24)
│   ├── interim/      # datos limpios/intermedios
│   └── processed/    # tablas finales para análisis
├── docs/
│   ├── diccionario-variables.md     # definición de variables
│   ├── fuentes-y-procedencia.md     # cómo y cuándo se extrajo cada cosa
│   └── decisiones.md                # bitácora de decisiones y "trampas" del dato
├── notebooks/        # 01_ingesta, 02_limpieza, 03_eda, ...
├── src/              # parsers, ingesta y limpieza reutilizables
├── outputs/          # figuras, tablas y reporte
├── environment.yml
└── .gitignore
```

## Metodología

1. **Ingesta y caracterización** — parseo de los pivotes HTML del cubo, carga de los archivos planos, documentación de esquema y trampas.
2. **Limpieza y modelo de datos** — formato *tidy*/largo, base de datos ligera (SQLite) y tabla de mapeo segmento↔valor.
3. **EDA y análisis** — tendencias de segmento, montos promedio, distribuciones y desajuste contra precios de lista.
4. **Validación** — chequeos de consistencia interna y contra referencias externas.
5. **Síntesis y entregable** — reporte (y tablero opcional).

## Limitaciones y consideraciones clave

Estas decisiones documentan por qué el análisis requiere criterio de dominio y no es replicable por una herramienta automática sin contexto:

- **"Valor de la vivienda" no son pesos:** es una clasificación por segmento (económica, popular, tradicional, media, residencial, residencial plus) con rangos de valor definidos por política, no un precio continuo.
- **"Monto" es crédito, no precio:** el monto promedio (~$493 K por crédito en Mérida, excluyendo no clasificados) es el financiamiento, no el valor de la vivienda; en la gama alta el crédito topa y subestima el valor.
- **"No disponible" ≈ 28.5% de los créditos** carece de segmento y de monto; se excluye del análisis de valor pero se reporta como dato (parte de la actividad no es compra de vivienda).
- **Dato agregado:** no hay transacciones individuales; el análisis es de estructura/distribución, no de propiedades.
- **Oferta delgada:** el dataset de listados (~59 propiedades) sirve para un contraste direccional por segmento, no para inferencia fina.

## Reproducción

```bash
conda env create -f environment.yml
conda activate vivienda-merida
jupyter lab
```

## Relación con el proyecto previo

Este proyecto y el [dataset de inmuebles de Mérida](https://github.com/edsonesperon/dataset-inmuebles-merida) son las dos mitades del mismo problema: aquel cubre la **oferta** (precios de lista, scraping, segmento medio-alto) y este la **demanda financiada** (dato oficial, agregado, por segmento). El dataset de listados es uno de los insumos de este proyecto; el scraper documentado en aquel es el mecanismo opcional para ampliarlo.

## Autor

Edson — [github.com/edsonesperon](https://github.com/edsonesperon)

## Licencia

Código bajo licencia MIT (pendiente de agregar `LICENSE`). Los datos provienen de fuentes públicas (SNIIV/Sedatu, Infonavit) sujetas a sus propios términos de uso.
