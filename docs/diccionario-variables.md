# Diccionario de variables

Documenta cada variable del proyecto, organizada por fuente, más las variables
derivadas que se construyen en el análisis. Las "trampas" del dato se anotan en
las notas, porque son decisivas para interpretarlo bien.

**Convenciones.** Tipo: categórica, entero, numérico (decimal), fecha, texto, booleano.
Unidad: se indica cuando aplica (pesos MXN, m², años, conteo).

---

## 1. SNIIV — Cubo Infonavit (columna vertebral · nivel municipio)

Fuente: cubo del SNIIV (Sedatu), filtrado a Yucatán → Mérida, 2015–2025. Las métricas
`acciones` y `monto` se descargan por separado (una a la vez).

| Variable | Tipo | Unidad | Descripción | Notas |
|---|---|---|---|---|
| `año` | entero | — | Año de originación del crédito (2015–2025) | |
| `estado` | categórica | — | Entidad federativa (filtro: Yucatán) | |
| `municipio` | categórica | — | Municipio (filtro: Mérida) | Único nivel sub-estatal disponible |
| `valor_vivienda` | categórica | — | Segmento de valor de la vivienda | **No son pesos**: clasificación en económica, popular, tradicional, media, residencial, residencial plus y "No disponible" |
| `acciones` | entero | conteo | Número de créditos formalizados | |
| `monto` | numérico | pesos MXN | Monto de crédito financiado (suma) | **No es el valor de la vivienda**: es lo prestado, y topa en la gama alta |

**Trampa de "No disponible":** ~28.5% de los créditos caen en este segmento, sin clasificación
de valor y con monto ≈ 0. Se excluyen del análisis de valor, pero se reportan como dato (parte
de la actividad no es compra de vivienda).

---

## 2. Datos Masivos — SII Infonavit (contexto · nivel estatal)

Fuente: consulta "Datos Masivos" del SII (Infonavit), nivel **estado** (no municipio) y sin
valor de vivienda. El corte exacto se define en la Fase 2; abajo, las variables disponibles
(nombres aproximados, a confirmar al extraer).

**Dimensiones**

| Variable | Tipo | Descripción |
|---|---|---|
| `tipo_de_producto` | categórica | Producto de crédito |
| `linea` | categórica | Línea de crédito (adquisición, mejora, pago de pasivos, etc.) |
| `clasificacion_vivienda` | categórica | Segmento de vivienda (análogo a `valor_vivienda`) |
| `nivel_ingreso` | categórica | Ingreso del acreditado, en UMA |
| `edad` | categórica/entero | Edad del acreditado |
| `estado` | categórica | Entidad federativa |
| `modalidad` | categórica | Modalidad del crédito |

**Métricas**

| Variable | Tipo | Unidad | Descripción |
|---|---|---|---|
| `creditos_formalizados` | entero | conteo | Número de créditos |
| `importe_cheque` | numérico | pesos MXN | Importe del cheque |
| `monto_credito` | numérico | pesos MXN | Monto de crédito |
| `subsidios` | numérico | pesos MXN | Subsidios otorgados |
| `calidad` (Ecuve / SISEVIVE / IDG) | numérico/índice | — | Indicadores de calidad de la vivienda |
| `recaudacion_fiscal` | numérico | pesos MXN | Datos de recaudación fiscal |

Uso previsto: contexto del acreditado (ingreso, edad) y de calidad a nivel estatal. **No** aporta
municipio ni valor de vivienda.

---

## 3. Inmuebles24 (oferta · dataset propio · nivel propiedad)

Fuente: dataset propio del proyecto `dataset-inmuebles-merida` (~59 anuncios, segmento medio-alto).
`precio` es **precio de lista**, no de cierre.

| Variable | Tipo | Unidad | Descripción | Notas |
|---|---|---|---|---|
| `fecha_registro` | fecha | — | Fecha de captura del anuncio | Dato a fecha de corte (no continuo) |
| `url` | texto | — | URL del anuncio | |
| `url_archivo` | texto | — | URL/archivo de respaldo | |
| `operación` | categórica | — | Tipo de operación (venta/renta) | Para el análisis interesa venta |
| `tipo_inmueble` | categórica | — | Tipo de inmueble (casa, depto, terreno…) | |
| `colonia` | texto | — | Colonia en Mérida | |
| `precio` | numérico | pesos MXN | **Precio de lista** del anuncio | No es precio de cierre ni de avalúo |
| `m2_construccion` | numérico | m² | Superficie construida | |
| `m2_terreno` | numérico | m² | Superficie de terreno | |
| `recamaras` | entero | conteo | Número de recámaras | |
| `banos` | numérico | conteo | Número de baños (puede ser .5) | |
| `estacionamientos` | entero | conteo | Cajones de estacionamiento | |
| `antigüedad` | numérico/categórica | años | Antigüedad de la vivienda | |
| `es_preventa` | booleano | — | Si el anuncio es preventa | |
| `notas` | texto | — | Notas libres | |

---

## 4. Variables derivadas (construidas en el análisis)

| Variable | Cómo se calcula | Unidad | Descripción |
|---|---|---|---|
| `monto_promedio_credito` | `monto` / `acciones` (por segmento y año) | pesos MXN | Crédito promedio por acción; proxy del financiamiento, no del valor |
| `participacion_segmento` | acciones (o monto) del segmento / total | % | Mezcla por segmento |
| `precio_m2` | `precio` / `m2_construccion` (Inmuebles24) | pesos MXN/m² | Precio de lista por m² |
| `segmento_rango_pesos` | mapeo segmento → rango oficial | pesos MXN | Traduce el segmento categórico a una banda de valor (ver sección 5) |

(Las variables de contraste oferta-vs-financiado se definen en la fase de análisis.)

---

## 5. Mapeo segmento ↔ rango de valor

El segmento `valor_vivienda` (y `clasificacion_vivienda`) corresponde a rangos de valor definidos
por **CONAVI / Infonavit**, expresados en múltiplos de UMA / salario mínimo y **revisados por año**.
La tabla con los umbrales exactos por año se construye en la Fase 3 (modelo de datos) a partir de
fuentes oficiales; **no se inventan aquí**. Sirve para acotar en pesos, de forma aproximada, cada
segmento, recordando que el `monto` de crédito subestima el valor en la gama alta.
