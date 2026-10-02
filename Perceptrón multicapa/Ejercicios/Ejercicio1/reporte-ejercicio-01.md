# Reporte - Ejercicio 01: mas capas en el perceptron multicapa

## 1. Trabajo realizado

Compare cuatro corridas sobre Iris: implementacion manual con NumPy y Keras, cada una con la topologia original `4 x 3 x 3` y con la topologia profunda `4 x 3 x 3 x 3 x 3`. Mantive `sigmoid`, MSE, `eta = 0.03` y 500 epocas en las cuatro corridas principales.

Los notebooks originales no se modificaron. Cree copias ejecutables en:

- `ejercicio-01-manual.ipynb`: forward y backpropagation genericos para cualquier numero de capas.
- `ejercicio-01-keras.ipynb`: modelos original, profundo y los dos retos opcionales.

Todo el trabajo y las pruebas se realizaron desde VS Code con el entorno `Python (Inteligencia_Artificial)`.

## 2. Resultados obtenidos

| Implementacion | Topologia | Error inicial | Error final | Accuracy | Tiempo aproximado |
|---|---:|---:|---:|---:|---:|
| NumPy manual | 4-3-3 | 0.695555 | 0.059584 | 96.67% | 6.028 s |
| NumPy manual | 4-3-3-3-3 | 0.681967 | 0.670880 | 33.33% | 11.927 s |
| Keras | 4-3-3 | 0.303676 | 0.221660 | 33.33% | 28.388 s |
| Keras | 4-3-3-3-3 | 0.237125 | 0.222132 | 33.33% | 25.357 s |

### Lectura de la tabla

- En la implementacion manual, la topologia original aprendio muy bien y la profunda practicamente no aprendio.
- En Keras, ambas redes sigmoide+MSE quedaron cerca de una clasificacion uniforme en esta corrida. El error bajo, pero el `argmax` de las salidas no produjo una buena clasificacion.
- El tiempo de Keras no debe compararse directamente con el de NumPy: incluye el costo de TensorFlow y diferencias de ejecucion.

## 3. Efecto de agregar capas

No mejoro de forma consistente. En la version manual, agregar dos capas empeoro claramente el resultado: el error final paso de `0.059584` a `0.670880` y la exactitud de `96.67%` a `33.33%`. En Keras, el error final fue casi igual (`0.221660` frente a `0.222132`) y la exactitud permanecio en `33.33%`.

Por lo tanto, mas capas no garantizan una solucion mejor cuando se apilan sigmoides, se usa MSE y solo se entrenan 500 epocas.

## 4. Diferencias entre NumPy y Keras

Las curvas no se comportaron igual en esta ejecucion. La implementacion manual original aprendio mucho mejor que Keras. Esto no significa necesariamente que Keras este mal. Hay diferencias importantes:

1. **Inicializacion:** fijar las semillas no obliga a que ambas implementaciones produzcan los mismos pesos.
2. **Orden de los datos:** Keras mezcla los ejemplos por defecto; la implementacion manual recorre Iris en el orden original.
3. **Actualizacion:** el codigo manual actualiza pesos ejemplo por ejemplo y calcula el error al final de cada epoca.
4. **Escalado:** Iris usa atributos con escalas distintas. La normalizacion podria cambiar la facilidad de optimizacion.
5. **Metrica:** MSE y accuracy miden cosas distintas; una reduccion de MSE no siempre implica una buena clasificacion.

## 5. Por que una red profunda puede aprender peor

Con sigmoides apiladas, la derivada `sigmoid(z)(1-sigmoid(z))` puede ser pequena. Al multiplicar varias derivadas durante backpropagation, el delta que llega a las primeras capas puede hacerse muy pequeno. Esto se conoce como desvanecimiento del gradiente.

En la corrida manual profunda, el error paso de `0.681967` a solo `0.670880` en 500 epocas. La curva se aplano desde el comienzo. Esa evidencia es compatible con un gradiente demasiado pequeno y con una topologia mas dificil de optimizar.

## 6. Reto opcional

En Keras probe una red profunda con ReLU en las capas ocultas, softmax en la salida y `categorical_crossentropy`:

- perdida final durante `fit`: `0.184039`;
- accuracy final durante el entrenamiento: `95.33%`;
- evaluacion posterior: accuracy `90.67%`.

Este resultado fue mucho mejor que las redes profundas todo-sigmoide+MSE de esta corrida. ReLU reduce la saturacion en las capas ocultas y la entropia cruzada es una perdida mas natural para clasificacion multiclase con salida softmax.

Tambien probe la variante `4 x 8 x 8 x 8 x 3` con sigmoide+MSE. Obtuvo perdida `0.222050` y accuracy `33.33%`. Mas neuronas tampoco resolvieron por si mismas el problema de optimizacion.

## 7. Pendientes personales de entrega

El trabajo y las pruebas ya fueron realizados desde VS Code. Para cerrar mi entrega me falta:

- [ ] Revisar las graficas y confirmar que se visualizan correctamente en las notebooks.
- [ ] Agregar las capturas de las cuatro curvas principales.
- [ ] Agregar las capturas de los dos `model.summary()` de Keras.
- [ ] Agregar la captura de la prediccion de ejemplo.
- [ ] Revisar el reporte final y actualizar los numeros si vuelvo a ejecutar las notebooks.
- [ ] Hacer el commit y el push desde VS Code.

## 8. Como reproducir

1. Abrir la carpeta `Inteligencia_Artificial` en VS Code.
2. Seleccionar el kernel `Python (Inteligencia_Artificial)`.
3. Abrir cualquiera de los dos notebooks del ejercicio.
4. Ejecutar **Run All**.
5. Revisar las celdas tituladas `Comparacion` y `Reto opcional`.

La implementacion manual usa `forward`, `mse`, `backward_update` y `train`. La funcion `backward_update` recorre las capas desde la salida hasta la entrada, por lo que la retropropagacion si utiliza las cuatro capas de la red profunda.
