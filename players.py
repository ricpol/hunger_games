"""Python Hunger Games. 
Motore di gioco per testare le varie strategie e farle competere tra loro, 
costruito in base alle regole illustrate qui
https://brilliant.org/competitions/hunger-games/rules/

Questo modulo raccoglie le strategie da far competere tra loro. 
Rispetto alle regole del gioco, cambiano solo due piccoli dettagli: 
1) le strategie *devono* essere espresse in termini OOP, quindi e' necessario
impacchettare la strategia in una classe. BasePlayer e una base astratta che 
fornisce l'API giusta, quindi raccomando di derivare le strategie da BasePlayer. 
2) ogni strategia (player) deve avere un nome (str), al solo scopo di 
identificarla nel log.  

Questo modulo raccoglie tre strategie di base:
- AlwaysHunt e' una strategia che sceglie sempre di cacciare con tutti
- AlwaysSlack sceglie invece sempre di non cacciare con nessuno
- CyclicHunter sceglie di cacciare (con tutti) solo una volta ogni n turni

Potete aggiungere le vostre strategie perfette qui!

(c) Riccardo Polignieri
Licenza GPL
"""

class BasePlayer(object):
    """Una classe astratta da cui derivare le strategie concrete. 
       Vedi le regole del gioco per i dettagli sulle signature dei metodi."""
    def __init__(self, name):
        self.name = name # un nome identificativo (str)
        
    def hunt_choices(self, round_number, current_food, current_reputation, 
                     m, player_reputations):
        # deve ritornare una lista di stringhe 'h' o 's'
        raise NotImplementedError
    
    def hunt_outcomes(self, food_earnings): pass
    def round_end(self, award, m, number_cooperators):pass



class AlwaysHunt(BasePlayer):
    def hunt_choices(self, round_number, current_food, current_reputation, 
                     m, player_reputations):
        return ['h'] * len(player_reputations)


class AlwaysSlack(BasePlayer):
    def hunt_choices(self, round_number, current_food, current_reputation, 
                     m, player_reputations):
        return ['s'] * len(player_reputations)


class CyclicHunter(BasePlayer):
    def __init__(self, name, cycle=2):
        BasePlayer.__init__(self, name)
        self.cycle = cycle
        self.counter = 1
        
    def hunt_choices(self, round_number, current_food, current_reputation, 
                     m, player_reputations):
        if self.counter == self.cycle:
            self.counter = 1
            return ['h'] * len(player_reputations)
        else:
            self.counter += 1
            return ['s'] * len(player_reputations)
            

