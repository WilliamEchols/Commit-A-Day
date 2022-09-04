import tkinter as tk

def create_hexagon(x, y, hex):
    rel = 0.86625
    s = 40
    canvas.create_polygon((x,s+y , rel*s+x,0.5*s+y, rel*s+x,-0.5*s+y , x,-s+y , -rel*s+x,-0.5*s+y , -rel*s+x,0.5*s+y), fill="#000000", outline=hex)

def create_hexagon_line(x, y, n):
    inc = 70
    for i in range(n):
        create_hexagon(i*inc+x, y, "#fff")

turn_num = 0
def click_handler(e):
    global turn_num
    x = (e.x - 35) // 70
    y = (e.y - 35) // 70
    
    x_offset = 0
    if(y%2!=0): 
        x = e.x // 70
        x_offset = -35

    y_offset = -(y-2)*10

    if(turn_num%2==0): hex = "#f00"
    else: hex = "#0f0"
    if(((y==0 or y==4) and x>0 and x<4) or ((y==1 or y==3) and x>0 and x<5) or (y==2 and x>=0 and x<5)):
        create_hexagon((x+1)*70+x_offset, (y+1)*70+y_offset, hex)

        turn_num += 1

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Hexagon Tic Tac Toe")
    canvas = tk.Canvas(window, width=6 * 70, height=6 * 70, bg="#000000")
    canvas.pack()

    # hexagon board
    b = 35
    for i in range(5):
        v = 4-i
        c = v-i
        if(v<2): v = i
        create_hexagon_line(b*v, b*(i+1)*2+(c*5), 7-v)

    canvas.bind("<Button-1>", click_handler)

    window.mainloop()