# Informed Search on the Romania Map

Greedy best-first search and A* on the Romania road map from Russell & Norvig,
AIMA Figures 3.2 and 3.22. Both algorithms use the same graph, problem, and
heuristic `h(n)`.

The default instance is **Arad → Bucharest**. The heuristic is the
**straight-line distance to Bucharest** from the AIMA table (admissible and
consistent). Optimal cost is **418 km**.

## Setup

```bash
cd "Búsqueda informada/project"
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows (PowerShell):

```powershell
cd "Búsqueda informada/project"
python3 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Later sessions: `cd` into this folder and run `source venv/bin/activate`
(or `.\venv\Scripts\Activate.ps1` on Windows). Deactivate with `deactivate`.

## Programs

| File | Role |
|---|---|
| `01_romania_map.py` | Print all cities and roads |
| `02_heuristics.py` | Print `h(n)` for every city toward the goal |
| `03_greedy_best_first_search.py` | Greedy — expand lowest `h(n)` |
| `04_a_star_search.py` | A* — expand lowest `f(n) = g(n) + h(n)` |

```bash
python 01_romania_map.py
python 02_heuristics.py
python 03_greedy_best_first_search.py
python 04_a_star_search.py
```

Change the instance with `--from-city` and `--to`:

```bash
python 04_a_star_search.py --from-city Timisoara --to Bucharest
```

If the goal is not Bucharest, `h(n)` falls back to Euclidean distance on
approximate map coordinates (the AIMA table is only defined for Bucharest).

## What to expect (Arad → Bucharest)

- **Greedy** follows `h(n)` only: `Arad → Sibiu → Fagaras → Bucharest` (**450 km**).
  Sibiu looks good; Fagaras looks even closer (`h = 176`) than Rimnicu Vilcea (`h = 193`), so greedy never takes the cheaper 418 km route.
- **A*** uses `f = g + h` and returns `Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest` (**418 km**).
- Each search printout lists `g`, `h`, and `f` along the path.

Neighbors are expanded in **alphabetical order** so runs are deterministic.
