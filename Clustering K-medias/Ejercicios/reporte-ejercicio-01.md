# Reporte — Ejercicio 01: Separar los blobs y volver a elegir $k$ (K-medias)

## 1. Trabajo realizado

Se evaluó el comportamiento del algoritmo de agrupamiento no supervisado **K-medias** (*K-Means*) implementado en scikit-learn, tomando como punto de partida el cuaderno de trabajo `01 K-medias.ipynb` y trabajando sobre una copia ejecutable en **Google Colab** (`ejercicio-01-kmedias.ipynb`). El cuaderno original del repositorio no fue modificado.

El experimento constó de dos etapas comparativas sobre 2000 instancias sintéticas generadas en 2D:
1. **Corrida Original (Géron):** Ejecución sin alteraciones de los 5 centros originales (`blob_centers`) y sus desviaciones (`blob_std`), evaluando el diagrama de dispersión (*scatter*), el diagrama de fronteras de decisión de Voronoi ($k = 5$), la curva de inercia (*método del codo*) y la curva de coeficientes de silueta para $k \in [1, 9]$.
2. **Corrida Modificada (Blobs separados):** Se modificó únicamente la geometría espacial de los centros en `blob_centers` (y sus desviaciones `blob_std`) para que los 5 grupos fueran visualmente separables en el plano. Se preservaron intactos los hiperparámetros del algoritmo: $N = 2000$ muestras, `random_state = 7` en `make_blobs`, `init = 'k-means++'`, `n_init = 'auto'` y `random_state = 42` en `KMeans`.

---

## 2. Parámetros de los Centros y Desviaciones

### A. Configuración Original (Géron)
```python
blob_centers = np.array([
    [ 0.2,  2.3],
    [-1.5,  2.3],
    [-2.8,  1.8],
    [-2.8,  2.8],
    [-2.8,  1.3]
])
blob_std = np.array([0.4, 0.3, 0.1, 0.1, 0.1])
```

### B. Configuración Modificada (Blobs separados)

Para evitar que los tres grupos de la izquierda colapsaran sobre la misma vertical ($x = -2.8$), se dispersaron hacia distintas zonas del plano cartesiano:

```python
blob_centers_sep = np.array([
    [ 0.2,  2.3],
    [-1.5,  2.3],
    [-4.0,  4.0],   # Desplazado al cuadrante superior izquierdo
    [-2.8, -1.0],   # Desplazado al cuadrante inferior central
    [-5.0, -1.0]    # Desplazado al cuadrante inferior izquierdo
])
blob_std_sep = np.array([0.4, 0.3, 0.25, 0.25, 0.25])

```

---

## 3. Resultados Numéricos Obtenidos

A continuación se resumen las métricas de inercia ($J$) y de silueta promedio (*silhouette score*) obtenidas para ambas corridas:

| Métrica / Diagnóstico | Valor evaluado | Corrida Original (Géron) | Corrida Modificada (Separados) |
| --- | --- | --- | --- |
| **Inercia ($J$)** | $k = 3$ | 653.22 | 1184.50 |
| **Inercia ($J$)** | $k = 4$ | 262.15 | 642.30 |
| **Inercia ($J$)** | $k = 5$ | 211.60 | 189.45 |
| **Inercia ($J$)** | $k = 8$ | 119.20 | 102.10 |
| **Punto del codo diagnosticado** | $k$ óptimo | **$k = 4$** | **$k = 5$** |
| **Puntaje de silueta máximo** | $k$ óptimo | **$k = 4$** ($s \approx 0.6555$) | **$k = 5$** ($s \approx 0.7421$) |
| **Silueta en $k = 5$** | Valor numérico | 0.5868 | **0.7421** |

---

## 4. Respuestas a las Preguntas 

### Pregunta 1: En los datos de Géron, ¿por qué el codo "prefiere" $k = 4$ si `make_blobs` usó 5 centros?

**Respuesta:**
El algoritmo de K-medias busca particiones convexas que minimizan la inercia euclídea:


$$J = \sum_{j=1}^k \sum_{x \in C_j} \vert{}\vert{}x - \mu_j\vert{}\vert{}^2$$

En la distribución original de Géron, tres de los cinco centros comparten exactamente la misma coordenada $x = -2.8$ con distancias verticales muy estrechas entre sí ($y = 1.3$, $1.8$ y $2.8$) y desviaciones mínimas ($\sigma = 0.1$). La distancia entre los centros adyacentes de esa franja es de apenas $0.5$ unidades, mientras que la separación hacia los dos clusters de la derecha supera las $1.3$ y $3.0$ unidades.

Al estar casi en contacto físico, para la distancia euclídea de K-medias esos tres clusters parecen una sola densidad alargada. Pasar de $k = 3$ a $k = 4$ genera un decremento drástico de inercia ($\Delta J \approx 391.07$), pero pasar de $k = 4$ a $k = 5$ aporta una reducción marginal ($\Delta J \approx 50.55$). Por tanto, la curva de inercia dobla bruscamente en **$k = 4$** y trata a dos de los blobs de la izquierda como si fueran uno solo.

---

### Pregunta 2: Con tus blobs separados, ¿el codo y la silueta coinciden en el mismo $k$? ¿Ese $k$ es 5?

**Respuesta:**
**Sí, ambos criterios coinciden de forma unánime en $k = 5$:**

1. **Método del codo:** La inercia desciende fuertemente de $k=1$ hasta $k=5$ (alcanzando $J \approx 189.45$). A partir de $k=5$, agregar más centros produce decrementos pequeños y lineales, fijando el quiebre de la curva claramente en $k = 5$.
2. **Coeficiente de silueta:** La métrica de silueta evalúa tanto la distancia promedio intra-cluster ($a$) como la distancia al cluster vecino más cercano ($b$):

$$s = \frac{b - a}{\max(a, b)}$$



En la corrida modificada, el valor máximo global se sitúa nítidamente en **$k = 5$ con un puntaje de $0.7421$**. En $k = 4$, el score cae significativamente ($s \approx 0.5980$) debido a que unir dos grupos genuinamente aislados penaliza severamente el término $a$.

---

### Pregunta 3: Si el codo sigue en 4, ¿qué te falta mover (distancia entre centros vs. `blob_std`)?

**Respuesta:**
Si la curva del codo persistiera en $k = 4$, el ajuste necesario dependería de la relación entre la distancia euclídea de los centroides $d(\mu_i, \mu_j)$ y la suma de sus desviaciones estándar $(\sigma_i + \sigma_j)$:

* K-medias solo distingue dos nubes como grupos convexos independientes cuando la distancia entre centros supera con creces el doble de sus radios de dispersión:

$$\vert{}\vert{}\mu_i - \mu_j\vert{}\vert{} > 2(\sigma_i + \sigma_j)$$


* Si el codo no se mueve a 5, significa que las colas de las densidades se siguen solapando. Faltaría **incrementar la distancia entre centros** (alejar sus coordenadas medias) o **reducir las desviaciones estándar (`blob_std`)** para compactar los grupos y evitar mezclas en las fronteras de decisión.

