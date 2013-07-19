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

ah1 = AlwaysHunt('ah1')
ah2 = AlwaysHunt('ah2')
ah3 = AlwaysHunt('ah3')
as1 = AlwaysSlack('as1')
as2 = AlwaysSlack('as2')
as3 = AlwaysSlack('as3')
ch1 = CyclicHunter('ch1')
ch2 = CyclicHunter('ch2', cycle=5)
ch3 = CyclicHunter('ch3', cycle=10)
ch4 = CyclicHunter('ch4', cycle=15)

g = Game([ah1, ah2, ah3, as1, as2, as3, ch1, ch2, ch3, ch4])
g.main()
