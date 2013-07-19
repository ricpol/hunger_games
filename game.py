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


txt_roundstart = "\nROUND %i; M: %i; players: %s\nreps: %s\nfood: %s\n"
txt_playerdecision = "player %s, hunts decision %s\n"
txt_foodearnings = "player %s, food earnings %s\n"
txt_award = "award: %i, tot hunters: %i, tot cooperators: %i\n"
txt_dead = "deads: %s\n"
txt_summary_log = "\nsummary of deaths:\n%s\n"

class Game(object):
    def __init__(self, players):
        self.players = players
        self.nameplayers = [p.name for p in players]
        self.num_players = len(players)
        self.hunts = [0.0] * self.num_players
        self.slacks = [0.0] * self.num_players
        self.foods = [300*(self.num_players-1)] * self.num_players
        self.round = 0
        self.log = open('log.txt', 'a')
    
    def _shuffle_players(self):
        """Dobbiamo dare ai giocatori le liste reputazione in ordine casuale, 
           ma anche ricordare in che ordine glie le abbiamo date...
           Per fare in fretta, le diamo a tutti nello stesso ordine
           (cambiando a ogni turno l'ordine dei giocatori)."""
        keys = range(self.num_players)
        random.shuffle(keys)
        self.players = [self.players[i] for i in keys]
        self.nameplayers = [self.nameplayers[i] for i in keys]
        self.hunts = [self.hunts[i] for i in keys]
        self.slacks = [self.slacks[i] for i in keys]
        self.foods = [self.foods[i] for i in keys]
    
    def do_round(self):
        self.round += 1
        # calcolo M
        m = random.randint(1, (self.num_players * (self.num_players-1))-1)
        # mescolo i giocatori
        self._shuffle_players()
        # calcolo le reputazioni correnti
        reps = []
        for h, s in zip(self.hunts, self.slacks):
            try: reps.append(h / (h+s))
            except ZeroDivisionError: reps.append(1.0)
        self.log.write(txt_roundstart % (self.round, m, str(self.nameplayers), 
                                         str(reps), str(self.foods)))
        tot_hunters = 0 # il numero di cacciatori totali (per il cibo premio)
        hunts = [] # matrice di chi caccia con chi
        
        for n, player in enumerate(self.players):
            reps_2 = reps[:]
            r = reps_2.pop(n) 
            hunt = player.hunt_choices(self.round, self.foods[n], r, m, reps_2)
            self.hunts[n] += hunt.count('h')
            self.slacks[n] += hunt.count('s')
            tot_hunters += hunt.count('h')
            hunt.insert(n, None) # re-inserisco None al posto del giocatore corrente
            hunts.append(hunt)
            self.log.write(txt_playerdecision % (self.nameplayers[n], str(hunt)))
        # distribuisco il cibo a seconda dei risultati della caccia
        tot_cooperators = 0
        for a in range(self.num_players):
            food_earning = []
            for b in range(self.num_players):
                if hunts[a][b] and hunts[b][a]:
                    res_a, res_b = FOODS[(hunts[a][b], hunts[b][a])]
                    if hunts[a][b] == hunts[b][a] == 'h':
                        tot_cooperators +=1
                    self.foods[a] += res_a
                    food_earning.append(res_a)
            self.players[a].hunt_outcomes(food_earning)
            self.log.write(txt_foodearnings % (self.nameplayers[a], str(food_earning)))
        # stabilisco se distribuire cibo aggiuntivo:
        if tot_hunters >= m:
            award = 2*(self.num_players-1)
            self.foods = [i+award for i in self.foods]
        else: 
            award = 0
        self.log.write(txt_award % (award, tot_hunters, tot_cooperators))
        # stabilisco se qualcuno e' morto:
        deads = [n for n, i in enumerate(self.foods) if i<1]
        deadnames = [i for i in self.nameplayers if self.nameplayers.index(i) in deads]
        self.log.write(txt_dead % str(deadnames))
        if deads: 
            self.num_players -= len(deads)
            self.players = [i for i in self.players if self.players.index(i) not in deads]
            self.nameplayers = [i for i in self.nameplayers if self.nameplayers.index(i) not in deads]
            self.foods = [i for i in self.foods if self.foods.index(i) not in deads]
            self.hunts = [i for i in self.hunts if self.hunts.index(i) not in deads]
            self.slacks = [i for i in self.slacks if self.slacks.index(i) not in deads]
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
            
