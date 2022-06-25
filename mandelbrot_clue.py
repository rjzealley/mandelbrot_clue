""" mandelbrot_clue.py
Copyright R J Zealley 2020
Create and display a Mandelbrot set on an Adafruit Clue

See https://learn.adafruit.com/circuitpython-display-support-using-displayio
"""

import board
from adafruit_clue import clue
import displayio

# Max number of interations before selecting colour
MAX_ITER = 16

# Set board screen pixels
WIDTH = 240
HEIGHT = 240

# Plot window
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1


# Run the Mandelbrot function and return the number of iterations before resolving
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1
    return n


# Debug function to demonstrate  how the Mandelbrot function works
def show_values():
    for a in range(-10, 10, 5):
        for b in range(-10, 10, 5):
            c = complex(a / 10, b / 10)
            print(c, mandelbrot(c))


# Clear the screen and show all white
def clear_screen():
    # Make a background color fill
    color_bitmap = displayio.Bitmap(320, 240, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF
    bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
    splash.append(bg_sprite)


# Core function to run the Mandelbrot function over each pixel, using pixel values to generate a value respresenting a colour
# Colours used to create a bitmap, shown after all pixels processed
def draw_mandelbrot():
    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 16)
    color_palette = displayio.Palette(16)

    color_palette[0] = 0x000000
    color_palette[1] = 0x000080
    color_palette[2] = 0x008000
    color_palette[3] = 0x008080
    color_palette[4] = 0x800000
    color_palette[5] = 0x800080
    color_palette[6] = 0x808000
    color_palette[7] = 0xC0C0C0
    color_palette[8] = 0x808080
    color_palette[9] = 0x0000FF
    color_palette[10] = 0x00FF00
    color_palette[11] = 0x00FFFF
    color_palette[12] = 0xFF0000
    color_palette[13] = 0xFF00FF
    color_palette[14] = 0xFFFF00
    color_palette[15] = 0xFFFFFF

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            # Convert pixel coordinate to complex number
            c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                        IM_START + (y / HEIGHT) * (IM_END - IM_START))
            
			# Compute the number of iterations
            m = mandelbrot(c)
            
			# The color depends on the number of iterations
            color = 15 - int(m * 15 / MAX_ITER)

            # Plot the point colour on the bitmap
            color_bitmap[x,y] = color

	# Show the completed bitmap
    bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
    splash.append(bg_sprite)


# Debug function showing colour values calculated for each row, column
def calc_mandelbrot():
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            # Convert pixel coordinate to complex number
            c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                        IM_START + (y / HEIGHT) * (IM_END - IM_START))
            # Compute the number of iterations
            m = mandelbrot(c)
            # The color depends on the number of iterations
            color = 15 - int(m * 15 / MAX_ITER)
            # Plot the point
            print(str(x), str(y), str(color))


# Main function
# Show Mandelbrot hello message and wait for button press
# Button A, calcuatle and show Mandelbrot bitmap
# Button B, show calcs in REPL
if __name__ == "__main__":
    print("Mandelbrot:")

    while True:
        if clue.button_a:
			# Create a TileGrid 
            splash = displayio.Group(max_size=4)
            board.DISPLAY.show(splash)
			
			# Set screen to blank white
            clear_screen()
			
			# Calculate then display Mandelbrot set
            draw_mandelbrot()

        if clue.button_b:
			# Show Mandelbrot set calculations: row, column, colour
            calc_mandelbrot()
			