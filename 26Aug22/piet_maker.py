# Goal: a basic piet (image-based esoteric language) editor in Python 3
# notes: allows for the selection of codel color by either color-readable name or new rotating function by relative Piet standard
# known issue: white border after export (artifact after eps to png conversion)

import tkinter as tk
from PIL import Image
import os

# init
n = 10 # number of codels in each row and column
l = 50 # pixels per side length
codels = []

# window information
window = tk.Tk()
window.title("Piet Editor")
greeting = tk.Label(text="left click- update tile     |     right click- toggle outline")
greeting.pack()
canvas = tk.Canvas(window, width=n*l+1, height=n*l+1, bg="#000000")

# top frame
top = tk.Frame(window)
top.pack(side=tk.TOP, )

# color section (hue colors)
colors = [ "#FFC0C0", "#FF0000", "#C00000", "#FFFFC0", "#FFFF00", "#C0C000", "#C0FFC0", "#00FF00", "#00C000", "#C0FFFF", "#00FFFF", "#00C0C0", "#C0C0FF", "#0000FF", "#0000C0", "#FFC0FF", "#FF00FF", "#C000C0" ]
color_names = [ "light red", "red", "dark red", "light yellow", "yellow", "dark yellow", "light green", "green", "dark green", "light cyan", "cyan", "dark cyan", "light blue", "blue", "dark blue", "light magenta", "magenta", "dark magenta" ]
current_color = tk.StringVar(window)
current_color.set(color_names[0]) 
select_color = tk.OptionMenu(window, current_color, *color_names)
select_color.pack(in_=top, side=tk.LEFT)

# additional colors not in standard loop (white and black)
extra_colors = [ "#FFFFFF", "#000000" ]
extra_colors_names = [ "white", "black" ]
select_extra_color = tk.OptionMenu(window, current_color, *extra_colors_names)
select_extra_color.pack(in_=top, side=tk.LEFT)

all_colors_index = colors + extra_colors
all_colors_hex = color_names + extra_colors_names

# helper function
def loop_update_hue(current, relative):
    temp = current + relative
    for i in range(abs(relative)):
        if((current+i+1)%3==0): temp -= 3
    return temp

options = [ "current", "push", "pop", "+", "-", "*", "/", "mod", "not", ">", "pointer", "switch", "dup", "roll", "in(int)", "in(char)", "out(num)", "out(char)" ]
def update_color(x):
    color_index = all_colors_hex.index(current_color.get())
    new_index = color_index

    option_index = options.index(x)
    new_index = loop_update_hue(new_index, option_index) # updates to correct hue but may not be correct color

    new_index += 3 * (option_index//3) # correct color to match hue
    new_index = new_index%len(options) # prevents out of range issue

    current_color.set(color_names[new_index])

current_option = tk.StringVar(window)
current_option.set(options[0]) 
select_option = tk.OptionMenu(window, current_option, *options, command=update_color)
select_option.pack(in_=top, side=tk.LEFT)

outline_showing = True

def change_codel(e):
    use_color = all_colors_index[all_colors_hex.index(current_color.get())]

    outline_color = "#FFFFFF"
    if not outline_showing: outline_color=""
    canvas.itemconfig(codels[e.x//l][e.y//l], fill=use_color, outline=outline_color)

def toggle_outline(e):
    global outline_showing
    outline_showing = not outline_showing
    for x in range(n):
        for y in range(n):
            if canvas.itemcget(codels[x][y], "outline")=="":
                canvas.itemconfig(codels[x][y], outline="#FFFFFF") # change outline to white
            else:
                canvas.itemconfig(codels[x][y], outline="") # remove outline

# save button
def export_piet():
    canvas.postscript(file="temp.eps")
    img = Image.open("temp.eps")
    img.save("piet_program.png", "png")
    os.remove("temp.eps")
tk.Button(window, text="Export to png", command=export_piet).pack(in_=top, side=tk.RIGHT)

if __name__ == "__main__":
    # default grid
    for x in range(n):
        group = []
        for y in range(n):
            group.append(canvas.create_rectangle(x*l+3,y*l+3,x*l+l+3,y*l+l+3,fill="#000000"))
        codels.append(group)

    # event listener
    canvas.bind('<Button-1>', change_codel)    # change codel color
    canvas.bind('<Button-2>', toggle_outline)  # toggle outline around codels

    # gui output
    canvas.pack()

    # save
    window.mainloop()