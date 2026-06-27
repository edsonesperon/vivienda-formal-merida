# Fuentes y procedencia

Documenta, por fuente, qué es, de dónde viene, cómo y cuándo se extrajo, y notas de
reproducibilidad. El objetivo es que cualquiera pueda rehacer la extracción.

---

## 1. SNIIV — Cubo Infonavit (Sedatu)

- **Qué es:** cubo dinámico (PivotTable) de originación de crédito Infonavit.
- **Fuente:** https://sniiv.sedatu.gob.mx/Cubo/Infonavit
- **Nivel:** municipio (único con este detalle) + segmento de valor.
- **Corte de datos:** según el cubo, al 31-mar-2026.
- **Fecha de extracción:** 2026-06-16.

**Procedimiento de extracción (reproducible):**

1. Año: de **2015 a 2025**.
2. Estado: **Yucatán**. Municipio: **Mérida**.
3. Variable: marcar **"Valor de la vivienda"**.
4. Visualización: **Tabla**, con `año` en filas y `valor_vivienda` en columnas.
5. Métrica: el cubo solo permite **una a la vez**, así que se descarga **dos veces**: una con **acciones** y otra con **monto**.
6. El botón "Descargar" entrega una **tabla HTML con extensión `.xls`** (no Excel real); se parsea leyendo el atributo `data-value` de cada celda.

**Archivos resultantes (en `data/raw/`):**

- `infonavit_acciones-segmento_merida_2015-2025_2026-06-16.xls`
- `infonavit_monto-segmento_merida_2015-2025_2026-06-16.xls`

---

## 2. Datos Masivos — SII Infonavit

- **Qué es:** consulta agregada ("Datos Masivos") del SII, descargable en texto plano.
- **Fuente:** portal del SII (portalmx.infonavit.org.mx → derechohabientes → el instituto → SII → masivos).
- **Nivel:** **estado** (no municipio). **No** incluye "valor de la vivienda".
- **Esquema:** ver el Archivo Descriptor (PDF) de la propia consulta.
- **Extracción:** pendiente; el corte exacto (dimensiones y métricas) se define en la Fase 2.

---

## 3. Inmuebles24 — dataset propio

- **Qué es:** ~59 anuncios de Inmuebles24 (Mérida, segmento medio-alto), con **precios de lista**.
- **Procedencia:** proyecto previo `dataset-inmuebles-merida`
  (github.com/edsonesperon/dataset-inmuebles-merida), archivo `data/propiedades.csv`.
- **Nivel:** propiedad (anuncio).
- **Recolección:** capturada en el proyecto anterior; el scraper automatizado quedó bloqueado por Cloudflare + hCAPTCHA, por lo que el conjunto es acotado.
- **Fecha:** ver la columna `fecha_registro` de cada anuncio.
- **Nota:** precios de **lista**, a fecha de corte (no continuos ni de cierre).

---

## 4. Umbrales de segmento y serie de UMA (insumos del mapeo)

Para el mapeo de la Fase 3 (`src/mapeo_segmentos.py`).

**Umbrales de los segmentos (múltiplos de UMA/SM):**

- **Oficial:** Infonavit, *Plan Estratégico y Financiero 2026* (aprobado por la
  Asamblea, dic-2025; cita INEGI y RUV): económica-popular hasta 200 UMA;
  tradicional 200–350 UMA. Fuente: portalmx.infonavit.org.mx (PEF 2026).
- **Convención (confianza media):** cortes 118, 750 y 1500, de la clasificación
  estándar RUV/AHM; el RUV sugiere ~128 para económica (subniveles popular
  128/158/200).

**Serie de referencia mensual:**

- **UMA diaria 2016–2025:** INEGI / DOF (mensual = diaria × 30.4).
  Fuente: https://www.inegi.org.mx/temas/uma/
- **2015:** salario mínimo general (pre-UMA), $70.10 diarios (aprox.).
