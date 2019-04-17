import time

nothing = -1
white = 0
black = 1

state = [
        [
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
        [
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
        [
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1, 1,
       -1,-1,-1,-1,-1,-1,-1,-1,
       -1,-1,-1,-1,-1,-1,-1,-1,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ]
]

class softwareTest():
    def print_value(y):
        if y == nothing:
            print("nothing ", end ='')
        elif y == black:
                print("black ", end ='')
        elif y == white:
            print("white ", end ='')
            
    def state_logic(i, j, prev_state, new_state):
        #current_state[i*8 + j] = new_state
        if prev_state == nothing and (new_state == black or new_state == white):
            print("piece placed 1")
            #onPiecePlaced(current_state)
        elif (prev_state == black or prev_state == white) and new_state == nothing:
            print("piece selected")
            #onPieceSelected(current_state)
        elif (prev_state == black and new_state == white) or (prev_state == white and new_state == black):
            print("piece placed 2")
            #onPiecePlaced(current_state)
            
    #while True:
    #sweep through inputs on mux
    for state_index in range(2):
        for i in range(8):
            #control_row_mux(i)
            for j in range(8):
                #control_col_mux(j)
                #x = interpret(chan_0.value)
                state_logic(i, j, state[state_index][i*8 +j], state[state_index + 1][i*8 +j] )

        #print ("current state of board:")
        #for i in range(64):
        #    print_value(current_state[i])
        #    if i % 8 == 7:
        #        print("\n")
        time.sleep(0.5)
