# Reporte — Ejercicio 01: Encadenamiento en la biblioteca

## 1. Trabajo realizado

Se implementó inferencia sobre **cláusulas definidas** (Russell y Norvig, *AIMA*, cap. 9) con dos algoritmos: **encadenamiento hacia adelante** (*forward chaining*) y **encadenamiento hacia atrás** (*backward chaining*). Ambos se usaron para decidir quién puede entrar de noche a la biblioteca. Antes de programar se corrió el proyecto de referencia (`project/`: `04_compare.py` sobre `kb/cats.yaml`) para revisar el formato de las trazas.

La solución está en:

- `solucion-01/biblioteca.yaml`: base de conocimiento (hechos, reglas en el orden de la tabla y las tres consultas).
- `solucion-01/encadenamiento.py`: lector de átomos, unificación, renombrado de variables, encadenamiento hacia adelante y hacia atrás.
- `solucion-01/trazas.txt`: salida completa de las tres consultas con ambos algoritmos.
- `solucion-01/trazas_credencial_luis.txt`: salida de la pregunta 3 (con `TieneCredencial(Luis)` añadido).

```bash
cd "Razonamiento Logico/Ejercicio 1/solucion-01"
python encadenamiento.py                       # las tres consultas
python encadenamiento.py --query "AccesoNoche(Luis)" --add-fact "TieneCredencial(Luis)"
```

---

## 2. Base de conocimiento

### A. Hechos

```text
Estudiante(Ana)        Estudiante(Luis)        Profesor(Marta)
TieneCredencial(Ana)   TieneCredencial(Marta)  HorarioNocturno(Hoy)
```

### B. Reglas (en este orden)

| Id | Si | Entonces |
|---|---|---|
| `R_miembro_est` | `Estudiante(x)` ∧ `TieneCredencial(x)` | `Miembro(x)` |
| `R_miembro_prof` | `Profesor(x)` | `Miembro(x)` |
| `R_acceso` | `Miembro(x)` ∧ `HorarioNocturno(Hoy)` | `AccesoNoche(x)` |
| `R_beca` | `Estudiante(x)` ∧ `TieneCredencial(x)` | `Becario(x)` |

Variables en minúscula (`x`) y constantes con mayúscula inicial (`Ana`, `Hoy`). Cada uso de una regla renombra sus variables (`x` → `x_1`, `x_2`, …); en las trazas se muestra la sustitución sobre la variable original (`{x/Ana}`).

### C. Cómo funciona cada algoritmo

| | Hacia adelante | Hacia atrás |
|---|---|---|
| Dirigido por | Los **datos** | La **meta** |
| Parte de | Los hechos | La consulta |
| Qué hace | Dispara toda regla cuyas premisas ya son hechos, por rondas, hasta que una ronda no produce nada nuevo | Busca la meta en los hechos; si no está, abre las reglas cuya cabeza unifica con ella y prueba sus premisas |
| Orden | Reglas en orden de la tabla, contra los hechos **al empezar la ronda** | Hechos primero, luego reglas en orden; la primera prueba exitosa gana |
| Añade hechos | Sí, **todas** las consecuencias | No |

---

## 3. Resultados Obtenidos

### A. Resumen

| Consulta | Hacia adelante | Hacia atrás |
|---|:---:|:---:|
| `AccesoNoche(Ana)` | **SÍ** | **SÍ** |
| `AccesoNoche(Luis)` | **NO** | **NO** |
| `AccesoNoche(Marta)` | **SÍ** | **SÍ** |

### B. Encadenamiento hacia adelante

La traza es la misma en las tres consultas, porque el algoritmo deriva todo sin importar qué se pregunta; solo cambia la comprobación final.

```text
--- ronda 1 ---
  dispara R_miembro_est   {x/Ana}    ⇒  Miembro(Ana)
  dispara R_miembro_prof  {x/Marta}  ⇒  Miembro(Marta)
  dispara R_beca          {x/Ana}    ⇒  Becario(Ana)
--- ronda 2 ---
  dispara R_acceso        {x/Ana}    ⇒  AccesoNoche(Ana)
  dispara R_acceso        {x/Marta}  ⇒  AccesoNoche(Marta)
--- ronda 3 ---
  sin átomos nuevos → punto fijo
```

Átomos nuevos, en orden: `Miembro(Ana)`, `Miembro(Marta)`, `Becario(Ana)`, `AccesoNoche(Ana)`, `AccesoNoche(Marta)`.

- `R_acceso` no dispara en la ronda 1: `Miembro(Ana)` y `Miembro(Marta)` se derivan en esa ronda y solo se usan como premisas en la siguiente.
- Luis sigue siendo solo `Estudiante(Luis)`: no aparece `Miembro(Luis)`, `Becario(Luis)` ni `AccesoNoche(Luis)`, porque no existe `TieneCredencial(Luis)`.

### C. Encadenamiento hacia atrás

**`AccesoNoche(Ana)` — probada**

```text
meta   AccesoNoche(Ana)
  regla R_acceso  {x/Ana}
    meta   Miembro(Ana)
      regla R_miembro_est  {x/Ana}
        meta   Estudiante(Ana)
          ✓ hecho Estudiante(Ana)
        meta   TieneCredencial(Ana)
          ✓ hecho TieneCredencial(Ana)
    meta   HorarioNocturno(Hoy)
      ✓ hecho HorarioNocturno(Hoy)
```

La traza solo usa `R_acceso` y `R_miembro_est`. No aparecen Luis, Marta, `R_beca` ni `Becario`.

**`AccesoNoche(Luis)` — no probada**

```text
meta   AccesoNoche(Luis)
  regla R_acceso  {x/Luis}
    meta   Miembro(Luis)
      regla R_miembro_est  {x/Luis}
        meta   Estudiante(Luis)
          ✓ hecho Estudiante(Luis)
        meta   TieneCredencial(Luis)
          ✗ falla TieneCredencial(Luis)
      ✗ R_miembro_est falla para Miembro(Luis)
      regla R_miembro_prof  {x/Luis}
        meta   Profesor(Luis)
          ✗ falla Profesor(Luis)
      ✗ R_miembro_prof falla para Miembro(Luis)
      ✗ falla Miembro(Luis)
  ✗ R_acceso falla para AccesoNoche(Luis)
  ✗ falla AccesoNoche(Luis)
```

**`AccesoNoche(Marta)` — probada**

```text
meta   AccesoNoche(Marta)
  regla R_acceso  {x/Marta}
    meta   Miembro(Marta)
      regla R_miembro_est  {x/Marta}
        meta   Estudiante(Marta)
          ✗ falla Estudiante(Marta)
      ✗ R_miembro_est falla para Miembro(Marta)
      regla R_miembro_prof  {x/Marta}
        meta   Profesor(Marta)
          ✓ hecho Profesor(Marta)
    meta   HorarioNocturno(Hoy)
      ✓ hecho HorarioNocturno(Hoy)
```

### D. Comparación del trabajo realizado

| Consulta | Átomos derivados hacia adelante | Metas visitadas hacia atrás | Trabajo extra de adelante |
|---|:---:|:---:|---|
| `AccesoNoche(Ana)` | 5 | 5 | `Miembro(Marta)`, `Becario(Ana)`, `AccesoNoche(Marta)` |
| `AccesoNoche(Luis)` | 5 | 5 | Los 5 átomos (ninguno es sobre Luis) |
| `AccesoNoche(Marta)` | 5 | 5 | `Miembro(Ana)`, `Becario(Ana)`, `AccesoNoche(Ana)` |

---

## 4. Respuestas a las Preguntas

### Pregunta 1: ¿Por qué `Becario(Ana)` sale en el encadenamiento hacia adelante de `AccesoNoche(Ana)` y no en el de hacia atrás?

**Respuesta:**
Porque el encadenamiento hacia adelante está **dirigido por los datos**: en cada ronda dispara **toda** regla cuyas premisas ya son hechos, sin mirar la consulta. En la ronda 1, `Estudiante(Ana)` y `TieneCredencial(Ana)` son hechos, así que `R_beca` se cumple y produce `Becario(Ana)`, aunque ese átomo no sirva para decidir el acceso. Además, el algoritmo no se detiene al probar la consulta: sigue hasta el punto fijo.

El encadenamiento hacia atrás está **dirigido por la meta**: solo abre reglas cuya **cabeza** unifica con la meta actual. Las metas que aparecen al probar `AccesoNoche(Ana)` son `AccesoNoche`, `Miembro`, `Estudiante`, `TieneCredencial` y `HorarioNocturno`. Ninguna es `Becario(…)`, así que la cabeza de `R_beca` nunca unifica y la regla nunca se abre.

---

### Pregunta 2: ¿Por qué hacia atrás prueba `R_miembro_est` al buscar `Miembro(Marta)`, si Marta es profesora?

**Respuesta:**
Porque el algoritmo **no sabe de antemano** cuál regla va a funcionar. Para la meta `Miembro(Marta)`:

1. Busca primero en los hechos: no existe `Miembro(Marta)`.
2. Recorre las reglas **en el orden de la tabla** y abre la primera cuya cabeza unifica con la meta. Tanto `R_miembro_est` como `R_miembro_prof` tienen cabeza `Miembro(x)`, y `R_miembro_est` va primero.
3. Con $\{x/\text{Marta}\}$ intenta la primera premisa, `Estudiante(Marta)`. No es un hecho y ninguna regla la concluye, así que falla y la regla entera se abandona (no hace falta probar `TieneCredencial(Marta)`).
4. Pasa a la siguiente regla, `R_miembro_prof`, cuya premisa `Profesor(Marta)` sí es un hecho.

Que Marta sea profesora no es algo que el algoritmo "vea" antes de intentarlo. Lo descubre al probar las reglas en orden. Si `R_miembro_prof` estuviera antes en la tabla, la traza de Marta no pasaría por la regla de estudiante.

---

### Pregunta 3: Si se añade el hecho `TieneCredencial(Luis)` y se vuelve a preguntar `AccesoNoche(Luis)`, ¿qué átomos nuevos aparecen y la consulta queda probada?

**Respuesta:**
Se comprobó con `python encadenamiento.py --query "AccesoNoche(Luis)" --add-fact "TieneCredencial(Luis)"`, que añade el hecho al final de la lista. **La consulta queda probada con ambos algoritmos.**

**Hacia adelante**, los átomos nuevos pasan de 5 a 8:

```text
--- ronda 1 ---
  dispara R_miembro_est   {x/Ana}    ⇒  Miembro(Ana)
  dispara R_miembro_est   {x/Luis}   ⇒  Miembro(Luis)        ← nuevo
  dispara R_miembro_prof  {x/Marta}  ⇒  Miembro(Marta)
  dispara R_beca          {x/Ana}    ⇒  Becario(Ana)
  dispara R_beca          {x/Luis}   ⇒  Becario(Luis)        ← nuevo
--- ronda 2 ---
  dispara R_acceso        {x/Ana}    ⇒  AccesoNoche(Ana)
  dispara R_acceso        {x/Luis}   ⇒  AccesoNoche(Luis)    ← nuevo
  dispara R_acceso        {x/Marta}  ⇒  AccesoNoche(Marta)
```

Aparecen tres átomos sobre Luis: **`Miembro(Luis)`**, **`Becario(Luis)`** y **`AccesoNoche(Luis)`**. `Miembro(Luis)` queda antes que `Miembro(Marta)` porque `R_miembro_est` recorre los hechos `Estudiante(…)` en orden (Ana, luego Luis) y se dispara antes que `R_miembro_prof`.

**Hacia atrás**, la traza es igual a la de Ana: `R_acceso` → `R_miembro_est` → `Estudiante(Luis)` ✓, `TieneCredencial(Luis)` ✓ → `HorarioNocturno(Hoy)` ✓. No se intenta `R_miembro_prof` y no se deriva `Becario(Luis)`, porque la primera prueba exitosa se acepta.
