from math import sin, cos, radians
import random
import tkinter as tk

window = tk.Tk()
window.title("Asteroids Clone")
canvas = tk.Canvas(window, width=400, height=400, bg="#000000")
canvas.pack()

speed = 0
angle = 10
ship = canvas.create_polygon((0,0 , 5,15, 10,0), fill="#000000", outline="#ffffff")
def move_ship(x, y):
    # translation
    canvas.coords(ship, canvas.coords(ship)[0]+x, canvas.coords(ship)[1]+y, canvas.coords(ship)[2]+x, canvas.coords(ship)[3]+y, canvas.coords(ship)[4]+x, canvas.coords(ship)[5]+y)

    if(canvas.coords(ship)[0]+2.5<0): move_ship(400, 0)       # left edge wrap
    elif(canvas.coords(ship)[0]+2.5>400): move_ship(-400, 0)  # right edge wrap
    if(canvas.coords(ship)[1]+2.5<0): move_ship(0, 400)       # up edge wrap
    elif(canvas.coords(ship)[1]+2.5>400): move_ship(0, -400)  # down edge wrap
def rotate_ship(adjust_angle):
    cx = (canvas.coords(ship)[0]+canvas.coords(ship)[2]+canvas.coords(ship)[4])/3
    cy = (canvas.coords(ship)[1]+canvas.coords(ship)[3]+canvas.coords(ship)[5])/3

    # spaghetti proof of concept
    x0 = canvas.coords(ship)[0]-cx
    y0 = canvas.coords(ship)[1]-cy
    n_x0 = x0 * cos(radians(adjust_angle)) + y0 * sin(radians(adjust_angle)) + cx
    n_y0 = -x0 * sin(radians(adjust_angle)) + y0 * cos(radians(adjust_angle)) + cy

    x1 = canvas.coords(ship)[2]-cx
    y1 = canvas.coords(ship)[3]-cy
    n_x1 = x1 * cos(radians(adjust_angle)) + y1 * sin(radians(adjust_angle)) + cx
    n_y1 = -x1 * sin(radians(adjust_angle)) + y1 * cos(radians(adjust_angle)) + cy

    x2 = canvas.coords(ship)[4]-cx
    y2 = canvas.coords(ship)[5]-cy
    n_x2 = x2 * cos(radians(adjust_angle)) + y2 * sin(radians(adjust_angle)) + cx
    n_y2 = -x2 * sin(radians(adjust_angle)) + y2 * cos(radians(adjust_angle)) + cy
    canvas.coords(ship, n_x0, n_y0, n_x1, n_y1, n_x2, n_y2)
move_ship(200, 200)

bullets = []
def shoot_bullet():
    bullet_x = canvas.coords(ship)[2]
    bullet_y = canvas.coords(ship)[3]

    bullet = canvas.create_rectangle(bullet_x, bullet_y, (bullet_x+1), (bullet_y+1))
    bullets.append(bullet)

asteroids = []
asteroid_angles = []
def create_asteroid():
    rand_x = random.randrange(0, 400)
    rand_y = random.randrange(0, 400)
    asteroid = canvas.create_line([8+rand_x,8+rand_y, 8+rand_x,60+rand_y, 60+rand_x,80+rand_y, 80+rand_x,8+rand_y, 8+rand_x,8+rand_y], smooth='true', splinesteps=2)
    asteroids.append(asteroid)
    asteroid_angles.append(random.randrange(0, 360))
create_asteroid()

var = tk.StringVar()
history = []
def keyup(e):
    if  e.keycode in history :
        if e.keycode==822083616: shoot_bullet()
        history.pop(history.index(e.keycode))
        var.set(str(history))
def keydown(e):
    if not e.keycode in history :
        history.append(e.keycode)
        var.set(str(history))

counter = 0
def loop():
    global speed, angle, counter
    if 2113992448 in history and speed<5: speed += 0.01       # up
    if 2097215233 in history and speed>-2: speed -= 0.01      # down
    if 2063660802 in history:                                 # left
        angle += 1
        rotate_ship(1)
    if 2080438019 in history:                                 # right
        angle -= 1
        rotate_ship(-1)
    if(speed!=0): move_ship(speed*sin(radians(angle)), speed*cos(radians(angle)))
    
    # bullets
    for b in bullets:
        canvas.coords(b, canvas.coords(b)[0]+10*sin(radians(angle)),canvas.coords(b)[1]+10*cos(radians(angle)),canvas.coords(b)[2]+10*sin(radians(angle)),canvas.coords(b)[3]+10*cos(radians(angle)))
        if(abs(canvas.coords(b)[0])>400 or abs(canvas.coords(b)[2])>400): bullets.remove(b) # delete conditions

        # bullet collision
        b = canvas.coords(b)
        coll = canvas.find_overlapping(b[0], b[1], b[2], b[3])
        if(len(coll) > 1):
            canvas.itemconfig(coll[0], state = 'hidden')

    for a in asteroids:
        a_angle = asteroid_angles[asteroids.index(a)]
        a_speed = 3
        canvas.coords(a, canvas.coords(a)[0]+a_speed*sin(radians(a_angle)),canvas.coords(a)[1]+a_speed*cos(radians(a_angle)),canvas.coords(a)[2]+a_speed*sin(radians(a_angle)),canvas.coords(a)[3]+a_speed*cos(radians(a_angle)),canvas.coords(a)[4]+a_speed*sin(radians(a_angle)),canvas.coords(a)[5]+a_speed*cos(radians(a_angle)),canvas.coords(a)[6]+a_speed*sin(radians(a_angle)),canvas.coords(a)[7]+a_speed*cos(radians(a_angle)),canvas.coords(a)[8]+a_speed*sin(radians(a_angle)),canvas.coords(a)[9]+a_speed*cos(radians(a_angle)))
        if(abs(canvas.coords(a)[0])>400 or abs(canvas.coords(a)[2])>400): 
            asteroid_angles.remove(a_angle)
            asteroids.remove(a)

    counter += 1
    if(counter % 150 == 0): create_asteroid()

    # ship collision
    s = canvas.coords(ship)
    coll = canvas.find_overlapping(s[0], s[1], s[2], s[3])
    if(len(coll) < 2):
        window.after(10, loop)



if __name__ == "__main__":
    loop()

    window.bind("<KeyPress>", keydown)
    window.bind("<KeyRelease>", keyup)

    window.mainloop()