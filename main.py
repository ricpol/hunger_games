"""Python Hunger Games. 
Motore di gioco per testare le varie strategie e farle competere tra loro, 
costruito in base alle regole illustrate qui
https://brilliant.org/competitions/hunger-games/rules/

Questo script esemplifica come usare il programma. 
Occorre solo istanziare alcuni Players (cfr. players.py per i dettagli), 
quindi invocare una istanza di Game (cfr. game.py per i dettagli) e avviarla
chiamando main(). 

Il programma produce un file log.txt che riassume tutto cio' che e' avvenuto 
turno per turno.

(c) Riccardo Polignieri
Licenza GPL
"""


from game import Game
from players import *


g = Game([
    AlwaysHunt('ah1'),
    AlwaysHunt('ah2'),
    AlwaysSlack('as1'),
    AlwaysSlack('as2'),
    CyclicHunter('ch1'),
    CyclicHunter('ch2', cycle=5),
    CyclicHunter('ch3', cycle=10),
    ReputationHunter('rh1'),
    ReputationHunter('rh2'),
    ReputationHunter('rh3'),
    ReputationHunter('rh4'),
    ReputationHunter('rh5'),
    ReputationHunter('rh6'),
          ])
g.main()
