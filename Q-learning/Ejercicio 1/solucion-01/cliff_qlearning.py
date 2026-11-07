#!/usr/bin/env python3
"""Ejercicio 1 — Q-learning tabular en Cliff Walking (Sutton & Barto, 4×12).

Uso:
    python cliff_qlearning.py              # corrida reportada (semilla 0)
    python cliff_qlearning.py --seed 7     # otra semilla
    python cliff_qlearning.py --no-plot    # sin matplotlib

Salidas (en esta carpeta):
    recompensas_por_episodio.csv   episodio, recompensa, media móvil (10)
    curva_recompensa.png           curva cruda + media móvil
"""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Entorno (libro): 4 filas × 12 columnas, fila 0 arriba.
# ---------------------------------------------------------------------------
ROWS, COLS = 4, 12
START = (3, 0)
GOAL = (3, 11)
CLIFF = {(3, c) for c in range(1, 11)}

# Orden fijo de acciones: también es el orden de desempate en argmax.
ACTIONS = ("N", "E", "S", "W")
DELTA = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

STEP_REWARD = -1.0
CLIFF_REWARD = -100.0


def step(state: tuple[int, int], action: str) -> tuple[tuple[int, int], float, bool]:
    """Devuelve (s', r, terminado).

    - Salirse del mapa: se queda en la misma casilla, r = −1.
    - Caer al acantilado: r = −100 y s' = S; el episodio NO termina.
    - Entrar a G: r = −1 y el episodio termina.
    """
    r, c = state
    dr, dc = DELTA[action]
    nr, nc = r + dr, c + dc
    if not (0 <= nr < ROWS and 0 <= nc < COLS):
        nr, nc = r, c
    nxt = (nr, nc)
    if nxt in CLIFF:
        return START, CLIFF_REWARD, False
    if nxt == GOAL:
        return GOAL, STEP_REWARD, True
    return nxt, STEP_REWARD, False


def nonterminal_states() -> list[tuple[int, int]]:
    """Estados alcanzables y no terminales (las casillas C nunca se ocupan)."""
    return [
        (r, c)
        for r in range(ROWS)
        for c in range(COLS)
        if (r, c) != GOAL and (r, c) not in CLIFF
    ]


# ---------------------------------------------------------------------------
# Q-learning
# ---------------------------------------------------------------------------
QTable = dict[tuple[int, int], dict[str, float]]


def empty_q() -> QTable:
    return {s: {a: 0.0 for a in ACTIONS} for s in nonterminal_states()}


def argmax_action(Q: QTable, s: tuple[int, int]) -> str:
    """Máximo de Q(s, ·); en empate gana la primera acción de ACTIONS (N, E, S, W)."""
    best = ACTIONS[0]
    for a in ACTIONS[1:]:
        if Q[s][a] > Q[s][best]:
            best = a
    return best


def epsilon_greedy(Q: QTable, s: tuple[int, int], eps: float, rng: random.Random) -> str:
    if rng.random() < eps:
        return rng.choice(ACTIONS)
    return argmax_action(Q, s)


def q_update(
    Q: QTable,
    s: tuple[int, int],
    a: str,
    r: float,
    s2: tuple[int, int],
    done: bool,
    alpha: float,
    gamma: float,
) -> tuple[float, float, float]:
    """Q(s,a) ← Q(s,a) + α [ r + γ max_a' Q(s',a') − Q(s,a) ].

    Si s' es terminal (G) el máximo futuro es 0. Si s' es S tras caer,
    S es un estado normal y se usa max_a' Q(S, a').
    Devuelve (Q viejo, blanco TD, Q nuevo).
    """
    future = 0.0 if done else max(Q[s2].values())
    target = r + gamma * future
    old = Q[s][a]
    Q[s][a] = old + alpha * (target - old)
    return old, target, Q[s][a]


def train(
    episodes: int,
    alpha: float,
    gamma: float,
    eps: float,
    seed: int,
    max_steps: int,
) -> tuple[QTable, list[float], list[int], int]:
    rng = random.Random(seed)
    Q = empty_q()
    returns: list[float] = []
    falls: list[int] = []
    truncated = 0
    for _ in range(episodes):
        s = START
        G = 0.0
        n_falls = 0
        done = False
        for _t in range(max_steps):
            a = epsilon_greedy(Q, s, eps, rng)
            s2, r, done = step(s, a)
            q_update(Q, s, a, r, s2, done, alpha, gamma)
            G += r
            if r == CLIFF_REWARD:
                n_falls += 1
            s = s2
            if done:
                break
        if not done:
            truncated += 1
        returns.append(G)
        falls.append(n_falls)
    return Q, returns, falls, truncated


def greedy_rollout(Q: QTable, max_steps: int) -> tuple[list[tuple[int, int]], list[str], float, bool]:
    """Recorre desde S con ε = 0. Devuelve (camino, acciones, retorno, llegó a G)."""
    s = START
    path = [s]
    acts: list[str] = []
    G = 0.0
    for _ in range(max_steps):
        a = argmax_action(Q, s)
        s, r, done = step(s, a)
        acts.append(a)
        path.append(s)
        G += r
        if done:
            return path, acts, G, True
    return path, acts, G, False


# ---------------------------------------------------------------------------
# Impresión
# ---------------------------------------------------------------------------
ARROWS = {"N": "↑", "E": "→", "S": "↓", "W": "←"}


def grid_policy(Q: QTable, path: list[tuple[int, int]] | None = None) -> str:
    """Flechas greedy en toda la cuadrícula; [x] marca las casillas del camino S → G."""
    on_path = set(path or [])
    lines = ["fila\\col " + "".join(f"{c:^4}" for c in range(COLS))]
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            s = (r, c)
            if s == GOAL:
                mark = "G"
            elif s in CLIFF:
                mark = "C"
            else:
                mark = ARROWS[argmax_action(Q, s)]
                if s == START:
                    mark = "S" + mark
            cells.append(f"[{mark}]" if s in on_path and s != GOAL else f" {mark} ")
        lines.append(f"{r:<9}" + "".join(f"{x:^4}" for x in cells))
    return "\n".join(lines)


def moving_average(xs: list[float], w: int) -> list[float]:
    out = []
    for i in range(len(xs)):
        window = xs[max(0, i - w + 1): i + 1]
        out.append(sum(window) / len(window))
    return out


def sanity_checks() -> None:
    """Los tres casos a mano que pide el ejercicio."""
    assert step(START, "N") == ((2, 0), -1.0, False), "N desde S"
    assert step(START, "E") == (START, -100.0, False), "E desde S (cae)"
    assert step((2, 11), "S") == (GOAL, -1.0, True), "S desde (2,11)"
    assert step(START, "W") == (START, -1.0, False), "W desde S (borde)"
    assert step(START, "S") == (START, -1.0, False), "S desde S (borde)"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--episodes", type=int, default=500)
    p.add_argument("--alpha", type=float, default=0.5)
    p.add_argument("--gamma", type=float, default=1.0)
    p.add_argument("--epsilon", type=float, default=0.1)
    p.add_argument("--max-steps", type=int, default=200)
    p.add_argument("--window", type=int, default=10, help="ventana de la media móvil")
    p.add_argument("--no-plot", action="store_true")
    args = p.parse_args()

    sanity_checks()
    print("Comprobaciones a mano del entorno")
    print("-" * 60)
    for s, a in ((START, "N"), (START, "E"), ((2, 11), "S")):
        s2, r, d = step(s, a)
        print(f"  s={s}  a={a}  ->  s'={s2}  r={r:g}  terminado={'sí' if d else 'no'}")
    print()

    print(
        f"α = {args.alpha}   γ = {args.gamma}   ε = {args.epsilon}   episodios = {args.episodes}   "
        f"tope = {args.max_steps}   semilla = {args.seed}"
    )
    print(f"Desempate en argmax: {', '.join(ACTIONS)} (gana la primera)")
    print()

    Q, returns, falls, truncated = train(
        args.episodes, args.alpha, args.gamma, args.epsilon, args.seed, args.max_steps
    )
    path, acts, G, reached = greedy_rollout(Q, args.max_steps)

    print("Política greedy (ε = 0); [x] = camino recorrido desde S")
    print("-" * 60)
    print(grid_policy(Q, path))
    print()
    print("Camino S → G:", " → ".join(f"({r},{c})" for r, c in path))
    print("Acciones:     ", " ".join(acts))
    print(f"Pasos = {len(acts)}   retorno greedy = {G:g}   llegó a G = {'sí' if reached else 'no'}")
    print()

    ma = moving_average(returns, args.window)
    print("Entrenamiento (ε-greedy encendida)")
    print("-" * 60)
    print(f"  episodios cortados por el tope: {truncated}")
    print(f"  caídas totales al acantilado:   {sum(falls)}")
    for lo, hi in ((0, 10), (10, 50), (50, 100), (100, 200), (200, 300), (300, 400), (400, 500)):
        seg = returns[lo:hi]
        if seg:
            print(f"  media episodios {lo + 1:>3}-{hi:<3}: {sum(seg) / len(seg):8.2f}")
    print(f"  mejor episodio: {max(returns):g}   peor: {min(returns):g}")
    print(f"  Q(S,N) = {Q[START]['N']:.3f}   Q(S,E) = {Q[START]['E']:.3f}")
    print()

    csv_path = HERE / "recompensas_por_episodio.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["episodio", "recompensa", f"media_movil_{args.window}", "caidas"])
        for i, (g, m, f) in enumerate(zip(returns, ma, falls), 1):
            w.writerow([i, f"{g:g}", f"{m:.2f}", f])
    print(f"Serie guardada en {csv_path.name}")

    if not args.no_plot:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        x = range(1, len(returns) + 1)
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(x, returns, color="#9bb7d4", lw=0.8, label="recompensa por episodio")
        ax.plot(x, ma, color="#1f4e79", lw=2, label=f"media móvil ({args.window})")
        ax.axhline(-13, color="#c0392b", ls="--", lw=1.2, label="greedy óptima (−13)")
        ax.set_ylim(-110, 0)
        ax.set_xlim(1, len(returns))
        ax.set_xlabel("Episodio")
        ax.set_ylabel("Suma de recompensas en el episodio")
        ax.set_title(f"Q-learning en Cliff Walking  (α={args.alpha}, ε={args.epsilon}, semilla={args.seed})")
        ax.grid(alpha=0.3)
        ax.legend(loc="lower right")
        fig.tight_layout()
        png = HERE / "curva_recompensa.png"
        fig.savefig(png, dpi=130)
        print(f"Gráfica guardada en {png.name}")


if __name__ == "__main__":
    main()
