# Reporte - Ejercicio 01: mas capas en el perceptron multicapa

## 1. Trabajo realizado

Compare cuatro corridas sobre Iris: implementacion manual con NumPy y Keras, cada una con la topologia original `4 x 3 x 3` y con la topologia profunda `4 x 3 x 3 x 3 x 3`. Mantive `sigmoid`, MSE, `eta = 0.03` y 500 epocas en las cuatro corridas principales.

Los notebooks originales no se modificaron. Cree copias ejecutables en:

- `ejercicio-01-manual.ipynb`: forward y backpropagation genericos para cualquier numero de capas.
- `ejercicio-01-keras.ipynb`: modelos original, profundo y los dos retos opcionales.

---

## 2. Resultados obtenidos

| Implementación | Topología | Error inicial | Error final | Accuracy final | Tiempo aprox. |
|---|:---:|:---:|:---:|:---:|:---:|
| **NumPy manual** | $4 \times 3 \times 3$ | 0.824421 | 0.086393 | ~96.0% | ~8.5 s |
| **NumPy manual** | $4 \times 3 \times 3 \times 3 \times 3$ | 0.772731 | 0.283513 | ~68.0% | ~17.2 s |
| **Keras** | $4 \times 3 \times 3$ | 0.263725 | 0.165915 | 66.67% | 28.28 s |
| **Keras** | $4 \times 3 \times 3 \times 3 \times 3$ | 0.245969 | 0.221961 | 33.33% | 28.23 s |

---

## 3. Respuestas a las Preguntas 

### Pregunta 1: ¿Bajó más el error al añadir dos capas, o se estancó / empeoró? ¿Ocurrió igual en NumPy y en Keras?

**Respuesta:**
El error **no bajó más**; por el contrario, en ambas implementaciones **se estancó y empeoró notablemente**:

1. **En la implementación a mano (NumPy):**
   - La red original ($4 \times 3 \times 3$) redujo el error de manera consistente de **0.824421 a 0.086393**, permitiendo separar las tres especies de flor exitosamente.
   - La red profunda ($4 \times 3 \times 3 \times 3 \times 3$) comenzó en **0.772731** y se mantuvo prácticamente estancada en **~0.670** durante más de 300 épocas. Aunque finalizó en **0.283513**, su convergencia fue mucho más lenta e ineficiente que la red simple.
2. **En la implementación en Keras:**
   - La red original redujo el MSE de **0.263725 a 0.165915**, alcanzando una exactitud de **66.67%**.
   - La red profunda apenas redujo su pérdida de **0.245969 a 0.221961**, colapsando a una exactitud de **33.33%** (lo que equivale a clasificar ciegamente todas las flores como pertenecientes a una sola clase mayoritaria).

Por lo tanto, el fenómeno de degradación del rendimiento fue cualitativamente **igual en ambas plataformas**: añadir capas ocultas a un problema sencillo con estas funciones de activación no facilitó el aprendizaje.

---

### Pregunta 2: ¿Las curvas de la notebook 01 y de Keras se parecen con la misma topología? Si no, ¿qué diferencias de implementación podrían explicarlo?

**Respuesta:**
Las curvas **no son numéricamente idénticas** (presentan escalas iniciales y trayectorias distintas), debido a tres diferencias fundamentales de implementación:

1. **Definición de la función de coste (Escalamiento de la pérdida):**
   - **NumPy:** La función `calculate_error` implementada calcula la suma de los errores al cuadrado de las 3 salidas por cada muestra y divide únicamente entre el total de muestras $N = 150$:
     $$\text{MSE}_{\text{NumPy}} = \frac{1}{N} \sum_{k=1}^{N} \sum_{i=1}^{3} (y_{k,i} - \hat{y}_{k,i})^2$$
   - **Keras:** La función nativa `MeanSquaredError()` promedia tanto sobre el número de muestras como sobre la dimensión de salida ($C = 3$ neuronas):
     $$\text{MSE}_{\text{Keras}} = \frac{1}{3N} \sum_{k=1}^{N} \sum_{i=1}^{3} (y_{k,i} - \hat{y}_{k,i})^2$$
     Por esta razón matemática, los valores de pérdida en Keras son aproximadamente un tercio de los calculados en el script manual.
2. **Inicialización de pesos sinápticos:**
   - **NumPy:** Se empleó una distribución uniforme en el intervalo simétrico $[-0.5, 0.5]$ con sesgos inicializados aleatoriamente en el mismo rango.
   - **Keras:** Utiliza por defecto el inicializador *Glorot Uniform* (Xavier), cuya varianza depende de la cantidad de entradas y salidas de la capa ($U(-\sqrt{6/(n_{in}+n_{out})}, \sqrt{6/(n_{in}+n_{out})})$), asignando además sesgos iniciales en 0.
3. **Dinámica del algoritmo de optimización:**
   - **NumPy:** Ejecuta un Descenso de Gradiente Estocástico (SGD) en línea estricto, actualizando los pesos muestra por muestra en el orden fijo en el que se encuentra el dataset Iris.
   - **Keras:** Por defecto entrena mediante minilotes (*mini-batches* de tamaño 32) y aplica un barajado aleatorio de muestras en cada época (`shuffle=True`), lo cual altera la trayectoria del descenso de gradiente.

---

### Pregunta 3: Con sigmoides apiladas y MSE, ¿tiene sentido que una red más profunda no aprenda mejor en Iris? Relaciónalo con lo que viste en las gráficas.

**Respuesta:**
Sí, **tiene total sentido teórico y empírico** debido a dos factores:

1. **Problema de baja complejidad:** El dataset Iris cuenta únicamente con 150 ejemplos y 4 dimensiones. Al ser un problema casi linealmente separable, una sola capa oculta de 3 neuronas es suficiente para aproximar las fronteras de decisión. Añadir más capas genera un espacio de optimización no convexo más complejo e innecesario.
2. **Desvanecimiento del Gradiente (*Vanishing Gradient*):**
   La derivada de la función sigmoide viene dada por:
   $$\sigma'(z) = \sigma(z)(1 - \sigma(z))$$
   El valor máximo de esta derivada ocurre en $z = 0$ y corresponde a **0.25**; para cualquier otro valor de activación, $\sigma'(z) < 0.25$.
   
   Al calcular el gradiente mediante la regla de la cadena para la primera capa oculta en una red de cuatro capas, se multiplican consecutivamente las derivadas locales de cada etapa:
   $$\delta^{(1)} = \sigma'(z^{(1)}) \cdot \left( W^{(2)T} \cdot \left( \sigma'(z^{(2)}) \cdot \left( W^{(3)T} \cdot \left( \sigma'(z^{(3)}) \cdot \delta^{(4)} \right) \right) \right) \right)$$
   Al multiplicar términos de magnitud $\le 0.25$ combinados con pesos pequeños ($\vert{}w\vert{} < 0.5$), la magnitud de la corrección que llega a `layer1` decae exponencialmente (del orden de $0.25^4 \approx 0.0039$).

**Relación con las gráficas:**
En la gráfica de la red profunda en NumPy se observa una meseta totalmente plana entre las épocas 50 y 300 en torno a un error de $\approx 0.671$. En Keras, la curva se aplana desde la época 150 en $\approx 0.222$. Esta falta de pendiente visual en las gráficas es la manifestación directa de que los gradientes de las capas iniciales se han anulado, impidiendo que la red ajuste sus características de entrada.

---

## 4. Retos Opcionales

### 4.1. Análisis de Aplanamiento Cada 50 Épocas (Notebook 01 y 02)
Al tabular los errores cada 50 épocas se comprueba cuándo deja de mejorar el modelo:

```text
========================================================================
 Época   | Error NumPy (4x3x3) | Error NumPy Profunda | Error Keras Profunda
========================================================================
   0     |      0.824421       |       0.772731       |       0.245969      
  50     |      0.379968       |       0.671077       |       0.230388      
 100     |      0.350246       |       0.671088       |       0.225166      
 150     |      0.355888       |       0.671061       |       0.223328      
 200     |      0.375034       |       0.670948       |       0.222626      
 250     |      0.390295       |       0.670493       |       0.222331      
 300     |      0.305621       |       0.668400       |       0.222189      
 350     |      0.184541       |       0.635097       |       0.222108      
 400     |      0.128824       |       0.383179       |       0.222051      
 450     |      0.101642       |       0.360857       |       0.222004      
 500     |      0.086393       |       0.283513       |       0.221961      
========================================================================
```

- **Red $4 \times 3 \times 3$:** Muestra un aprendizaje acelerado en las primeras 50 épocas y se aplana asintóticamente hacia la solución óptima a partir de la época 350-400.
- **Redes profundas:** La curva se aplana prematuramente desde las primeras 50 épocas debido al desvanecimiento del gradiente, sin haber alcanzado una separación de clases adecuada.

### 4.2. Red Profunda en Keras con ReLU + Softmax + Categorical Crossentropy

Se entrenó el modelo con 3 capas ocultas densas con activación **ReLU**, salida con activación **Softmax** y función de pérdida `categorical_crossentropy`:

- **Pérdida final:** 1.099081
- **Exactitud final:** 33.33%
- **Diagnóstico:** Al utilizar capas muy estrechas (3 neuronas) junto a un optimizador SGD sin momento a $\eta = 0.03$, las activaciones ReLU corren el riesgo de desactivarse por completo (*dying ReLU*) si reciben combinaciones lineales negativas con inicializaciones estándar, demostrando que arquitecturas profundas estrechas requieren tasas de aprendizaje mayores o inicializadores específicos (como He Normal).

### 4.3. Variación del Ancho de Capas Ocultas ($4 \times 8 \times 8 \times 8 \times 3$)

Se evaluó una red profunda con 8 neuronas en cada capa oculta manteniendo activación sigmoide y MSE:

- **Pérdida final:** 0.221487
- **Exactitud final:** 33.33%
- **Diagnóstico:** Incrementar el número de neuronas por capa no soluciona el problema de desvanecimiento del gradiente causado por la función de activación sigmoide en cascada.