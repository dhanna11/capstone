class CoreGame():

    def gameLoop():
        try:
            event = event_queue.get()
        except queue.Empty: 
            pass
        else:
            if isinstance(event, Event.PIECE_MOVED):
                oldboardArray = convertFENToTernaryList(board.fen())
                newboardArray = event.newboardArray
                print(oldboardArray)
                print(newboardArray)
                move = BoardChangeToMove(newboardArray, oldboardArray)
                print(move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move detected")
