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

def print_value(y):
    if y == nothing:
        print("nothing ", end ='')
    elif y == black:
        print("black ", end ='')
    elif y == white:
        print("white ", end ='')
        
def state_logic(i, j, piece_prev_state, piece_new_state):
    #board_current_state[i*8 + j] = new_piece_state
    if (piece_prev_state == nothing
        and (piece_new_state == black or piece_new_state == white)):
        #piece_placed.emit(current_state)
        print("piece placed 1")
        
    elif ((piece_prev_state == black or piece_prev_state == white)
            and piece_new_state == nothing):
        #piece_selected.emit(current_state)
        print("piece selected")
        
    elif ((piece_prev_state == black and piece_new_state == white)
            or (piece_prev_state == white and piece_new_state == black)):
        #piece_placed.emit(current_state)'
        print("piece placed 2")
        
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