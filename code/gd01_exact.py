"""GD01: comprobacion exacta del contraejemplo al Teorema 2 de Qiu, Carroll y Allen (ICLR 2026, arXiv 2601.20299 v1).

Uso: python -I -X utf8 gd01_exact.py OUT_JSON

Modelo (sec. 3.3 y Algoritmo 2 del articulo): respuestas binarias; n participantes; m expertos honestos con priors sacados
de D. Puntuacion del emisor s: (1/(n-1)) sum_{t != s} [log pbar(A_t | A_s) - log qbar(A_t)], con pbar y qbar MEDIAS
ARITMETICAS sobre expertos de P_j(A_t | A_s) y P_j(A_t). Los objetivos responden con honestidad.

V1 (caso A, lectura I): D_A = 0,9 Lat + 0,1 Ind (intercambiables para todo n).
   Lat: Z ~ Bern(1/2), A_i | Z iid con P(A_i = Z) = 9/10.  Ind: A_i iid Bern(1/5).
   Un participante de tipo Ind gana con "siempre 0" frente a la honestidad, para toda fraccion f de expertos Lat en [4/5, 1].
V4 (caso B, lectura II): priors en estrella que distinguen al participante 1 (P1, P2, w = 7/20); "siempre 1" gana ex ante.
V5: variante Algoritmo 1 (media de logaritmos) en el caso A.
V6: el paso (19) de la prueba (media aritmetica frente a media geometrica) falla en el caso A.
Comprobacion independiente: fuerza bruta sobre todos los perfiles de A^n (n = 2, 3, 4) con probabilidades racionales exactas.
"""
import itertools
import json
import math
import sys
from fractions import Fraction as F

OUT = sys.argv[1]
res = {}


# ---------- priors como funciones de probabilidad sobre A^n (exactas) ----------
def lat_prob(prof, keep=F(9, 10)):
    """Lat: Z ~ Bern(1/2); cada A_i = Z con probabilidad keep, independientes dado Z."""
    tot = F(0)
    for z in (0, 1):
        p = F(1, 2)
        for a in prof:
            p *= keep if a == z else 1 - keep
        tot += p
    return tot


def ind_prob(prof, p1=F(1, 5)):
    p = F(1)
    for a in prof:
        p *= p1 if a == 1 else 1 - p1
    return p


def star_prob(prof, a1, r1, r0):
    """Estrella centrada en el participante 0: A_0 ~ Bern(a1); los demas iid dado A_0 con P(A_t = 1 | A_0) = r1 o r0."""
    x = prof[0]
    p = a1 if x == 1 else 1 - a1
    r = r1 if x == 1 else r0
    for a in prof[1:]:
        p *= r if a == 1 else 1 - r
    return p


def marg_pair(prob, n, s, t):
    """Distribucion conjunta exacta de (A_s, A_t) sumando sobre A^n."""
    j = {(a, b): F(0) for a in (0, 1) for b in (0, 1)}
    for prof in itertools.product((0, 1), repeat=n):
        j[(prof[s], prof[t])] += prob(prof)
    return j


def cond(j, x):
    z = j[(x, 0)] + j[(x, 1)]
    return [j[(x, 0)] / z, j[(x, 1)] / z]


def marg(j):
    return [j[(0, 0)] + j[(1, 0)], j[(0, 1)] + j[(1, 1)]]   # marginal de A_t


# ---------- puntuacion esperada del emisor por fuerza bruta ----------
def expected_score(n, s, belief_prob, experts, weights, strategy):
    """E_{perfil ~ creencia del emisor}[ (1/(n-1)) sum_t log pbar(A_t|r) - log qbar(A_t) ], r = strategy(A_s).
    experts: lista de funciones de probabilidad sobre A^n; weights: sus pesos (media aritmetica)."""
    pairs = {}
    for t in range(n):
        if t == s:
            continue
        js = [marg_pair(e, n, s, t) for e in experts]
        pb = {x: [sum(w * cond(j, x)[y] for w, j in zip(weights, js)) for y in (0, 1)] for x in (0, 1)}
        qb = [sum(w * marg(j)[y] for w, j in zip(weights, js)) for y in (0, 1)]
        pairs[t] = (pb, qb)
    tot = 0.0
    for prof in itertools.product((0, 1), repeat=n):
        pr = belief_prob(prof)
        if pr == 0:
            continue
        r = strategy(prof[s])
        sc = sum(math.log(pairs[t][0][r][prof[t]]) - math.log(pairs[t][1][prof[t]]) for t in pairs) / (n - 1)
        tot += float(pr) * sc
    return tot


HONEST, ALWAYS0, ALWAYS1, FLIP = (lambda a: a), (lambda a: 0), (lambda a: 1), (lambda a: 1 - a)

# ---------- V1: caso A ----------
def gainA_closed(f):
    """Formula cerrada (por objetivo) de la ganancia de "siempre 0" para el tipo Ind con senal 1."""
    f = F(f)
    pb1_1, pb1_0 = (10 + 31 * f) / 50, (10 - f) / 50       # pbar(A_t=1 | r=1), pbar(A_t=1 | r=0)
    return (F(1, 5) * (math.log(pb1_0) - math.log(pb1_1)) + F(4, 5) * (math.log(1 - pb1_0) - math.log(1 - pb1_1)))


res['V1'] = {'c0_cota_Lean': (1 / 5) * math.log(9 / 41) + (4 / 5) * math.log(51 / 19), 'por_f': {}, 'fuerza_bruta': {}}
for f in (F(4, 5), F(17, 20), F(9, 10), F(19, 20), F(1)):
    res['V1']['por_f'][str(f)] = float(gainA_closed(f))
for n in (2, 3, 4):
    for f in (F(4, 5), F(9, 10), F(1)):
        experts, weights = [lambda p: lat_prob(p), lambda p: ind_prob(p)], [f, 1 - f]
        if f == 1:
            experts, weights = experts[:1], [F(1)]
        h = expected_score(n, 0, ind_prob, experts, weights, HONEST)
        d = expected_score(n, 0, ind_prob, experts, weights, ALWAYS0)
        # ganancia por objetivo = media sobre la senal propia (P(senal 1) = 1/5) de la ganancia condicionada
        res['V1']['fuerza_bruta']['n=%d,f=%s' % (n, f)] = {'honesto': h, 'siempre0': d, 'ganancia': d - h,
                                                          'formula_x_P(senal1)': float(gainA_closed(f)) / 5}
res['V1']['min_formula_en_rejilla_[4/5,1]'] = min(float(gainA_closed(F(k, 1000))) for k in range(800, 1001))

# ---------- V2: Supuesto 1 para D_A ----------
def assumption1(probs, n=3):
    I0, L0 = 0.0, 0.0
    for p in probs:
        j = marg_pair(p, n, 0, 1)
        mi = [j[(0, 0)] + j[(0, 1)], j[(1, 0)] + j[(1, 1)]]
        mt = marg(j)
        for a in (0, 1):
            for b in (0, 1):
                I0 = max(I0, abs(math.log(j[(a, b)] / (mi[a] * mt[b]))))
    for p, q in itertools.permutations(probs, 2):
        jp, jq = marg_pair(p, n, 0, 1), marg_pair(q, n, 0, 1)
        for a in (0, 1):
            L0 = max(L0, abs(math.log((jp[(a, 0)] + jp[(a, 1)]) / (jq[(a, 0)] + jq[(a, 1)]))),
                     abs(math.log(marg(jp)[a] / marg(jq)[a])))
    return I0, L0


I0A, L0A = assumption1([lat_prob, ind_prob])
res['V2'] = {'I0': I0A, 'L0': L0A}

# ---------- V3: probabilidades (exactas) ----------
def binom_tail_outside(m, p, lo, hi):
    """P(K/m fuera de [lo, hi]) con K ~ Bin(m, p), exacta."""
    p = F(p)
    out = F(0)
    for k in range(m + 1):
        if not (F(lo) <= F(k, m) <= F(hi)):
            out += math.comb(m, k) * p ** k * (1 - p) ** (m - k)
    return float(out)


res['V3'] = {'P_algun_Ind_entre_n': {n: 1 - 0.9 ** n for n in (5, 10, 20, 50, 100)},
             'P_fraccion_Lat_fuera_[4/5,1]': {m: binom_tail_outside(m, F(9, 10), F(4, 5), 1) for m in (50, 100, 200, 500, 1000)}}
eps = res['V1']['c0_cota_Lean'] / 2
delta = 0.05
res['V3']['umbral_Teorema2_m_n_para_eps=c0/2_delta=0,05'] = 16 * (I0A + L0A) / eps * math.log((I0A + L0A) / eps + 2 / delta)

# ---------- V4: caso B (estrella; lectura II) ----------
P1 = dict(a1=F(1, 20), r1=F(9, 20), r0=F(1, 20))
P2 = dict(a1=F(19, 20), r1=F(1, 5), r0=F(19, 20))
w = F(7, 20)


def gainB_closed(f):
    f = F(f)
    a, b, c, d = (4 + 5 * f) / 20, (19 - 18 * f) / 20, (16 - 5 * f) / 20, (1 + 18 * f) / 20
    return (19 * (math.log(a) - math.log(b)) + 127 * (math.log(c) - math.log(d))) / 400


res['V4'] = {'c1_cota_Lean': (19 * math.log(55 / 136) + 127 * math.log(70 / 41)) / 400,
             'por_f': {str(f): gainB_closed(f) for f in (F(3, 10), F(7, 20), F(2, 5))}, 'fuerza_bruta': {},
             'min_formula_en_rejilla_[3/10,2/5]': min(gainB_closed(F(k, 1000)) for k in range(300, 401)),
             'P_fraccion_fuera_[3/10,2/5]': {m: binom_tail_outside(m, w, F(3, 10), F(2, 5)) for m in (200, 500, 1000, 2000)}}
mixB = lambda prof: w * star_prob(prof, **P1) + (1 - w) * star_prob(prof, **P2)
for n in (2, 3, 4):
    for f in (F(3, 10), F(7, 20), F(2, 5)):
        ex = [lambda p: star_prob(p, **P1), lambda p: star_prob(p, **P2)]
        h = expected_score(n, 0, mixB, ex, [f, 1 - f], HONEST)
        d = expected_score(n, 0, mixB, ex, [f, 1 - f], ALWAYS1)
        res['V4']['fuerza_bruta']['n=%d,f=%s' % (n, f)] = {'honesto': h, 'siempre1': d, 'ganancia': d - h,
                                                          'formula': gainB_closed(f)}
I0B, L0B = assumption1([lambda p: star_prob(p, **P1), lambda p: star_prob(p, **P2)])
res['V4']['Supuesto1'] = {'I0': I0B, 'L0': L0B}

# ---------- V5: variante Algoritmo 1 (media de logaritmos) en el caso A ----------
res['V5'] = {'ganancia_formula_f*(3/5)*log(41/9)': {str(f): float(f) * 0.6 * math.log(41 / 9) for f in (F(4, 5), F(9, 10), F(1))}}
lat2 = marg_pair(lat_prob, 2, 0, 1)
ind2 = marg_pair(ind_prob, 2, 0, 1)
for f in (F(4, 5), F(9, 10)):
    def sc(r, bel=(F(4, 5), F(1, 5))):
        return sum(float(bel[y]) * (float(f) * math.log(cond(lat2, r)[y]) + float(1 - f) * math.log(cond(ind2, r)[y]))
                   for y in (0, 1))
    res['V5']['directa_f=%s' % f] = sc(0) - sc(1)

# ---------- V6: el paso (19) en el caso A (f = 9/10, m -> infinito) ----------
# LHS(17) honesto con media aritmetica; RHS(19) con la media geometrica normalizada P_bar de log P_bar = E_D log P.
def geo_pair(js, ws):
    g = {k: math.exp(sum(float(wt) * math.log(j[k]) for j, wt in zip(js, ws))) for k in js[0]}
    z = sum(g.values())
    return {k: v / z for k, v in g.items()}


ws = [F(9, 10), F(1, 10)]
jsA = [lat2, ind2]
gp = geo_pair(jsA, ws)
pbA = {x: [sum(float(wt) * float(cond(j, x)[y]) for wt, j in zip(ws, jsA)) for y in (0, 1)] for x in (0, 1)}
qbA = [sum(float(wt) * float(marg(j)[y]) for wt, j in zip(ws, jsA)) for y in (0, 1)]
gcond = {x: [gp[(x, y)] / (gp[(x, 0)] + gp[(x, 1)]) for y in (0, 1)] for x in (0, 1)}
gmarg = [gp[(0, y)] + gp[(1, y)] for y in (0, 1)]
belief = {(a, b): float(ind2[(a, b)]) for a in (0, 1) for b in (0, 1)}  # creencia del participante Ind
lhs = sum(pr * (math.log(pbA[a][b]) - math.log(qbA[b])) for (a, b), pr in belief.items())
rhs = sum(pr * (math.log(gcond[a][b]) - math.log(gmarg[b])) for (a, b), pr in belief.items())
dev_arith = sum(pr * (math.log(pbA[0][b]) - math.log(qbA[b])) for (a, b), pr in belief.items())
res['V6'] = {'LHS17_honesto_media_aritmetica': lhs, 'RHS19_media_geometrica': rhs, 'LHS_menos_RHS': lhs - rhs,
             'desviacion_siempre0_media_aritmetica': dev_arith,
             'nota': 'el paso (19) exige LHS >= RHS - eps/2 y el (22) acota la desviacion por el mismo puente; '
                     'aqui la desviacion supera al honesto en mas de c0'}

with open(OUT, 'wb') as fh:
    fh.write(json.dumps(res, indent=1, ensure_ascii=False).encode('utf-8'))
print(json.dumps(res, indent=1, ensure_ascii=False))
