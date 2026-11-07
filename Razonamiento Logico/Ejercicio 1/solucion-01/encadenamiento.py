#!/usr/bin/env python3
"""Ejercicio 1 — Encadenamiento hacia adelante y hacia atrás (cláusulas definidas).

Uso:
    python encadenamiento.py                                  # las 3 consultas de biblioteca.yaml
    python encadenamiento.py --query "AccesoNoche(Luis)"      # una consulta
    python encadenamiento.py --query "AccesoNoche(Luis)" --add-fact "TieneCredencial(Luis)"
    python encadenamiento.py --out trazas.txt                 # además guarda la salida
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Átomos, sustituciones y unificación
# ---------------------------------------------------------------------------
# Un término es una cadena: variable si empieza con minúscula, constante si no.
# Una sustitución es un dict {variable: término}.

_ATOM_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*(?:\(([^()]*)\))?\s*$")


@dataclass(frozen=True)
class Atom:
    pred: str
    args: tuple[str, ...]

    def __str__(self) -> str:
        return f"{self.pred}({', '.join(self.args)})" if self.args else self.pred


@dataclass(frozen=True)
class Rule:
    name: str
    body: tuple[Atom, ...]
    head: Atom

    def __str__(self) -> str:
        return f"{self.name}:  {' ∧ '.join(map(str, self.body))}  ⇒  {self.head}"


def parse_atom(text: str) -> Atom:
    m = _ATOM_RE.match(str(text))
    if not m:
        raise ValueError(f"átomo inválido: {text!r}")
    args = tuple(a.strip() for a in m.group(2).split(",")) if m.group(2) else ()
    return Atom(m.group(1), args)


def is_var(term: str) -> bool:
    return term[:1].islower()


def walk(term: str, theta: dict[str, str]) -> str:
    """Sigue la cadena de ligaduras de una variable hasta un valor final."""
    while is_var(term) and term in theta:
        term = theta[term]
    return term


def substitute(atom: Atom, theta: dict[str, str]) -> Atom:
    return Atom(atom.pred, tuple(walk(t, theta) for t in atom.args))


def unify(a: Atom, b: Atom, theta: dict[str, str]) -> dict[str, str] | None:
    """Unificador más general de dos átomos (términos planos), extendiendo theta."""
    if a.pred != b.pred or len(a.args) != len(b.args):
        return None
    theta = dict(theta)
    for s, t in zip(a.args, b.args):
        s, t = walk(s, theta), walk(t, theta)
        if s == t:
            continue
        if is_var(s):
            theta[s] = t
        elif is_var(t):
            theta[t] = s
        else:
            return None  # dos constantes distintas
    return theta


def rename(rule: Rule, k: int) -> Rule:
    """Variables frescas por cada uso de la regla: x → x_k."""

    def ren(atom: Atom) -> Atom:
        return Atom(atom.pred, tuple(f"{t}_{k}" if is_var(t) else t for t in atom.args))

    return Rule(rule.name, tuple(ren(p) for p in rule.body), ren(rule.head))


def show_binding(theta: dict[str, str], rule: Rule) -> str:
    """Sustitución sobre las variables originales de la regla (x/Ana), sin el índice."""
    variables = []
    for atom in (*rule.body, rule.head):
        for t in atom.args:
            if is_var(t) and t not in variables:
                variables.append(t)
    parts = [f"{v.rsplit('_', 1)[0]}/{walk(v, theta)}" for v in variables]
    return "{" + ", ".join(parts) + "}"


# ---------------------------------------------------------------------------
# Base de conocimiento
# ---------------------------------------------------------------------------
@dataclass
class KB:
    facts: list[Atom]
    rules: list[Rule]
    queries: list[Atom]


def load_kb(path: Path) -> KB:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    facts = [parse_atom(f) for f in raw.get("facts", [])]
    rules = [
        Rule(r["id"], tuple(parse_atom(p) for p in r["if"]), parse_atom(r["then"]))
        for r in raw.get("rules", [])
    ]
    queries = [parse_atom(q) for q in raw.get("queries", [])]
    return KB(facts, rules, queries)


# ---------------------------------------------------------------------------
# Encadenamiento hacia adelante (dirigido por los datos)
# ---------------------------------------------------------------------------
def matches(body: tuple[Atom, ...], facts: list[Atom], theta: dict[str, str]) -> list[dict[str, str]]:
    """Todas las sustituciones que satisfacen las premisas, en orden de premisas y de hechos."""
    if not body:
        return [theta]
    out = []
    for fact in facts:
        t2 = unify(substitute(body[0], theta), fact, theta)
        if t2 is not None:
            out.extend(matches(body[1:], facts, t2))
    return out


def forward_chain(kb: KB, query: Atom) -> tuple[bool, list[Atom], list[str]]:
    facts = list(kb.facts)
    new_total: list[Atom] = []
    trace = [f"Hechos iniciales: {', '.join(map(str, facts))}"]
    k = 0
    ronda = 0
    while True:
        ronda += 1
        trace.append(f"--- ronda {ronda} ---")
        snapshot = list(facts)  # hechos conocidos al empezar la ronda
        nuevos: list[Atom] = []
        for rule in kb.rules:
            k += 1
            r = rename(rule, k)
            for theta in matches(r.body, snapshot, {}):
                head = substitute(r.head, theta)
                if head in facts or head in nuevos:
                    continue
                nuevos.append(head)
                trace.append(f"  dispara {rule.name}  {show_binding(theta, r)}  ⇒  {head}")
        if not nuevos:
            trace.append("  sin átomos nuevos → punto fijo")
            break
        facts.extend(nuevos)  # se usan como premisas hasta la ronda siguiente
        new_total.extend(nuevos)

    for fact in facts:  # primera respuesta en el orden final de los hechos
        if unify(query, fact, {}) is not None:
            trace.append(f"Consulta {query}: unifica con el hecho {fact}")
            return True, new_total, trace
    trace.append(f"Consulta {query}: no unifica con ningún hecho")
    return False, new_total, trace


# ---------------------------------------------------------------------------
# Encadenamiento hacia atrás (dirigido por la meta)
# ---------------------------------------------------------------------------
def backward_chain(kb: KB, query: Atom) -> tuple[bool, list[Atom], list[str]]:
    trace: list[str] = []
    goals: list[Atom] = []
    k = [0]

    def prove(goal: Atom, theta: dict[str, str], depth: int, stack: tuple[Atom, ...]) -> dict[str, str] | None:
        """bc_or: una meta. Hechos primero, luego reglas; la primera prueba gana."""
        goal = substitute(goal, theta)
        pad = "  " * depth
        if goal in stack:
            trace.append(f"{pad}ciclo: {goal} ya está en la pila de metas → se corta")
            return None
        trace.append(f"{pad}meta   {goal}")
        if goal not in goals:
            goals.append(goal)

        for fact in kb.facts:
            t2 = unify(goal, fact, theta)
            if t2 is not None:
                trace.append(f"{pad}  ✓ hecho {fact}")
                return t2

        for rule in kb.rules:
            k[0] += 1
            r = rename(rule, k[0])
            t2 = unify(goal, r.head, theta)
            if t2 is None:
                continue
            trace.append(f"{pad}  regla {rule.name}  {show_binding(t2, r)}")
            result = prove_all(r.body, t2, depth + 2, stack + (goal,))
            if result is not None:
                return result
            trace.append(f"{pad}  ✗ {rule.name} falla para {goal}")

        trace.append(f"{pad}  ✗ falla {goal}")
        return None

    def prove_all(body: tuple[Atom, ...], theta: dict[str, str], depth: int, stack: tuple[Atom, ...]) -> dict[str, str] | None:
        """bc_and: las premisas en orden; si una falla, falla la conjunción."""
        for premise in body:
            theta = prove(premise, theta, depth, stack)
            if theta is None:
                return None
        return theta

    trace.append(f"Consulta: {query}")
    ok = prove(query, {}, 0, ()) is not None
    return ok, goals, trace


# ---------------------------------------------------------------------------
# Programa
# ---------------------------------------------------------------------------
def run(kb: KB, queries: list[Atom]) -> None:
    print("Base de conocimiento")
    print("=" * 64)
    print("Hechos:")
    for f in kb.facts:
        print(f"  {f}")
    print("Reglas (en orden):")
    for r in kb.rules:
        print(f"  {r}")

    resumen = []
    for q in queries:
        print()
        print("#" * 64)
        print(f"# CONSULTA: {q}")
        print("#" * 64)

        ok_f, nuevos, tr_f = forward_chain(kb, q)
        print("\nEncadenamiento hacia ADELANTE")
        print("-" * 64)
        print("\n".join(tr_f))
        print(f"Átomos nuevos (en orden): {', '.join(map(str, nuevos)) or '(ninguno)'}")
        print(f"Probada: {'SÍ' if ok_f else 'NO'}")

        ok_b, metas, tr_b = backward_chain(kb, q)
        print("\nEncadenamiento hacia ATRÁS")
        print("-" * 64)
        print("\n".join(tr_b))
        print(f"Metas visitadas: {', '.join(map(str, metas))}")
        print(f"Probada: {'SÍ' if ok_b else 'NO'}")

        extra = [a for a in nuevos if a not in metas]
        print(f"\nTrabajo extra de adelante (no visitado por atrás): {', '.join(map(str, extra)) or '(ninguno)'}")
        resumen.append((q, ok_f, ok_b))

    print()
    print("Resumen")
    print("=" * 64)
    print(f"{'Consulta':<22}  {'Adelante':>8}  {'Atrás':>6}")
    for q, f, b in resumen:
        print(f"{str(q):<22}  {'SÍ' if f else 'NO':>8}  {'SÍ' if b else 'NO':>6}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kb", type=Path, default=HERE / "biblioteca.yaml")
    p.add_argument("--query", action="append", help="consulta (se puede repetir); por defecto las del YAML")
    p.add_argument("--add-fact", action="append", default=[], help="hecho extra, se añade al final")
    p.add_argument("--out", type=Path, help="guardar también la salida en este archivo")
    args = p.parse_args()

    kb = load_kb(args.kb)
    kb.facts.extend(parse_atom(f) for f in args.add_fact)
    queries = [parse_atom(q) for q in args.query] if args.query else kb.queries

    if args.out:
        buf = io.StringIO()
        real = sys.stdout
        sys.stdout = buf
        try:
            run(kb, queries)
        finally:
            sys.stdout = real
        text = buf.getvalue()
        print(text, end="")
        args.out.write_text(text, encoding="utf-8")
        print(f"\n(salida guardada en {args.out})")
    else:
        run(kb, queries)


if __name__ == "__main__":
    main()
