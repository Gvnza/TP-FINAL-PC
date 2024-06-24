import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import bernoulli

def gauss():
    teams = 50
    pokes_per_team = 6
    epochs = 50
    mutation_prob = 0.03
    simulation_cuantity = 1000
    total_mutaciones = []

    # Realizar simulaciones
    for _ in range(simulation_cuantity):
        mutaciones = np.zeros((epochs, teams, pokes_per_team))
        for epoca in range(epochs):
            for equipo in range(teams):
                for pokemon in range(pokes_per_team):
                    mutaciones[epoca, equipo, pokemon] = bernoulli.rvs(mutation_prob)
        total_mutaciones.append(np.sum(mutaciones))

    # Graficar la distribución de la cantidad de mutaciones
    plt.hist(total_mutaciones, bins=30, density=True, alpha=0.6, color='g')

    # Ajustar una curva gaussiana
    mu, sigma = np.mean(total_mutaciones), np.std(total_mutaciones)

    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)

    p = np.exp(-((x - mu)**2 / (2 * sigma**2))) / (np.sqrt(2 * np.pi) * sigma)

    plt.plot(x, p, 'k', linewidth=2)

    plt.xlabel('Total de mutaciones')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de la cantidad de mutaciones en 1000 simulaciones')
    plt.show()