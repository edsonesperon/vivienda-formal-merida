# Bitácora de decisiones

Registra las "trampas" del dato encontradas y las decisiones analíticas tomadas frente a
ellas. Sirve para que el análisis sea interpretable y defendible: muchas de estas decisiones
requieren criterio de dominio y no se deducen del dato en bruto.

---

1. **"Valor de la vivienda" es un segmento, no pesos.** La variable no es un precio continuo,
   sino una clasificación categórica (económica, popular, tradicional, media, residencial,
   residencial plus). *Decisión:* tratarla como segmento, no como valor en pesos.

2. **"Monto" es crédito financiado, no valor de la vivienda.** El monto promedio en Mérida
   (~$493 K por crédito, excluyendo no clasificados) es tamaño de crédito, no de vivienda.
   *Decisión:* interpretar `monto` como financiamiento; usarlo como proxy y piso del valor,
   nunca como el valor mismo.

3. **El crédito topa en la gama alta.** En residencial / residencial plus el crédito promedio
   resulta menor que en media / tradicional, porque el crédito Infonavit topa y el comprador
   pone el resto por fuera. *Decisión:* para valuar la gama alta, confiar en el segmento
   (rangos conocidos) más que en el monto.

4. **"No disponible" ≈ 28.5% de los créditos.** Casi un tercio no tienen segmento ni monto
   (monto ≈ 0); probablemente no son compra de vivienda. *Decisión:* excluirlos del análisis
   de valor, pero reportarlos como dato (≈28% de la actividad no es adquisición).

5. **El cubo no descarga acciones y monto juntos.** El SNIIV solo permite una métrica por
   descarga. *Decisión:* bajar dos extractos por corte (acciones y monto) y cruzarlos por año
   y segmento.

6. **La descarga del SNIIV es HTML disfrazado de `.xls`.** "Descargar" entrega una tabla HTML
   con extensión `.xls`. *Decisión:* parsearla leyendo el atributo `data-value` de cada celda,
   no abrirla como Excel.

7. **Datos Masivos es estatal y sin valor de vivienda.** No tiene municipio ni segmento de
   valor. *Decisión:* usar SNIIV como columna vertebral (municipio + segmento) y Datos Masivos
   solo como contexto estatal (ingreso, edad, calidad).

8. **El precio de Inmuebles24 es de lista, no de cierre.** Son ~59 anuncios, segmento
   medio-alto, a fecha de corte. *Decisión:* usarlos para un contraste direccional de la oferta
   por segmento / distribución, no para inferencia fina.

9. **Mapeo segmento → pesos por año (opción rigurosa).** Los segmentos se definen
   en múltiplos de la referencia mensual (salario mínimo hasta 2015, UMA desde
   2016), no en pesos fijos, así que la frontera en pesos se recorre cada año.
   *Decisión:* construir la tabla por año (múltiplo × UMA/SM del año), no una tabla
   fija; la foto en pesos de la AHM resultó de un año viejo y se descartó como
   referencia fija. Umbrales 200 y 350 UMA: oficiales (Infonavit PEF 2026). Cortes
   118, 750 y 1500: convención RUV/AHM, marcados como tales.

10. **Comparabilidad intertemporal de la clasificación.** El propio Infonavit
    reconoce que el alza de precios por encima de la inflación afecta la
    comparabilidad en el tiempo de la clasificación estándar por rangos de valor.
    *Nota para la Fase 4:* parte del "corrimiento al alza" 2015–2025 puede ser
    artefacto de umbrales que no siguieron el ritmo de los precios, no solo mercado
    real; hay que distinguir cuánto es real vs. artefacto al interpretar.
