from tkinter import *
import random
from PIL import Image, ImageTk

tk = Tk()
c = Canvas(tk, width=1280, height=1024, bg="white")
c.pack()
tk["bg"] = "black"

N = 9
vy = 136
color = {"red": ImageTk.PhotoImage(Image.open("images/red.png").resize((136,136), Image.ANTIALIAS)),
         "orange": ImageTk.PhotoImage(Image.open("images/orange.png").resize((136,136), Image.ANTIALIAS)),
         "blue": ImageTk.PhotoImage(Image.open("images/blue.png").resize((136,136), Image.ANTIALIAS)),
         "green": ImageTk.PhotoImage(Image.open("images/green.png").resize((136,136), Image.ANTIALIAS))}

res = []
cannon_creat = ImageTk.PhotoImage(Image.open("images/cannon.png").resize((144,168), Image.ANTIALIAS))
bullet_creat = ImageTk.PhotoImage(Image.open("images/bullet.png").resize((80,20), Image.ANTIALIAS))
cannon = c.create_image(170, 669, image=cannon_creat, anchor=NW)
bullet = []


def spawn_squ():
    x = 30
    for _ in range(N):
        cc = random.choice(list(color))
        res1 = c.create_image(x, -136, image=color[cc], anchor=NW, tag="down")
        c.tag_lower("down")
        res.append({"color": cc, "img": res1})
        x += 136
    c.after(5000, spawn_squ)
c.after(5000, spawn_squ)

def Move_squ():
    global vy, x_mouse, y_mouse
    for i in range(len(res)):
        res1 = res[i]["img"]
        c.move(res1, 0, vy)
    c.after(5000, Move_squ)
c.after(5000, Move_squ)

def spawn_bullet(event):
    for i in range(len(res)):
        res1 = res[i]["img"]
        #c.tag_lower("dow")
        x, y = c.coords(res1)
        if event.x > x and event.x <= x + 136 and event.y >= y and event.y <= y + 136:
            x_mouse = event.x
            y_mouse = event.y
            bullet1 = c.create_image(202, 669, image=bullet_creat, anchor=NW, tag="dow")
            bullet.append({"fill": bullet1})
c.bind("<Button-1>", spawn_bullet)

def Move_bullet():
    for i in range(len(bullet)):
        bullet1 = bullet[i]["fill"]
        c.move(bullet1, 0, -2)
    c.after(50, Move_bullet)
c.after(50, Move_bullet)

def Player():
    n = 0
    for j in range(len(bullet)):
        for i in range(len(res)):
            bullet1 = bullet[j - n]["fill"]
            x1, y1 = c.coords(bullet1)
            res1 = res[i]["img"]
            x2, y2 = c.coords(res1)
            if x1 > x2 and x1 < x2 + 136 and y1 >= y2 and y1 <= y2 +136:
                res2 = res[i]["color"]
                if res2 == "green":
                    c.delete(res[i]["img"])
                    c.delete(bullet[j - n]["fill"])
                    del res[i]['color']
                    del bullet[j-n]["fill"]
                    n += 1
                    if not 'color' in res[i]:
                        del res[i]
                    if not 'fill' in bullet[j]:
                        del bullet[j]
                        break
    c.after(50, Player)
c.after(50, Player)


mainloop()