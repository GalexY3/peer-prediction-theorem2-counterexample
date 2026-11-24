/-
GD01 · Contraejemplo al Teorema 2 de Qiu, Carroll y Allen, «Truthfulness Despite Weak Supervision:
Evaluating and Training LLMs Using Peer Prediction», ICLR 2026 (arXiv 2601.20299 v1). Carril del portátil, 24/11/2026.

Enunciados fijados en `formal/goodhart_pp/PREREG_GD01.md` (FREEZE_GD01, commit 7350872f) antes de escribir las pruebas.
Archivo independiente: no está en la raíz `AaNash.lean`. Compilar con `lake env lean AaNash/PeerPredictionGD01.lean`.

* `sc b p`: parte de la puntuación esperada (Algoritmo 2: log p̄(A_t | informe) − log q̄(A_t)) que depende del informe,
  para un emisor que cree P(A_t = 1) = b, cuando la predicción media de los expertos es p̄(A_t = 1 | informe) = p.
* Caso A (lectura I): expertos Lat (41/50, 9/50) en fracción f e Ind (1/5). Un participante Ind (b = 1/5) con señal 1
  gana al menos c₀ > 0 informando 0 en lugar de 1, para todo f ∈ [4/5, 1].
* Caso B (lectura II): priors en estrella P1, P2 con w = 7/20; «siempre 1» gana ex ante al menos c₁/400 > 0
  para todo f ∈ [3/10, 2/5].
-/
import Mathlib

namespace AaNash.GD01

/-- parte de la puntuación esperada que depende del informe: b·log p + (1−b)·log(1−p),
    con b = P(A_t = 1) para el emisor y p = p̄(A_t = 1 | informe) -/
noncomputable def sc (b p : ℝ) : ℝ := b * Real.log p + (1 - b) * Real.log (1 - p)

/-- caso A: fracción f de expertos Lat (41/50, 9/50) y 1 − f de Ind (1/5) -/
noncomputable def pbarA (f : ℝ) (r : Bool) : ℝ := f * (if r then 41/50 else 9/50) + (1 - f) * (1/5)

theorem caseA_gain (f : ℝ) (h0 : 4/5 ≤ f) (h1 : f ≤ 1) :
    (1/5) * Real.log (9/41) + (4/5) * Real.log (51/19)
      ≤ sc (1/5) (pbarA f false) - sc (1/5) (pbarA f true) := by
  have hF : pbarA f false = f * (9/50) + (1 - f) * (1/5) := by simp [pbarA]
  have hT : pbarA f true = f * (41/50) + (1 - f) * (1/5) := by simp [pbarA]
  rw [hF, hT]
  unfold sc
  have hp0 : (9/50 : ℝ) ≤ f * (9/50) + (1 - f) * (1/5) := by nlinarith
  have hp1 : f * (41/50) + (1 - f) * (1/5) ≤ 41/50 := by nlinarith
  have hp1pos : 0 < f * (41/50) + (1 - f) * (1/5) := by nlinarith
  have hq0 : (204/250 : ℝ) ≤ 1 - (f * (9/50) + (1 - f) * (1/5)) := by nlinarith
  have hq1 : 1 - (f * (41/50) + (1 - f) * (1/5)) ≤ 76/250 := by nlinarith
  have hq1pos : 0 < 1 - (f * (41/50) + (1 - f) * (1/5)) := by nlinarith
  have l0 := Real.log_le_log (by norm_num) hp0
  have l1 := Real.log_le_log hp1pos hp1
  have l2 := Real.log_le_log (by norm_num) hq0
  have l3 := Real.log_le_log hq1pos hq1
  have e1 : Real.log (9/41) = Real.log (9/50) - Real.log (41/50) := by
    rw [← Real.log_div (by norm_num) (by norm_num)]; norm_num
  have e2 : Real.log (51/19) = Real.log (204/250) - Real.log (76/250) := by
    rw [← Real.log_div (by norm_num) (by norm_num)]; norm_num
  rw [e1, e2]
  linarith

theorem caseA_c0_pos : 0 < (1/5) * Real.log (9/41) + (4/5) * Real.log (51/19) := by
  have h : (1/5 : ℝ) * Real.log (9/41) + (4/5) * Real.log (51/19)
      = (1/5) * Real.log ((9/41) * (51/19) ^ 4) := by
    rw [Real.log_mul (by norm_num) (by positivity), Real.log_pow]; push_cast; ring
  rw [h]
  apply mul_pos (by norm_num)
  apply Real.log_pos
  norm_num

/-- caso B: fracción f de expertos P1 (9/20, 1/20) y 1 − f de P2 (1/5, 19/20) -/
noncomputable def pbarB (f : ℝ) (r : Bool) : ℝ :=
  f * (if r then 9/20 else 1/20) + (1 - f) * (if r then 1/5 else 19/20)

theorem caseB_gain (f : ℝ) (h0 : 3/10 ≤ f) (h1 : f ≤ 2/5) :
    (19 * Real.log (55/136) + 127 * Real.log (70/41)) / 400
      ≤ (146/400) * (sc (19/146) (pbarB f true) - sc (19/146) (pbarB f false)) := by
  have hT : pbarB f true = f * (9/20) + (1 - f) * (1/5) := by simp [pbarB]
  have hF : pbarB f false = f * (1/20) + (1 - f) * (19/20) := by simp [pbarB]
  rw [hT, hF]
  unfold sc
  have ha : (11/40 : ℝ) ≤ f * (9/20) + (1 - f) * (1/5) := by nlinarith
  have hc : f * (1/20) + (1 - f) * (19/20) ≤ 17/25 := by nlinarith
  have hcpos : 0 < f * (1/20) + (1 - f) * (19/20) := by nlinarith
  have hna : (7/10 : ℝ) ≤ 1 - (f * (9/20) + (1 - f) * (1/5)) := by nlinarith
  have hnc : 1 - (f * (1/20) + (1 - f) * (19/20)) ≤ 41/100 := by nlinarith
  have hncpos : 0 < 1 - (f * (1/20) + (1 - f) * (19/20)) := by nlinarith
  have l0 := Real.log_le_log (by norm_num) ha
  have l1 := Real.log_le_log hcpos hc
  have l2 := Real.log_le_log (by norm_num) hna
  have l3 := Real.log_le_log hncpos hnc
  have e1 : Real.log (55/136) = Real.log (11/40) - Real.log (17/25) := by
    rw [← Real.log_div (by norm_num) (by norm_num)]; norm_num
  have e2 : Real.log (70/41) = Real.log (7/10) - Real.log (41/100) := by
    rw [← Real.log_div (by norm_num) (by norm_num)]; norm_num
  rw [e1, e2]
  linarith

theorem caseB_c1_pos : 0 < 19 * Real.log (55/136) + 127 * Real.log (70/41) := by
  have h : 19 * Real.log (55/136) + 127 * Real.log (70/41)
      = Real.log ((55/136) ^ 19 * (70/41) ^ 127) := by
    rw [Real.log_mul (by positivity) (by positivity), Real.log_pow, Real.log_pow]; push_cast; ring
  rw [h]
  apply Real.log_pos
  norm_num

/-- la creencia ex ante del caso B sale de P1, P2 y w = 7/20: P(A₁ = 0, A_t = y) para y = 1 y y = 0 -/
theorem caseB_mixture :
    (7/20 : ℚ) * ((19/20) * (1/20)) + (13/20) * ((1/20) * (19/20)) = 19/400 ∧
    (7/20 : ℚ) * ((19/20) * (19/20)) + (13/20) * ((1/20) * (1/20)) = 127/400 := by
  constructor <;> norm_num

/-- variante Algoritmo 1 (media de logaritmos) en el caso A: ganancia f·((4/5)·log(41/9) + (1/5)·log(9/41)) > 0 -/
theorem alg1_caseA_pos (f : ℝ) (hf : 0 < f) :
    0 < f * ((4/5) * Real.log (41/9) + (1/5) * Real.log (9/41)) := by
  have hinv : Real.log (9/41) = - Real.log (41/9) := by
    rw [← Real.log_inv]; norm_num
  have hpos : 0 < Real.log (41/9) := Real.log_pos (by norm_num)
  rw [hinv]
  apply mul_pos hf
  linarith

end AaNash.GD01

#print axioms AaNash.GD01.caseA_gain
#print axioms AaNash.GD01.caseA_c0_pos
#print axioms AaNash.GD01.caseB_gain
#print axioms AaNash.GD01.caseB_c1_pos
#print axioms AaNash.GD01.caseB_mixture
#print axioms AaNash.GD01.alg1_caseA_pos
