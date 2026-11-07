# Ejercicio 1 — Q-learning en Cliff Walking

## Contexto

Cliff Walking es el ejemplo de control con diferencias temporales de Sutton y
Barto (*Reinforcement Learning: An Introduction*, ejemplo de *cliff walking*:
la cuadrícula con S, “The Cliff” y G, y la curva de recompensa por episodio).

El agente camina por una cuadrícula. Cada paso cuesta −1. La fila inferior,
entre la salida y la meta, es un acantilado: pisarlo cuesta −100. Con
**ε-greedy** (ε = 0.1), Q-learning aprende la política que va **junto al
borde** del acantilado: es la más corta y, por tanto, la de mayor retorno.

La figura del libro también dibuja la curva de Sarsa. **Este ejercicio pide
únicamente Q-learning.**

Antes de programar, recorre el proyecto de referencia. Ahí el algoritmo está
escrito para leerse línea por línea (sin NumPy y sin Gym), sobre un pasillo
de tres casillas y una cuadrícula pequeña:

`/Users/victoruccetina/Documents/code/inteligencia-artificial/Q-learning/project`

Ese proyecto **ilustra el algoritmo**. El mundo que vas a resolver es el del
libro, descrito abajo. En particular, `envs/cliff.yaml` es una cuadrícula
**3×5** en la que caer al acantilado **termina** el episodio. En el libro la
cuadrícula es **4×12** y caer **devuelve al agente a S** sin terminar el
episodio.

## Objetivo

Implementar Q-learning tabular con comportamiento ε-greedy y usarlo para
aprender una política en Cliff Walking. La política greedy (ε = 0) debe
seguir el camino óptimo, pegado al acantilado, con retorno **−13**.

## Archivos a crear / modificar

Crea tu propio programa (por ejemplo `Q-learning/ejercicios/solucion-01/`).
Puedes organizar el código como quieras.

Deja intacto `Q-learning/project`: consúltalo, no lo entregues como solución
ni cambies sus módulos para “hacer pasar” este ejercicio.

## El entorno (libro)

Cuadrícula de **4 filas × 12 columnas**. La fila 0 es la de arriba. Las
acciones son `N`, `E`, `S`, `W` (norte resta 1 a la fila, este suma 1 a la
columna).

```
fila\col   0  1  2  3  4  5  6  7  8  9  10 11
0          .  .  .  .  .  .  .  .  .  .  .  .
1          .  .  .  .  .  .  .  .  .  .  .  .
2          .  .  .  .  .  .  .  .  .  .  .  .
3          S  C  C  C  C  C  C  C  C  C  C  G
```

- **S** = inicio `(3, 0)`.
- **G** = meta `(3, 11)`. Entrar a G termina el episodio.
- **C** = The Cliff: `(3, 1)` … `(3, 10)`.
- Si la acción sacaría al agente del mapa, se queda en la misma casilla.
- Transición ordinaria (incluye entrar a G y chocar con el borde): **r = −1**.
- Transición al acantilado: **r = −100** y el siguiente estado es **S**. El
  episodio **continúa**.
- El episodio termina solo al entrar a G (o al alcanzar el tope de pasos).
- Descuento **γ = 1** (episodio sin descuento, como en el libro).

El camino óptimo es único en casillas: desde S, un paso al norte, once al
este por la fila 2 y un paso al sur hasta G. Son **13** pasos, todos con
recompensa −1, así que el retorno greedy óptimo es **−13**.

## Qué debe hacer tu programa

1. **Tabla Q.** Un valor `Q(s, a)` por cada estado no terminal y cada acción.
   Inicialízala en **0**.
2. **Conducta ε-greedy.** Con probabilidad ε elige una acción al azar; si no,
   elige una acción que maximice `Q(s, ·)`. En empates, usa un orden fijo
   (por ejemplo `N`, `E`, `S`, `W`, la primera de la lista).
3. **Actualización de Q-learning** en cada paso, con la acción que de verdad
   se ejecutó y el máximo del estado siguiente:

```
Q(s, a) ← Q(s, a) + α [ r + γ max_a' Q(s', a') − Q(s, a) ]
```

   Si `s'` es terminal (la meta), el máximo futuro es **0**. Si `s'` es S
   después de caer, S sigue siendo un estado normal: el máximo futuro es
   `max_a' Q(S, a')`.
4. **Entrenamiento** de varios episodios. En cada uno, parte de S, elige y
   actualiza hasta llegar a G o agotar un tope de pasos (un tope de unos
   **200** pasos evita un ciclo infinito si la política aún no llega a G).
5. **Evaluación greedy.** Con la Q ya entrenada, recorre desde S **sin**
   exploración (ε = 0) y registra el camino, el número de pasos y el retorno.

Parámetros de la corrida que vas a reportar (los de la figura: ε = 0.1 y
500 episodios en el eje horizontal):

| Parámetro | Valor |
|---|---|
| α | 0.5 |
| γ | 1 |
| ε | 0.1 |
| episodios | 500 |
| Q inicial | 0 |
| semilla | fija (la que tú elijas; repórtala) |

## Pasos sugeridos

1. Lee el README del proyecto y corre el pasillo de la clase, para ver un
   solo backup de Q-learning antes de escribir el tuyo:

```bash
cd "Q-learning/project"
python3 -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

python 01_show_env.py
python 02_one_update.py
python 03_train.py
```

2. En `qlearn/agent.py` sigue estas piezas, en este orden: `empty_q`,
   `argmax_action`, `epsilon_greedy`, `td_target_q`, `apply_update` y el
   ramal `method == "q-learning"` de `train`. Ahí está la misma regla de
   actualización que vas a programar.
3. Implementa el entorno 4×12 con las transiciones de la sección anterior.
   Comprueba a mano tres casos: un paso norte desde S (cae en `(2, 0)`,
   r = −1); un paso este desde S (cae en S, r = −100, el episodio sigue);
   el paso sur desde `(2, 11)` (entra a G, r = −1, el episodio termina).
4. Entrena con la tabla de parámetros y fija la semilla.
5. Imprime la política greedy (flechas sobre la cuadrícula, o la lista de
   acciones desde S) y el retorno de esa política.
6. Guarda la recompensa **acumulada de cada episodio de entrenamiento**
   (con la ε-greedy encendida). Una media móvil de unos 10 episodios basta
   para comparar la forma de tu curva con la de Q-learning en la figura.

## Criterios de aceptación

- El programa implementa Q-learning (el blanco del update es
  `r + γ max_a' Q(s', a')`) con conducta ε-greedy.
- El entorno es el 4×12 del libro: caer devuelve a S con −100 y el episodio
  sigue; entrar a G termina el episodio con −1.
- Con α = 0.5, γ = 1, ε = 0.1 y 500 episodios, la política greedy desde S
  llega a G en **13** pasos, por la fila inmediata al acantilado, y el
  retorno greedy es **−13**.
- Reportas la semilla y la serie (o la gráfica) de recompensa por episodio
  durante el entrenamiento.
- La solución es código tuyo. `Q-learning/project` queda como referencia.

Durante el entrenamiento la recompensa por episodio **no** tiene por qué
acercarse a −13. Con ε = 0.1 el agente a veces da un paso al sur, cae y
suma −100. La curva de Q-learning en la figura se queda por debajo de la
política greedy precisamente por eso. El −13 se mide en la evaluación con
ε = 0.

## Entrega

1. El código que implementa el entorno y Q-learning, con la semilla usada.
2. La política greedy (cuadrícula con flechas o camino S → G) y el retorno
   greedy.
3. La recompensa por episodio de las 500 episodios (tabla o gráfica, con
   media móvil si la curva cruda es difícil de leer).
4. Un reporte breve (media página) que responda:
   - ¿Por qué el camino de 13 pasos, pegado al acantilado, es óptimo?
   - ¿Por qué la curva de entrenamiento queda por debajo de −13 aunque la
     política greedy ya sea óptima?
   - En el paso que cae al acantilado, ¿cuál es `s'` en el backup de
     Q-learning, y por qué ese backup no trata el acantilado como estado
     terminal?

## Pistas

- Q-learning es **off-policy**: la acción que se ejecuta sale de ε-greedy;
  el blanco usa el **máximo** de `Q(s', ·)`, aunque esa acción greedy no
  sea la que el agente vaya a tomar después.
- Con todas las recompensas ≤ 0 y Q inicial en 0, al principio todas las
  acciones empatan. El desempate fijo decide qué acción se prueba primero;
  documenta el orden que usaste.
- Si muchos episodios se cortan por el tope de pasos, la política todavía
  no está llegando a G: revisa que caer reinicie en S **sin** marcar el
  episodio como terminado, y que entrar a G **sí** lo termine.
- El pasillo del proyecto (`02_one_update.py`) muestra la aritmética de un
  backup con α = 0.5. El de Cliff Walking es la misma fórmula; cambian el
  estado, la recompensa y si `s'` es terminal.
