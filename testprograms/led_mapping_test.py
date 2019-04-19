def led_index(raw_index):
    #only change for odd rows
    if(raw_index % 16 >= 8):
        row = raw_index//8
        add_index = 8 * (row+1) - 1 - raw_index
        led_index = 8*row + add_index
        print(led_index)
    else:
        print(raw_index)

def main():
    print("simple test for mapping raw index on board to led index")
    led_index(7)

main()