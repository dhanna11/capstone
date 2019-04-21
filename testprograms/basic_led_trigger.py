import time
import board
import neopixel


class board_LED:
    pixel_pin = board.D18
    num_pixels = 64
    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                               pixel_order=ORDER)

    #converts board position to corresponding led position
    def led_index(raw_index):
        #only change for odd rows
        if(raw_index % 16 >= 8):
            row = raw_index//8
            add_index = 8 * (row+1) - 1 - raw_index
            led_index = 8*row + add_index
            return led_index
        else:
            return raw_index

    def led_piece_selected(pos):
        #light up the selected piece in red
        pixels[led_index(pos)] = (255,0,0)
    
    def led_possible_move(pos):
        #lighting up the rest in green
        pixels[pos] = (0,255,0) 
    
    #
    def led_piece_placed():
        pixels.fill(0,0,0)
    
    
