# Uninformed Search on the Romania Map

Route finding on the Romania road map from Russell & Norvig, AIMA Figure 3.2.
Five uninformed-search algorithms share the same graph and `RouteFindingProblem`.

Coordinates are city names. Step costs are road distances in **km**. The default
problem is **Arad → Bucharest** (optimal cost **418 km**).

## Setup

Create a Python 3 virtual environment, activate it, then install dependencies.

```bash
cd "Búsqueda no informada/project"
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows (PowerShell):

```powershell
cd "Búsqueda no informada/project"
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
| `02_breadth_first_search.py` | BFS — fewest *roads*, not fewest km |
| `03_uniform_cost_search.py` | UCS — cheapest path in km |
| `04_depth_first_search.py` | DFS — graph search, not optimal |
| `05_depth_limited_search.py` | DLS — DFS with a depth limit |
| `06_iterative_deepening_search.py` | IDS — DLS with limit = 0, 1, 2, … |

```bash
python 01_romania_map.py
python 01_romania_map.py --from-city Arad
python 02_breadth_first_search.py
python 03_uniform_cost_search.py
python 04_depth_first_search.py
python 05_depth_limited_search.py --limit 2
python 05_depth_limited_search.py --limit 3
python 06_iterative_deepening_search.py
```

Change the instance with `--from-city` and `--to`:

```bash
python 03_uniform_cost_search.py --from-city Timisoara --to Bucharest
```

## What to expect (Arad → Bucharest)

- **BFS** returns `Arad → Sibiu → Fagaras → Bucharest` (3 roads, 450 km) — fewest hops, not cheapest km.
- **UCS** returns `Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest` at **418 km**.
- **DFS** returns some valid path; usually longer.
- **DLS** with `--limit 2` reports `cutoff`. With `--limit 3` it can reach Bucharest via Fagaras.
- **IDS** finds the same hop-optimal path as BFS.

Neighbors are expanded in **alphabetical order** so runs are deterministic.
