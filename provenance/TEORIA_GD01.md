# GD01 · Medir el acuerdo premia no informar: el Teorema 2 de Qiu, Carroll y Allen (ICLR 2026)

**Fecha:** 24/11/2026 (portátil, ala A10).

**Origen:** el sondeo `novelty/2026-11-24_scout_goodhart/report.md`, que buscaba el caso de «medir altera el comportamiento» (Goodhart) en juegos.

**Encaje en el carril:** auditar teoremas publicados que llevan a varios agentes una garantía que solo vale con uno, o con creencias comunes. Es el mismo patrón que AA/Nash y TAR².

## 1. El resultado auditado

**Fuente:** Qiu, Carroll y Allen, «Truthfulness Despite Weak Supervision: Evaluating and Training LLMs Using Peer Prediction», ICLR 2026, arXiv 2601.20299, v1 del 28/01/2026 (la única en arXiv el 24/11/2026). Se leyeron enteras las secciones 3.1–3.3 y el apéndice C.2.

**Mecanismo (Algoritmo 2):**
- n participantes dan respuestas Aᵢ y m expertos dan probabilidades Prⱼ(A_t) y Prⱼ(A_t | A_s).
- El emisor s recibe (1/(n−1))·Σ_{t≠s} [log p̄(A_t | A_s) − log q̄(A_t)], donde p̄ y q̄ son medias **aritméticas** sobre los expertos.

**Teorema 2** (texto literal resumido):
- Los priors de participantes y expertos se sacan de forma independiente de una misma 𝒟 sobre [0,1]^{n|𝒜|}.
- Bajo el Supuesto 1 (I₀ acota el PMI dentro de cada prior y L₀ el cociente de marginales entre priors) y con m, n ≥ 16(I₀+L₀)/ε·log((I₀+L₀)/ε + |𝒜|/δ), con probabilidad 1 − δ el perfil en el que participantes y expertos son honestos es, «ex ante (when 𝒟 and the instantiation of all 𝒫ⱼᴶ are known by the agents)», un ε-equilibrio bayesiano-Nash.
- Los autores lo presentan como «novel and may be of independent interest», y dicen que hace intuitivamente que «tailored lies that target specific individuals» dejen de compensar.

**Afirmaciones que lo acompañan:** el mecanismo «penalizes both deceptive answers and uninformative ones», y los modelos entrenados con esas puntuaciones están «incentivised to converge upon honest and informative policies».

## 2. Por qué falla

**La mejor respuesta del emisor:**
- El término log q̄ no depende del informe r.
- El emisor con creencia P_s maximiza Σ_y P_s(y | a)·log p̄(y | r): elige el informe r cuya predicción experta media p̄(·|r) está más cerca, en divergencia KL, de su propia creencia P_s(·|a).
- La honestidad (r = a) solo es la mejor respuesta si p̄(·|a) es la más cercana.

**El argumento de los autores no lo arregla:**
- Una multitud grande de expertos hace que p̄ converja a la media de 𝒟, pero no acerca p̄ a la creencia de **un** participante cuyo prior difiere de esa media.
- La «mentira a medida» no apunta a un individuo, sino a la **mayoría** de los expertos. Más expertos la estabilizan en lugar de diluirla.

**La prueba (C.2):**
- El paso (19) sustituye, «por Hoeffding», el log de la media aritmética de las probabilidades de los expertos por el PMI bajo P̄, con log P̄ = E_𝒟[log P]. Es una media geométrica, sin normalizar. Hoeffding no autoriza ese cambio y la diferencia de Jensen no desaparece con m.
- El paso a n finito («(20) is the mean of (17) over the choice of {𝒫ᵢᴬ}») promedia sobre el prior del propio emisor. Con eso solo compara la honestidad con desviaciones que no dependen de ese prior.

## 3. Contraejemplos

**Caso A, lectura I** (cada participante conoce su propio prior; es la notación de la prueba, E sobre 𝒫ₛᴬ):
- **La población:** 𝒟_A = 0,9·Lat + 0,1·Ind, ambos intercambiables y válidos para todo n.
  - **Lat:** Z ~ Bern(1/2) y cada Aᵢ = Z con probabilidad 9/10, independientes dado Z. Para cualquier par, P(A_t = 1 | A_s = 1) = 41/50 y P(A_t = 1 | A_s = 0) = 9/50.
  - **Ind:** Aᵢ iid Bern(1/5).
- **La mejor respuesta del participante Ind:**
  - Con una fracción f de expertos Lat, p̄(1|1) = (10 + 31f)/50 y p̄(1|0) = (10 − f)/50.
  - Un participante de tipo Ind (cree que el objetivo responde 1 con probabilidad 1/5, sea cual sea su propia respuesta) prefiere **responder siempre 0**.
  - Con señal 1, gana (1/5)·log(p̄(1|0)/p̄(1|1)) + (4/5)·log((1−p̄(1|0))/(1−p̄(1|1))). Es 0,689 con f = 9/10 y al menos 0,524 en f ∈ [4/5, 1].
- **La cota para Lean:** c₀ = (1/5)·log(9/41) + (4/5)·log(51/19) ≈ 0,487 > 0, válida para todo f ∈ [4/5, 1].
- **Por qué contradice el Teorema 2:**
  - Con m expertos, la fracción Lat cae fuera de [4/5, 1] con probabilidad exacta de 0,0094 (m = 50) a 10⁻²¹ (m = 1000).
  - Con n participantes, hay al menos uno de tipo Ind con probabilidad 1 − 0,9ⁿ → 1.
  - Como la ganancia por objetivo no depende de n ni de m, el perfil honesto **no** es ε-equilibrio para ningún ε < c₀, en contra de la conclusión del teorema para m y n grandes. El propio umbral del teorema para ε = c₀/2 y δ = 0,05 es 493.
  - El Supuesto 1 se cumple: I₀ = 1,02 y L₀ = 0,92.
- **La desviación ganadora es no informativa**, lo contrario de «penalizes … uninformative» respuestas. Con el Algoritmo 1 (media de logaritmos) también falla: la ganancia es f·(3/5)·log(41/9) > 0.

**Caso B, lectura II** (el participante no ajusta su estrategia a su propio prior; ex ante sobre 𝒟):
- Con priors intercambiables de clase latente no se encontró contraejemplo en una búsqueda exploratoria. Sí lo hay con priors que distinguen a un participante, que la hipótesis del teorema (cualquier 𝒟 sobre [0,1]^{n|𝒜|}) permite.
- **La construcción:**
  - Dos priors «en estrella» centrados en el participante 1: A₁ ~ Bern(a) y los demás, iid dado A₁, con P(A_t = 1 | A₁).
  - P1 = (1/20; 9/20; 1/20) y P2 = (19/20; 1/5; 19/20), con w = 7/20.
- **El resultado:** «responder siempre 1» gana ex ante (1/400)·[19·log(p̄(1|1)/p̄(1|0)) + 127·log(p̄(0|1)/p̄(0|0))], que vale 0,175 con f = 7/20 y al menos c₁ = (19·log(55/136) + 127·log(70/41))/400 ≈ 0,127 en f ∈ [3/10, 2/5].
- **El mecanismo:** los expertos promedian condicionales, mientras que la creencia ex ante es la condicional de la mezcla. Con marginales distintas, las dos cosas no coinciden.

## 4. Lo que no se toca

- **El Teorema 1** (prior común; es clásico, de Schoenebeck y Yu 2023).
- **Los experimentos del artículo.**
- **La afirmación sobre la convergencia del aprendizaje:** es otra pregunta, sobre la dinámica y no sobre equilibrios.
