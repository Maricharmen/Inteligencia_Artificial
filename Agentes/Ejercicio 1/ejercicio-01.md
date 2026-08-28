# Ejercicio 1 — Cambiar la ubicación del Wumpus y los pits

## Contexto

En el proyecto `Agentes/project` (Mundo de Wumpus, AIMA cap. 2 y 7) el entorno se
describe con archivos YAML en `config/`. El agente y el simulador leen ese archivo
para armar la cueva: tamaño de la cuadrícula, posición inicial, Wumpus, pits
(pozos), oro y puntajes.

El mapa clásico es `config/classic_4x4.yaml` (AIMA Figura 7.2):

```yaml
grid:
  width: 4
  height: 4

agent:
  start: [1, 1]
  direction: east
  arrows: 1

wumpus: [1, 3]

pits:
  - [3, 1]
  - [3, 3]
  - [4, 4]

gold: [2, 3]
```

Recuerda: las coordenadas son **1-based** y `(1, 1)` es la casilla inferior
izquierda. `(x, y)`: `x` es la columna (izquierda→derecha) y `y` la fila
(abajo→arriba).

En este ejercicio **no vas a programar**: vas a **diseñar tu propia cueva**
moviendo el Wumpus y los pits, y luego observar cómo cambia el comportamiento de
los agentes.

## Objetivo

Crear una nueva configuración modificando la posición del **Wumpus** y de los
**pits**, respetando las reglas del entorno, y analizar el efecto sobre los
distintos agentes.

## Archivos a crear / modificar

- Crea un archivo nuevo: `Agentes/project/config/mi_cueva_4x4.yaml`.
  Puedes partir de una copia de `config/classic_4x4.yaml`.

No modifiques el código de `agents/` ni de `wumpus/`.

## Requisitos del nuevo mapa

1. Mantén la cuadrícula de **4x4** y el agente iniciando en `[1, 1]` mirando al
   este.
2. Cambia la posición del **Wumpus** a una casilla distinta de la del mapa
   clásico.
3. Cambia la posición de **los pits** (al menos **2** pits) a casillas distintas
   de las del mapa clásico.
4. Coloca el **oro** en una casilla alcanzable.
5. El mapa debe ser **válido** según las reglas del entorno (ver más abajo). Si
   rompes una regla, el programa lanzará un error al cargar el YAML.

### Reglas de validez (obligatorias)

- Todas las posiciones deben estar **dentro** de la cuadrícula (`1..4`).
- El agente **no** puede iniciar sobre un pit ni sobre el Wumpus.
- El **oro** no puede estar sobre un pit ni sobre el Wumpus.
- El **Wumpus** no puede estar sobre un pit.
- Además (para que la partida tenga sentido): deja al menos **un camino seguro**
  desde `[1, 1]` hasta el oro y de regreso a `[1, 1]`; no rodees la salida ni el
  oro por completo con pozos.

## Pasos sugeridos

1. Copia `config/classic_4x4.yaml` a `config/mi_cueva_4x4.yaml`.
2. Dibuja en papel la cuadrícula 4x4 y marca dónde pondrás el agente, el Wumpus,
   los pits y el oro.
3. Edita el YAML con tus nuevas coordenadas (campos `wumpus`, `pits`, `gold`).
4. Ejecuta primero el visor del entorno para confirmar que el mapa carga y se ve
   como esperabas:

```bash
cd Agentes/project
python 01_wumpus_world.py --config config/mi_cueva_4x4.yaml
```

5. Prueba los agentes sobre tu mapa y observa las diferencias:

```bash
python 02_simple_reflex_agent.py --config config/mi_cueva_4x4.yaml
python 03_model_based_agent.py  --config config/mi_cueva_4x4.yaml
python 04_goal_based_agent.py   --config config/mi_cueva_4x4.yaml
python 05_utility_based_agent.py --config config/mi_cueva_4x4.yaml
python 06_learning_agent.py --episodes 1500 --config config/mi_cueva_4x4.yaml
```

## Criterios de aceptación

- `config/mi_cueva_4x4.yaml` carga sin errores de validación.
- El Wumpus y los pits están en posiciones **distintas** a las del mapa clásico.
- Existe un camino seguro de ida y vuelta al oro (algún agente lo demuestra
  saliendo con **puntaje positivo**).
- El mapa cumple todas las reglas de validez.

## Entrega

1. El archivo `config/mi_cueva_4x4.yaml`.
2. Un diagrama (dibujo o ASCII) de tu cueva, indicando agente, Wumpus, pits y oro.
3. Un breve reporte (media página) que responda:
   - ¿Qué agentes lograron salir con el oro en tu mapa y cuáles no?
   - ¿Por qué el **agente de reflejo simple** falla (o tiene suerte) en tu diseño?
   - ¿Cómo cambia el resultado del **agente basado en modelo** si acercas o alejas
     un pit de la casilla inicial?
4. Evidencias (captura de pantalla) de haber corrido los 4 agentes con tus nueva configuración del mundo.

## Reto opcional

- Diseña una segunda variante (`config/mi_cueva_dificil_4x4.yaml`) en la que el
  **Wumpus bloquee el único camino seguro** hacia el oro. Observa que el agente
  basado en modelo se queda girando, mientras que el agente basado en metas
  (`04_goal_based_agent.py`) **dispara** para destrabar el paso.

## Pistas

- Un **pit** produce *breeze* (brisa) en sus casillas vecinas (arriba, abajo,
  izquierda, derecha). El **Wumpus** produce *stench* (hedor) en sus vecinas.
  Ubícalos pensando en qué percibirá el agente.
- Si el YAML da error al cargar, lee el mensaje: casi siempre indica exactamente
  qué regla rompiste (posición fuera de rango, solapamiento, etc.).
- Empieza con cambios pequeños (mover un pit una casilla) y ve aumentando la
  dificultad.
