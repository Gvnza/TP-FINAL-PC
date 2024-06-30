from simulation import simulation
from final_battles import battle, init_pygame

def main():
    best_team = simulation()
    rival = int(input('Elije a tu rival [1, 2, 3, 4, 5]\n'))
    while rival not in [1, 2, 3, 4, 5]:
        rival = int(input('Elije a tu rival [1, 2, 3, 4, 5]\n'))
    init_pygame()
    battle(best_team, rival)

if __name__ == '__main__':
    main()


