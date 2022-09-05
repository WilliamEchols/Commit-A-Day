# Goal: a visualizer for an algorithmic sort
# note: my implementation of the Quicksort algorith is baed on examples found at https://en.wikipedia.org/wiki/Quicksort

import tkinter as tk
import random
import time

rectangles = []

values = []
num = 100

def draw_rects(h_arr, low, high):
    for i in range(len(rectangles)): # clear
        canvas.delete(rectangles[i])
    border = 10
    w = (600-border)/num
    for i in range(num): # draw new rects
        if i>=low and i<=high: outline="#0f0" # in range
        elif i<low: outline="#f00" # before range
        else: outline = "#fff" # after/catch all
        rect = canvas.create_rectangle(w*i+border, border, w*(i+1), border+h_arr[i], outline=outline)
        rectangles.append(rect)

# quicksort
def quicksort_partition(low, high, vals):
    pivot = vals[high]
    ptr = low
    for i in range(low, high):
        if vals[i] <= pivot:
            vals[i], vals[ptr] = vals[ptr], vals[i] # swap
            ptr += 1
    vals[ptr], vals[high] = vals[high], vals[ptr] # swap
    return ptr
def quicksort(low, high, vals):
    if low==num: # terminate
        return vals
    if low < high: # main loop
        pi = quicksort_partition(low, high, vals)
        quicksort(low, pi-1, vals)
        quicksort(pi+1, high, vals)

    canvas.update()
    time.sleep(0.1)
    draw_rects(vals, low, high)

    return vals

if __name__ == "__main__":
    values = []
    for i in range(num):
        values.append(random.randrange(0, 400))

    window = tk.Tk()
    window.title("Quicksort Visualizer")
    canvas = tk.Canvas(window, width=600, height=400, bg="#000000")
    canvas.pack()

    draw_rects(values, 0, 0)

    quicksort(0, len(values)-1, values)

    window.mainloop()

