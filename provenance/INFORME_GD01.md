# INFORME GD01 · El Teorema 2 de Qiu, Carroll y Allen (ICLR 2026) es falso: medir el acuerdo premia no informar

**Fecha:** 24/11/2026 (portátil, ala A10).

**Trazabilidad:**
- Teoría, preregistro (con los enunciados de Lean) y FREEZE en `7350872f`, antes de escribir las pruebas.
- Lean: `formal/aa_nash/AaNash/PeerPredictionGD01.lean`, independiente y fuera de la raíz.
- Comprobaciones exactas: `GD01_RESULTS/gd01_exact.json`.
- Recibo de compilación: `GD01_RESULTS/lean_compilacion.txt`.
- Sondeo de novedad copiado en `novedad/`.

## Veredicto preregistrado: **TEOREMA 2 REFUTADO, en la lectura I y también en la lectura II**

| Comprobación | Resultado |
|---|---|
| Lean: los 9 enunciados son idénticos a los del preregistro (comparación automática) | sí |
| Lean: `caseA_gain`, `caseA_c0_pos`, `caseB_gain`, `caseB_c1_pos`, `caseB_mixture`, `alg1_caseA_pos` | compilan sin `sorry`; axiomas: propext, Classical.choice y Quot.sound |
| V1: fuerza bruta sobre 𝒜ⁿ (n = 2, 3, 4) frente a la fórmula, caso A | diferencia máxima 7·10⁻¹⁷; ganancia mínima 0,105 por objetivo (media sobre señales) |
| V2: Supuesto 1 en 𝒟_A | I₀ = 1,02; L₀ = 0,92 |
| V3: probabilidades y umbral | P(fracción Lat fuera de [4/5, 1]) va de 0,0094 (m = 50) a 10⁻²¹ (m = 1000); P(algún Ind) = 1 − 0,9ⁿ; el umbral del propio teorema para ε = c₀/2 y δ = 0,05 es m, n ≥ 493 |
| V4: fuerza bruta del caso B | diferencia máxima 8·10⁻¹⁷; ganancia mínima 0,138; Supuesto 1 con I₀ = 2,72 y L₀ = 2,94 |
| V5: variante Algoritmo 1 | la fórmula coincide exactamente con el cálculo directo |

## Qué se ha demostrado, en palabras

**El mecanismo:**
- La *peer prediction* del artículo puntúa la respuesta de un modelo según cuánto ayuda a una multitud de expertos a predecir lo que responden los demás.
- El Teorema 2 afirma que, aunque participantes y expertos tengan creencias distintas, con muchos expertos y participantes decir la verdad es un ε-equilibrio.

**El caso A, en una población natural:**
- El 90 % cree que hay una verdad que todos siguen con ruido; el 10 % cree que las respuestas son independientes y suelen ser 0.
- A un participante del 10 % le conviene **responder siempre 0**, sea cual sea su respuesta sincera. Gana al menos 0,487 nats por objetivo, para cualquier fracción de expertos «de mayoría» entre el 80 % y el 100 %.
- La razón: su puntuación es mejor cuando la predicción media de los expertos se parece a lo que él espera. Más expertos no lo arreglan, lo estabilizan.
- Como con muchos participantes casi seguro hay alguno así, la conclusión del teorema falla para todo ε < 0,487, con m y n tan grandes como pide el propio teorema.

**El caso B, en la lectura caritativa** (nadie ajusta su estrategia a su propio prior): con priors que distinguen a un participante, que el teorema permite, «responder siempre 1» gana ex ante al menos 0,127.

**Las dos desviaciones ganadoras son no informativas.** Contradicen la frase del artículo de que el mecanismo «penalizes both deceptive answers and uninformative ones». Es Goodhart en sentido estricto: optimizar la medida del acuerdo lleva a dejar de informar.

**Dónde falla la prueba (C.2):**
- El paso (19) cambia, «por Hoeffding», la media aritmética de las probabilidades de los expertos por una media geométrica de los priors (log P̄ = E_𝒟[log P], sin normalizar). Hoeffding no autoriza eso, y la diferencia de Jensen no se reduce con m.
- El paso a n finito promedia sobre el prior del propio emisor. Así solo descarta desviaciones que no dependen de él.

## Alcance y límites

- **Lean** verifica la desigualdad para cada par emisor-objetivo y la mezcla de creencias del caso B.
- La reducción de la puntuación con n participantes a pares se verifica por **fuerza bruta exacta** con n ≤ 4, más el argumento de linealidad (la puntuación es una media sobre objetivos de términos por pares). No está en Lean.
- La concentración de la fracción de expertos se da con **probabilidades binomiales exactas** (V3), no en Lean.
- **Lectura I frente a II:** la lectura I es la de la notación de la propia prueba (esperanza bajo 𝒫ₛᴬ). La II se refuta con priors que no son intercambiables. Con priors intercambiables de clase latente no se encontró contraejemplo para la II (búsqueda exploratoria; no es una prueba de que no exista).
- **No se toca:**
  - el Teorema 1 (prior común, clásico), que es correcto;
  - los experimentos del artículo ni su utilidad práctica;
  - la afirmación sobre la convergencia del entrenamiento, que es otra pregunta.
- **Pendiente:**
  - leer la discusión de OpenReview (`forum?id=mdw0vvRBEL`), bloqueada por la verificación del navegador, que no se forzó;
  - una lectura experta independiente de la lectura I;
  - la decisión del usuario sobre contactar con los autores. No se ha contactado con nadie ni se ha publicado nada.
- **Verificación propia no es réplica externa.**

## Grado

**1/3 (autoevaluado), candidato a 2/3\*.**

**Lo que acerca a 2/3\*:**
- es un teorema nuevo de ICLR 2026, presentado como «of independent interest», sin v2;
- el contraejemplo es pequeño y exacto, verificado en Lean con enunciados preregistrados;
- el fallo de la prueba está localizado;
- el patrón es el del carril: una garantía para creencias comunes, trasladada a creencias heterogéneas y a entrenamiento.

**Lo que falta:**
- que el foro de OpenReview no muestre ya una corrección;
- una lectura experta independiente;
- si el usuario lo decide, la respuesta de los autores, como en AA/Nash.

**Para el TFM** es el núcleo formal de la línea «Goodhart en sistemas de crédito»:
- AU01/AU02: repartir el crédito rompe el óptimo del equipo;
- SE01/SE02: más crédito por voto trae más preguntas de bajo reconocimiento, sin que los votantes compensen;
- GD01: medir el acuerdo premia no informar.

CT2 sin asignar.

## Adenda (24/11/2026): foro de OpenReview leído

El usuario pasó la verificación del navegador en su Chrome y se leyó el foro entero (`forum?id=mdw0vvRBEL`, 16/16 respuestas). Notas en `novedad/openreview_foro_mdw0vvRBEL.md`.

**No hay ninguna corrección ni crítica del Teorema 2 en el foro:**
- Las cuatro revisiones (6, 6, 8 y 4) declaran que las matemáticas no se comprobaron con detalle.
- Ninguna nota menciona el paso (19), la diferencia de Jensen, las desviaciones que dependen del propio prior ni las respuestas no informativas.
- La metarrevisión habla de distancia entre teoría y experimentos, no de que el teorema sea incorrecto.

**La única tensión registrada no cubre GD01:**
- El revisor PGHr señaló que la Fig. 9 con α = 0, el método sin pesos, «seems to contradict» el Teorema 2.
- Los autores lo atribuyen a que en la práctica no se cumple la hipótesis de que los priors de participantes y expertos salen de la misma distribución.
- Los contraejemplos de GD01 **sí** cumplen esa hipótesis, así que la explicación de los autores no los cubre.

**Los autores dicen que el propósito del teorema es que «more participants imply better truthfulness».** En el caso A la ganancia de la desviación no depende de n ni de m.

**Sigue pendiente:**
- La ficha dice «Last Modified: 11 Apr 2026». La lista de revisiones volvió a pedir la verificación y no se leyó.
- **Hay que comparar el Teorema 2 del PDF final de OpenReview con el de arXiv v1** antes de dar el contraejemplo por vigente frente a la versión publicada.
- La lectura experta independiente y la decisión del usuario sobre los autores no cambian.

**Grado:** sigue en 1/3, candidato a 2/3\*. Uno de los tres pendientes queda resuelto en parte: el foro no tiene corrección, pero falta el PDF final.

**Actualización (mismo día): PDF final leído.** Con la sesión del usuario iniciada en OpenReview se leyó el PDF final («Published as a conference paper at ICLR 2026», 36 pp.).
- El Teorema 2 (pp. 6–7) y su prueba (C.2, pp. 27–28) coinciden con arXiv v1 en todo lo que usa GD01:
  - las hipótesis, el umbral y la conclusión ex ante;
  - el paso (19) «from Hoeffding's inequality» con log 𝒫̄ = E_𝒟[log 𝒫];
  - el supuesto 𝒫ᵢᴬ = 𝒫̄ en el caso n → ∞;
  - «(20) is the mean of (17) over the choice of {𝒫ᵢᴬ}».
- La lista de revisiones de OpenReview está vacía.
- **El contraejemplo vale contra la versión publicada.** La comparación es visual, no un diff textual; detalle en `novedad/openreview_foro_mdw0vvRBEL.md`.
- Pendientes que quedan para 2/3\*: la lectura experta independiente y la decisión del usuario sobre los autores.

## Adenda de precisión (24/11/2026): ganancia condicionada frente a promediada

Al redactar el mensaje a los autores se precisa la magnitud del caso A. El contraejemplo no cambia; cambia cuánto vale ε según cómo se lea el ε-equilibrio.

- **c₀ ≈ 0,487** es la ganancia por objetivo **condicionada a que la propia respuesta sea 1**: ε-equilibrio *interim*, por tipo y señal.
- **Promediada sobre la propia respuesta,** con P(señal 1) = 1/5 bajo el prior Ind, la ganancia es al menos **c₀/5 ≈ 0,097**. Es la cota que corresponde a la «ganancia mínima 0,105 por objetivo (media sobre señales)» de V1: 0,105 en f = 4/5.
- **Por tanto,** la conclusión del Teorema 2 falla:
  - para todo ε < 0,487 en la lectura condicionada, con umbral 493 para ε = c₀/2 y δ = 0,05;
  - para todo ε < 0,097 en la lectura promediada sobre la propia respuesta, con umbral 2791 para ε = c₀/10 y δ = 0,05.
- Las dos ganancias son independientes de m y de n, así que el teorema queda refutado en ambas lecturas.
- La frase «falla para todo ε < 0,487» de la sección «Qué se ha demostrado» solo vale en la lectura condicionada.
- `TEORIA_GD01.md` está congelado y no se toca; esta adenda lo precisa.
- El caso B ya era ex ante, promediado: c₁ ≈ 0,127.

**Borrador de mensaje a los autores** (no enviado): `MENSAJE_AUTORES_BORRADOR.md`.
