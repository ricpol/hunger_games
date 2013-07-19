"""Python Hunger Games. 
Motore di gioco per testare le varie strategie e farle competere tra loro, 
costruito in base alle regole illustrate qui
https://brilliant.org/competitions/hunger-games/rules/

Questo modulo e' il motore del gioco, che funziona secondo le regole descritte 
(o almeno dovrebbe!). 
Non dovrebbero essere necessarie modifiche qui. Le strategie si impostano 
in players.py, e il gioco si avvia da main.py. 

L'unica cosa che, volendo, si puo' modificare sono END_GAME_TRIGGER e 
END_GAME_CHANCE, che regolano la lunghezza del gioco. Ovviamente, il gioco 
termina in ogni caso quando e' rimasto in vita solo un giocatore. 

Il gioco produce comune unico output un file log.txt 
che occorre consultare alla fine per scoprire chi ha vinto, e tutto il resto. 

(c) Riccardo Polignieri
Licenza GPL
"""

import random

FOODS = {('h', 'h'): (0, 0),
         ('s', 's'): (-2, -2), 
         ('h', 's'): (-3, 1), 
         ('s', 'h'): (1, -3)}

END_GAME_TRIGGER = 500 # dopo questo turno, innesca una possibilita' di abortire
END_GAME_CHANCE = .005 # possibilita' che il gioco abortisca subito


txt_roundstart = "\nROUND %i      M: %i\nnames: %s\nreps:  %s\nfood:  %s\n"
txt_playerdecision = "player %s, decision: %s\n"
txt_foodearnings = "player %s, earns: %s\n"
txt_award = "award: %i, tot hunters: %i, tot cooperators: %i\n"
txt_dead = "deads: %s\n"
txt_summary_log = "\nsummary of deaths:\n%s\n"

class PlayerStats(object):
    def __init__(self, player):
        self.hunt_choices = player.hunt_choices
        self.hunt_outcomes = player.hunt_outcomes
        self.round_end = player.round_end
        self.name = player.name
        self.hunts = 0.0
        self.slacks = 0.0
        self.food = 0
        self.reputation = 1.0
        
    def adjust_reputation(self):
        try: self.reputation = (self.hunts / (self.hunts + self.slacks)) 
        except ZeroDivisionError: self.reputation = 1.0
        

class Game(object):
    def __init__(self, players):
        self.players = [PlayerStats(p) for p in players]
        self.num_players = len(players)
        for p in self.players:
            p.food = 300*(self.num_players-1)
        self.round = 0
        self.log = open('log.txt', 'a')
        
    def do_round(self):
        self.round += 1
        # calcolo M
        m = random.randint(1, (self.num_players * (self.num_players-1))-1)
        # calcolo le reputazioni correnti
        for p in self.players: 
            p.adjust_reputation()
        self.log.write(txt_roundstart % (self.round, m, 
                                         str([p.name for p in self.players]),
                                         str([p.reputation for p in self.players]), 
                                         str([p.food for p in self.players])))
        tot_hunters = 0 # il numero di cacciatori totali (per il cibo premio)
        hunts = [] # matrice di chi caccia con chi
        
        for n, player in enumerate(self.players):
            other_reps = [p.reputation for p in self.players if p != player]
            # mescolo le reputazioni degli altri
            keys = range(self.num_players-1)
            random.shuffle(keys)
            other_reps = [other_reps[i] for i in keys]
            # chiedo al giocatore le sue decisioni di caccia
            hunt = player.hunt_choices(self.round, player.food, 
                                       player.reputation, m, other_reps)
            player.hunts += hunt.count('h')
            player.slacks += hunt.count('s')
            tot_hunters += hunt.count('h')
            # riordino le sue decisioni secondo l'ordine iniziale
            # (per chiarezza nel log)
            hunt = [h for k, h in sorted(zip(keys, hunt))]
            hunt.insert(n, 'X') # un segnaposto per il giocatore corrente
            hunts.append(hunt)
            self.log.write(txt_playerdecision % (player.name, str(hunt)))
        # distribuisco il cibo a seconda dei risultati della caccia
        tot_cooperators = 0
        for a, player in enumerate(self.players):
            food_earning = []
            for b in range(self.num_players):
                if hunts[a][b] != 'X' and hunts[b][a] != 'X':
                    res_a, res_b = FOODS[(hunts[a][b], hunts[b][a])]
                    if hunts[a][b] == hunts[b][a] == 'h':
                        tot_cooperators +=1
                    player.food += res_a
                    food_earning.append(res_a)
            self.players[a].hunt_outcomes(food_earning)
            self.log.write(txt_foodearnings % (self.players[a].name, str(food_earning)))
        # stabilisco se distribuire cibo aggiuntivo:
        if tot_hunters >= m:
            award = 2*(self.num_players-1)
            for player in self.players:
                player.food += award
        else: 
            award = 0
        self.log.write(txt_award % (award, tot_hunters, tot_cooperators))
        # stabilisco se qualcuno e' morto:
        deadnames = []
        for player in self.players:
            if player.food < 1: 
                deadnames.append(player.name)
        self.log.write(txt_dead % str(deadnames))
        if deadnames: 
            self.num_players -= len(deadnames)
            self.players = [p for p in self.players if p.name not in deadnames]
        # finisco il turno
        for player in self.players:
            player.round_end(award, m, tot_cooperators)
        return deadnames

    def main(self):
        summary_log = ''
        while True:
            if self.round > END_GAME_TRIGGER:
                if random.random() < END_GAME_CHANCE: 
                    summary_log += 'END GAME TRIGGERED'
                    break
            deads = self.do_round()
            if deads:
                summary_log += '%i: %s\n' % (self.round, str(deads))
            if self.num_players <= 1: 
                break
        self.log.write(txt_summary_log % summary_log)
            
