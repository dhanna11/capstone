def BoardChangeToMove(newboardArray, oldboardArray):
    print(len(newboardArray))
    assert(len(newboardArray) == len(oldboardArray))
    for i in range(len(newboardArray)):
        # Castling handled as rook captures own piece
        if ((newboardArray[i] != -1) and (oldboardArray[i] == -1)):
            # white or black move
            dest_square = i       
        elif (newboardArray[i] == 0) and (oldboardArray[i] == 1):
            # black capture
            dest_square = i
        elif (newboardArray[i] == 1) and (oldboardArray[i] == 0):
            # white capture
            dest_square = i
        elif (newboardArray[i] == -1) and (oldboardArray[i] != -1):
            # new blank place implies source. May break en pasante
            source_square = i
        else:
            assert(newboardArray[i] == oldboardArray[i])
    
    return chess.Move(source_square, dest_square)

# White upper case, 1. Black lowercase, 0
# Blank negative -1
# Order matters
# FEN record starts from rank 8 and ends with rank 1
# and from file "a" to file "h"
def convertFENToTernaryList(fen_str):
    l = []
    fen_str_board = fen_str.split(" ")[0]
    fen_rows = fen_str_board.split("/")
    print(fen_rows)
    for string_row in fen_rows[::-1]:
        for c in string_row:
            print(c)
            if (c.isnumeric()):                
                l.extend([-1] * int(c))
            elif (c.islower()):
                l.append(0)
            elif (c.isupper()):
                l.append(1)

    assert(len(l) == 64)
    return l
