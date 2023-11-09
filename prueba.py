import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
from scipy.stats import expon

# Constante: Bailabilidad de la canción (constante)
bailabilidad = 0.5

# Generar valores para la cantidad de bloques restantes
bloques_restantes = np.arange(0, 11)  # Por ejemplo, de 0 a 10 bloques restantes

# Calcular el parámetro lambda en función de la bailabilidad y los bloques restantes
lmbda = bailabilidad * bloques_restantes

# Generar datos siguiendo una distribución de Poisson
data=expon.pdf(scale=10,x=1/0.6)

# Graficar la distribución de Poisson
plt.bar(bloques_restantes, data)
plt.xlabel('Bloques Restantes')
plt.ylabel('Frecuencia')
plt.title('Distribución de Poisson basada en Bailabilidad y Bloques Restantes')
plt.show()

