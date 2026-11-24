# PREREG GD01 · Verificación formal del contraejemplo al Teorema 2 de Qiu, Carroll y Allen (ICLR 2026)

**Fecha:** 24/11/2026 (portátil, ala A10). La teoría está en `TEORIA_GD01.md`.

**Congelado** (hashes en `FREEZE_GD01.txt`): este preregistro (con los enunciados de Lean), `TEORIA_GD01.md` y `gd01_exact.py`. Se sube antes de escribir las pruebas de Lean y antes de la ejecución definitiva del script.

## 1. Qué se sabe ya (no es un experimento ciego)

Es un ciclo de **verificación matemática**, no una prueba con datos. Los valores numéricos ya se conocen por la exploración del sondeo y por las ejecuciones de desarrollo de `gd01_exact.py`, que cuadran con la fuerza bruta en 10⁻¹⁶.

**Lo que este preregistro fija antes de las pruebas:**
- los enunciados exactos;
- la lectura del Teorema 2;
- los criterios de éxito y de fracaso;
- qué no se afirma.

**Comprobaciones de que no esté ya corregido:**
- arXiv solo tiene la v1 (28/01/2026).
- El foro de OpenReview (`forum?id=mdw0vvRBEL`) muestra una verificación del navegador que no se ha forzado, así que **no se ha leído la discusión de revisión**. Queda pendiente: el usuario puede abrirlo.
- El sondeo no encontró ninguna crítica publicada del Teorema 2.

## 2. Lecturas del Teorema 2

- **Lectura I (principal):** cada participante conoce su propio prior 𝒫ᵢᴬ, y el equilibrio se comprueba para cada tipo. Es la notación de la propia prueba, que toma la esperanza bajo 𝒫ₛᴬ.
- **Lectura II (secundaria):** el participante no condiciona su estrategia a su propio prior; la comparación es ex ante sobre 𝒟, con desviaciones σ: 𝒜 → 𝒜 iguales para todos los tipos.

## 3. Enunciados de Lean

**Archivo:** `formal/aa_nash/AaNash/PeerPredictionGD01.lean`, independiente y fuera de la raíz `AaNash.lean`.
- **Compilación:** `lake env lean AaNash/PeerPredictionGD01.lean`.
- **Condición:** sin `sorry`; `#print axioms` solo puede mostrar propext, Classical.choice y Quot.sound.

```lean
namespace AaNash.GD01
/-- parte de la puntuación esperada que depende del informe: b·log p + (1−b)·log(1−p),
    con b = P(A_t = 1) para el emisor y p = p̄(A_t = 1 | informe) -/
noncomputable def sc (b p : ℝ) : ℝ := b * Real.log p + (1 - b) * Real.log (1 - p)
/-- caso A: fracción f de expertos Lat (41/50, 9/50) y 1 − f de Ind (1/5) -/
noncomputable def pbarA (f : ℝ) (r : Bool) : ℝ := f * (if r then 41/50 else 9/50) + (1 - f) * (1/5)
theorem caseA_gain (f : ℝ) (h0 : 4/5 ≤ f) (h1 : f ≤ 1) :
    (1/5) * Real.log (9/41) + (4/5) * Real.log (51/19)
      ≤ sc (1/5) (pbarA f false) - sc (1/5) (pbarA f true)
theorem caseA_c0_pos : 0 < (1/5) * Real.log (9/41) + (4/5) * Real.log (51/19)
/-- caso B: fracción f de expertos P1 (9/20, 1/20) y 1 − f de P2 (1/5, 19/20) -/
noncomputable def pbarB (f : ℝ) (r : Bool) : ℝ := f * (if r then 9/20 else 1/20) + (1 - f) * (if r then 1/5 else 19/20)
theorem caseB_gain (f : ℝ) (h0 : 3/10 ≤ f) (h1 : f ≤ 2/5) :
    (19 * Real.log (55/136) + 127 * Real.log (70/41)) / 400
      ≤ (146/400) * (sc (19/146) (pbarB f true) - sc (19/146) (pbarB f false))
theorem caseB_c1_pos : 0 < 19 * Real.log (55/136) + 127 * Real.log (70/41)
/-- la creencia ex ante del caso B sale de P1, P2 y w = 7/20: P(A₁ = 0, A_t = y) para y = 1 y y = 0 -/
theorem caseB_mixture :
    (7/20 : ℚ) * ((19/20) * (1/20)) + (13/20) * ((1/20) * (19/20)) = 19/400 ∧
    (7/20 : ℚ) * ((19/20) * (19/20)) + (13/20) * ((1/20) * (1/20)) = 127/400
/-- variante Algoritmo 1 (media de logaritmos) en el caso A: ganancia f·((4/5)·log(41/9) + (1/5)·log(9/41)) > 0 -/
theorem alg1_caseA_pos (f : ℝ) (hf : 0 < f) :
    0 < f * ((4/5) * Real.log (41/9) + (1/5) * Real.log (9/41))
end AaNash.GD01
```

**Correspondencia** (la cubre `gd01_exact.py` por fuerza bruta):
- sc(b, p̄(·|r)) − sc(b, p̄(·|r′)) es la diferencia de puntuación esperada por objetivo entre los informes r y r′, porque el término log q̄ se cancela.
- La media aritmética de las condicionales de una reserva de expertos con fracción f es pbarA o pbarB.
- En el caso B, el factor 146/400 = P_mezcla(A₁ = 0) y 19/146 = P_mezcla(A_t = 1 | A₁ = 0).

## 4. Comprobaciones exactas (`gd01_exact.py`)

**Ejecución:** `python -I -X utf8 gd01_exact.py GD01_RESULTS/gd01_exact.json`.

| Código | Comprobación | Criterio |
|---|---|---|
| V1 | Fuerza bruta sobre 𝒜ⁿ (n = 2, 3, 4; f ∈ {4/5, 9/10, 1}) frente a la fórmula cerrada del caso A | diferencia < 10⁻⁹ y ganancia > 0 en todos |
| V2 | Supuesto 1 en 𝒟_A | I₀ y L₀ finitos |
| V3 | Probabilidades exactas de que la fracción Lat quede fuera de [4/5, 1] (m = 50 … 1000) y de que haya algún participante Ind (1 − 0,9ⁿ); umbral del Teorema 2 para ε = c₀/2 y δ = 0,05 | umbral finito; probabilidad de fallo del teorema ≥ 1 − 0,9ⁿ − P(fuera) |
| V4 | Fuerza bruta del caso B (n = 2, 3, 4; f ∈ {3/10, 7/20, 2/5}) frente a la fórmula; Supuesto 1 en 𝒟_B | diferencia < 10⁻⁹ y ganancia > 0 |
| V5 | Variante Algoritmo 1 en el caso A, directa frente a la fórmula | coinciden y > 0 |
| V6 | Paso (19) en el caso A: lado izquierdo con media aritmética frente a media geométrica | solo descriptivo |

## 5. Regla de veredicto

| Veredicto | Condición |
|---|---|
| **TEOREMA 2 REFUTADO (lectura I)** | `caseA_gain` y `caseA_c0_pos` compilan sin `sorry` y con los axiomas estándar, y V1, V2 y V3 pasan |
| **… y también en la lectura II** | además `caseB_gain`, `caseB_c1_pos` y `caseB_mixture` compilan, y V4 pasa |
| **NO VERIFICADO** | algún enunciado no se puede probar o la fuerza bruta discrepa. Se informa tal cual; cualquier cambio de enunciado requiere una adenda fechada antes de reintentar |

`alg1_caseA_pos` y V5 son secundarios: muestran que no es un artefacto de la variante del Algoritmo 2.

## 6. Qué no se afirma

- El Teorema 1 (prior común) no se discute.
- No se evalúan los experimentos del artículo, ni si el método funciona en la práctica.
- No se demuestra nada sobre la dinámica de entrenamiento («converge upon honest … policies»).
- Lean no formaliza la reducción a pares de la puntuación con n participantes. La cubre la fuerza bruta exacta para n ≤ 4 y el argumento de linealidad de `TEORIA_GD01.md`.
- No se contacta con los autores ni se publica nada sin decisión del usuario.
