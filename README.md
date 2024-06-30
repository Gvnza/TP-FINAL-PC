# TP-FINAL-PC

Trabajo final pensamiento computacional. 

Archivos ejecutables:
    Simulation.py - Simulacion de las epocas, se puede cambiar el número de epocas en el for de la linea 44. Hace los graficos y los CSVs
    Main.py - Hace lo mismo que Simulation.py y toma al mejor equipo y lo hace pelear con el rival que elijas.

Cambios:
    Implementacion del crítico: Hay un 4% de probabilidad de que se efectue un golpe crítico.
    'Fixeo' de los ataques - Había un problema en la forma en la que se verificaba si el ataque fallaba o no - las presiciones estaban en funcion de 100 y se verificaba 
                             con un random.random() el cual esta en funcion de 1 (O sea, las presiciones iban de 0 a 100 y el random.random() de 0 a 1). Se multiplicó por 
                             100 el random.random()
    Algoritmo Genetico:
        Equipos:
            Se hace pelear a los 2 equipos elegidos (los cuales se eligen segun el % de victorias de todos los equipos que representan)   
            Mutacion - Solo pueden mutar los pokemones del equipo perdedor
            Se eligen en un 75% de los casos a los pokemones del equipo ganador
        Rivales:
            Si el promedio de batallas ganadas por equipo es mayora 350 y los rivales no aumentaron sus estadísticas en la anterior época, estos mejoran sus estadiísticas 
            Cuando sus estadísticas mejoran, solo mejoran 3 al azar Si el pokemon no es legendario
            Los rivales tienen un pokemon legendario asegurado, y pueden tener un máximo de 2.
    Gráficos:
        Se añadieron unos cuantos gráficos:
            Gauss:
                Hace mil simulaciones (no realmente, solo toma los datos y probabilidades) y usando bernoulli de scipy.stats y numpy se un grafico que sea una campana de gauss
                y otro que muestre cuantas veces se repitio una cantidad de simulaciones (ya que es un histograma, se reparten en 30 bins)
            Victorias:
                Las victorias del mejor equipo y el mejor rival por epoca.
                Promedio de victorias de los equipos por época.
        
    
