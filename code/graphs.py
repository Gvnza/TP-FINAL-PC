import matplotlib.pyplot as plt

def standard_graphs(average_list, result_list, time_per_epoch, best_teams):
    average_wins(average_list, result_list)
    time_per_epoch(time_per_epoch)
    best_teams_wins(best_teams)
    

def average_wins(average_list, result_list):
    plt.plot(average_list, 'forestgreen', label='Equipos')
    plt.plot(result_list, 'firebrick', label='Rivales')
    plt.xlabel('Época')
    plt.ylabel('Promedio de Victorias')
    plt.title('Promedio de Victorias por Epoca')
    plt.legend()
    plt.show()

def time_per_epoch(time_per_epoch):
    plt.plot(time_per_epoch, 'indigo')
    plt.xlabel('Época')
    plt.ylabel('Tiempo (s)')
    plt.title('Tiempo por época')
    plt.show()

def best_teams_wins(best_teams):
    plt.plot(best_teams, 'gold')
    plt.xlabel('Época')
    plt.ylabel('Batallas ganadas')
    plt.title('Mejor equipo por época')
    plt.show()


