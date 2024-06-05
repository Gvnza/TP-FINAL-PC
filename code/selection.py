import random
import team_battle

def selection(number_of_teams, number_of_battles):
    teams_dicc, teams = team_battle.fights(number_of_teams, number_of_battles)
    total_wins = sum(list(teams_dicc.values()))
    probability = {}
    for key in teams_dicc.keys():
        probability[key] = int(teams_dicc[key])/total_wins

    keys = list(probability.keys())
    top10 = keys[:11]
    top5 = keys[:6]
    top3 = keys[:4]
    values = list(probability.values())
    totalcount10 = 0
    totalcount5 = 0
    totalcount3 = 0
    for _ in range(1000):
        count10 = 0
        count3 = 0
        count5 = 0
        for _ in range(15):
            r1 = random.choices(population= keys, weights=values)
            if r1[0] in top10:
                count10 += 1
                if r1[0] in top5:
                    count5 += 1
                    if r1[0] in top3:
                        count3 += 1
            else:
                print(r1)
        totalcount10 += count10
        totalcount3 += count3
        totalcount5 += count5
    totalcount5 = totalcount5/1000
    totalcount10 = totalcount10/1000
    totalcount3 = totalcount3/1000
    print(f'Toma al top 20% un {totalcount10*100/15}')
    print(f'Toma al top 10% un {totalcount5*100/15}')
    print(f'toma al top 5% un {totalcount3*100/15}')
    
selection(50, 400)