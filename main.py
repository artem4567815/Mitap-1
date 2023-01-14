from tkinter import *
import random
from PIL import Image, ImageTk
import math

tk = Tk()
tk.geometry("1280x1024")
c = Canvas(tk, width=1280, height=1024, bg="white")

c.pack()
tk["bg"] = "black"

N = 9
vy = 136

res = []

color = {"red": ImageTk.PhotoImage(Image.open("images/red.png").resize((136,136), Image.ANTIALIAS)),
         "orange": ImageTk.PhotoImage(Image.open("images/orange.png").resize((136,136), Image.ANTIALIAS)),
         "blue": ImageTk.PhotoImage(Image.open("images/blue.png").resize((136,136), Image.ANTIALIAS)),
         "green": ImageTk.PhotoImage(Image.open("images/green.png").resize((136,136), Image.ANTIALIAS))}

background = ImageTk.PhotoImage(Image.open("images/backr.png").resize((1280, 1024), Image.ANTIALIAS))
bac = c.create_image(0, 0, image=background, anchor=NW)


cannon_creat_green = ImageTk.PhotoImage(Image.open("images/cannon.png").resize((144,168), Image.ANTIALIAS))
cannon_creat_blue = ImageTk.PhotoImage(Image.open("images/blue_cannon.png").resize((324,168), Image.ANTIALIAS))

bullet_creat_green = ImageTk.PhotoImage(Image.open("images/bullet.png").resize((80,20), Image.ANTIALIAS))
bullet_creat_blue = ImageTk.PhotoImage(Image.open("images/bullet_blue.png").resize((52,88), Image.ANTIALIAS))

aim = ImageTk.PhotoImage(Image.open("images/aim2.png").resize((136,136), Image.ANTIALIAS))
aim2 = c.create_image(30, -136, image=aim, anchor=NW)

cannon_green = c.create_image(170, 669, image=cannon_creat_green, anchor=NW)
cannon_blue = c.create_image(360, 669, image=cannon_creat_blue, anchor=NW)
c.tag_raise(cannon_green)

bullet = []
bullet_blue = []


def Move_aim_down():
    c.move(aim2, 0, vy)
    c.after(5000, Move_aim_down)
c.after(5000, Move_aim_down)
def Move_aim(key):
    x, y = c.coords(aim2)
    print(y)
    print(y + 136)
    if key.char == "d" and x < 1118:
        c.move(aim2, 136, 0)
    if key.char == "a" and x > 30:
        c.move(aim2, -136, 0)
    if key.char == "w" and y > 0:
        c.move(aim2, 0, -136)
    if key.char == "s" and y <= y + 136:
        c.move(aim2, 0, 136)


tk.bind("<KeyPress>", Move_aim)
def spawn_squ():
    x = 30
    for _ in range(N):
        cc = random.choice(list(color))
        res1 = c.create_image(x, -136, image=color[cc], anchor=NW)
        res.append({"color": cc, "img": res1})
        x += 136
    c.after(5000, spawn_squ)
c.after(5000, spawn_squ)

def Move_squ():
    global vy
    for i in range(len(res)):
        res1 = res[i]["img"]
        c.tag_raise(aim2, res1)
        print(c.coords(res1))
        c.move(res1, 0, vy)
    c.after(5000, Move_squ)
c.after(5000, Move_squ)

def spawn_bullet_green(event):
    for i in range(len(res)):
        res1 = res[i]["img"]
        x, y = c.coords(res1)
        x1, y1 = c.coords(aim2)
        x1 += 68
        y1 += 68
        if x1 > x and x1 <= x + 136 and y1 >= y and y1 <= y + 136:
            bullet1 = c.create_image(202, 669, image=bullet_creat_green, anchor=NW)
            c.tag_lower(bullet1)
            bullet.append({"fill": bullet1})


def spawn_bullet_blue(event):
    for i in range(len(res)):
        res1 = res[i]["img"]
        x, y = c.coords(res1)
        if event.x > x and event.x <= x + 136 and event.y >= y and event.y <= y + 136:
            bullet2 = c.create_image(496, 669, image=bullet_creat_blue, anchor=NW)
            c.tag_lower(bullet2)
            bullet_blue.append({"fill": bullet2})

def Move_two_bul(event):
    spawn_bullet_blue(event)
    spawn_bullet_green(event)
c.bind("<Button-1>", Move_two_bul)
def Move_bullet():
    x, y = c.coords(aim2)
    x2 = x + 68
    y2 = y + 68
    for i in range(len(bullet)):
        bullet1 = bullet[i]["fill"]
        x3, y3 = c.coords(bullet1)
        s = (x2 - x3) ** 2 + (y3 - y2) ** 2
        s2 = math.sqrt(s)
        coef = 200/s2
        c.move(bullet1, int((x2 - x3) * coef), -int((y3-y2)) * coef)
    c.after(50, Move_bullet)
c.after(50, Move_bullet)

def Move_bullet_blue():
    c.tag_raise(cannon_blue)
    c.tag_raise(cannon_green)
    for i in range(len(bullet_blue)):
        bullet1 = bullet_blue[i]["fill"]
        c.move(bullet1, 0, -100)
    c.after(50, Move_bullet_blue)
c.after(50, Move_bullet_blue)

def Layer():
    for i in range(len(bullet)):
        bullet1 = bullet[i]["fill"]
        x, y = c.coords(bullet1)
        if y < 660:
            c.tag_raise(bullet1)
    for j in range(len(bullet_blue)):
        bullet2 = bullet_blue[j]["fill"]
        x1, y1 = c.coords(bullet2)
        if y1 < 600:
            c.tag_raise(bullet2)

    c.after(50, Layer)
c.after(50, Layer)
def Player():
    n = 0
    S = 0
    for j in range(len(bullet)):
        for i in range(len(res)):
            x5, y5 = c.coords(aim2)
            bullet1 = bullet[j - n]["fill"]
            x1, y1 = c.coords(bullet1)
            res1 = res[i]["img"]
            x2, y2 = c.coords(res1)
            # if x1 > x2 and x1 < x2 + 136 and y1 >= y2 and y1 <= y2 +136:
            #     res2 = res[i]["color"]
            #     if res2 == "green":
            #         c.delete(res[i]["img"])
            #         c.delete(bullet[j - n]["fill"])
            #         del res[i]['color']
            #         del bullet[j-n]["fill"]
            #         n += 1
            #         if not 'color' in res[i]:
            #             del res[i]
            #         if not 'fill' in bullet[j]:
            #             del bullet[j]
            #             break
            if x1 > x5 and x1 < x5 + 136 and y1 > y5 and y1 < y5 + 136 and x1 > x2 and x1 < x2 + 136 and y1 >= y2 and y1 <= y2 +136:
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
                else:
                    c.delete(bullet[j - S]["fill"])
                    del bullet[j - S]["fill"]
                    S += 1
                    if not 'fill' in bullet[j]:
                        del bullet[j]
                        break
    c.after(50, Player)
c.after(50, Player)

def Player2():
    n = 0
    for j in range(len(bullet_blue)):
        for i in range(len(res)):
            bullet1 = bullet_blue[j - n]["fill"]
            x1, y1 = c.coords(bullet1)
            res1 = res[i]["img"]
            x2, y2 = c.coords(res1)
            if x1 > x2 and x1 < x2 + 136 and y1 >= y2 and y1 <= y2 +136:
                res2 = res[i]["color"]
                if res2 == "blue":
                    c.delete(res[i]["img"])
                    c.delete(bullet_blue[j - n]["fill"])
                    del res[i]['color']
                    del bullet_blue[j-n]["fill"]
                    n += 1
                    if not 'color' in res[i]:
                        del res[i]
                    if not 'fill' in bullet_blue[j]:
                        del bullet_blue[j]
                        break
    c.after(50, Player2)
c.after(50, Player2)



mainloop()