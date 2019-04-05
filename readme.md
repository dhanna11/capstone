High level architecture as of now:
Board object (one per smartchess board), and the GUI are observers (see observer design pattern) to core game state

Boards and GUI send events objects to a queue to be processed by coregame logic.

Core game logic also spawn's stockfish pondering threads for each position.

Events API:
  From GUI:     
     START_NEW_GAME
  From Board:
     PIECE_SELECTED
     PIECE_PLACED
     
Messages API:
   ILLEGAL_MOVE/BOARDSTATE
   NEW_POSITION
   CLOCK_TIME
   SELECT_SQUARES
   DELECT_SQUARES
   SWITCH TURN
   

TODO:
Write out actual UML diagrams
Produce a sequence diagram