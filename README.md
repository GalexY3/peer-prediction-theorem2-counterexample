# Larger Crowds Do Not Restore Truthfulness in Peer Prediction with Heterogeneous Priors

**Contents.** This archive contains a machine-checked counterexample to Theorem 2 of Qiu, Carroll and Allen, "Truthfulness Despite Weak Supervision: Evaluating and Training LLMs Using Peer Prediction" (ICLR 2026, arXiv:2601.20299). It includes the note, the Lean proofs, the exact-check script, the results and the preregistration.

**DOI.** [10.5281/zenodo.24517882](https://doi.org/10.5281/zenodo.24517882) (Zenodo, version v1.0.0).

**Author.** Alejandro Panera Pascual (Universidad de Salamanca), ORCID 0009-0008-5194-7399.

**Scope.** Peer prediction for language models, its construction, Theorem 2 and the experiments are the work of Qiu, Carroll and Allen. This archive examines only Theorem 2, the heterogeneous-prior guarantee. Theorem 1 (common prior) is not affected.

## Contents

| Path | What it is |
|---|---|
| `paper/main.pdf`, `paper/main.tex` | The note (6 pages) |
| `lean/PeerPredictionGD01.lean` | Lean 4 + Mathlib proofs: `caseA_gain`, `caseA_c0_pos`, `caseB_gain`, `caseB_c1_pos`, `caseB_mixture`, `alg1_caseA_pos` |
| `lean/LEAN_AXIOMS_GD01.txt` | Compilation receipt: `#print axioms` shows only `propext`, `Classical.choice` and `Quot.sound`; no `sorry`; SHA-256 of the Lean file |
| `code/gd01_exact.py` | Exact checks V1–V6: brute force over all answer profiles for n = 2, 3, 4 with rational arithmetic, Assumption 1 constants, binomial probabilities, theorem threshold, step (19) |
| `results/` | Frozen outputs `gd01_exact.json` and `gd01_exact_stdout.txt` |
| `provenance/` | Theory, preregistration with the exact Lean statements, SHA-256 freeze, and report with addenda. In Spanish. The freeze (commit 7350872f of the author's private research repository) was made before the proofs were written |

## Reproduce

### 1. Lean

Toolchain `leanprover/lean4:v4.36.0`, Mathlib at commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`. The file imports only Mathlib. Inside a Lake project with that Mathlib:

```
lake env lean PeerPredictionGD01.lean
```

The file ends with `#print axioms` for each declaration.

### 2. Exact checks

Python ≥ 3.10, standard library only:

```
python -I -X utf8 gd01_exact.py out.json
```

The output should match `results/gd01_exact.json`.

## Main numbers

**Case A (each participant knows its own prior).** 𝒟 = 0.9·Lat + 0.1·Ind with binary answers:
- **Lat:** a latent truth Z ~ Bern(1/2), with each answer equal to Z with probability 9/10.
- **Ind:** answers i.i.d. Bern(1/5).
- **Assumption 1:** holds with I₀ ≈ 1.02 and L₀ ≈ 0.92.
- **The deviation.** For every fraction of Lat experts in [4/5, 1], a participant with prior Ind gains by always answering 0:
  - at least c₀ = (1/5)·log(9/41) + (4/5)·log(51/19) ≈ 0.487 nats per target, conditional on its answer being 1;
  - at least c₀/5 ≈ 0.097 nats averaged over its own answer.
- **Against the theorem.** Neither bound depends on m or n, so honest reporting is not an ε-equilibrium for any ε < 0.097 for large m and n. The theorem's own threshold for ε = c₀/10 and δ = 0.05 is m, n ≥ 2791.

**Case B (deviations may not depend on the participant's own prior; ex ante).** With non-exchangeable "star" priors, always answering 1 gains at least 0.127 ex ante.

**Algorithm 1 variant.** The gain is f·(3/5)·log(41/9) > 0.

## Notes on the provenance files

- **INFORME_GD01.md.** Its main text states the failure "for every ε < 0.487". That holds for the interim reading, conditional on the participant's own answer. A dated addendum in the same file, reproduced in the note, gives the averaged bound c₀/5 ≈ 0.097.
- **Threshold for ε = c₀/2.** The value is 493.2, so the smallest integer that meets it is 494.
- **`gd01_exact.py`, V6.** The frozen script contains a descriptive string saying that the deviation beats honesty "by more than c₀". The computed gap at f = 9/10 is 0.138, which exceeds c₀/5 but not c₀. The numbers in the JSON are correct; only the string is imprecise.
- **Published version.** The statement of Theorem 2 and the proof steps discussed were checked against both arXiv:2601.20299v1 and the published OpenReview version (forum mdw0vvRBEL), and are the same in both.

## License

- Text, figures and data: CC BY 4.0.
- Code written for this archive (`code/`, `lean/`): MIT.
