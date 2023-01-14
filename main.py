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

game_time = 0
res = []

color = {"red": ImageTk.PhotoImage(Image.open("images/cannon_red_new.png").resize((136, 136), Image.ANTIALIAS)),
         "blue": ImageTk.PhotoImage(Image.open("images/blue_new.png").resize((136, 136), Image.ANTIALIAS)),
         "green": ImageTk.PhotoImage(Image.open("images/green_new.png").resize((136, 136), Image.ANTIALIAS))}

background = ImageTk.PhotoImage(Image.open("images/backr.png").resize((1280, 1024), Image.ANTIALIAS))
bac = c.create_image(0, 0, image=background, anchor=NW)

base = ImageTk.PhotoImage(Image.open("images/base_2.png").resize((1280, 142), Image.ANTIALIAS))
base1 = c.create_image(0, 650, image=base, anchor=NW)
cannon_creat_green = ImageTk.PhotoImage(Image.open("images/green_conon_new_new.png"))
cannon_creat_blue = ImageTk.PhotoImage(Image.open("images/cannon_blue_new.png"))
cannon_creat_red = ImageTk.PhotoImage(Image.open("images/red_cannon_New.png"))


bullet_creat_green = ImageTk.PhotoImage(Image.open("images/bullet.png").resize((80, 20), Image.ANTIALIAS))
bullet_creat_blue = ImageTk.PhotoImage(Image.open("images/bullet_blue.png").resize((52, 88), Image.ANTIALIAS))

aim = ImageTk.PhotoImage(Image.open("images/aim2.png").resize((136, 136), Image.ANTIALIAS))
aim2 = c.create_image(30, -136, image=aim, anchor=NW)

cannon_green = c.create_image(250, 525, image=cannon_creat_green, anchor=NW)
cannon_blue = c.create_image(470, 527, image=cannon_creat_blue, anchor=NW)
cannon_red = c.create_image(970, 530, image=cannon_creat_red, anchor=NW)
c.tag_raise(cannon_green)

bullet = []
bullet_blue = []
time = 5000

black_hp = ImageTk.PhotoImage(Image.open("images/heart_black.png"))
red_hp = ImageTk.PhotoImage(Image.open("images/heart.png"))

hp5 = c.create_image(10, 730, image=red_hp, tag='down', anchor=NW)
hp4 = c.create_image(90, 730, image=red_hp, tag='down', anchor=NW)
hp3 = c.create_image(170, 730, image=red_hp, tag='down', anchor=NW)
hp2 = c.create_image(250, 730, image=red_hp, tag='down', anchor=NW)
hp = c.create_image(330, 730, image=red_hp, tag='down', anchor=NW)

class BulletClass:

    def __init__(self, tx, ty, image):
        self.tx = tx
        self.ty = ty
        self.image = image


def Move_aim_down():
    global time
    c.move(aim2, 0, vy)
    c.after(time, Move_aim_down)
c.after(time, Move_aim_down)

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
    global time
    x = 30
    for _ in range(N):
        cc = random.choice(list(color))
        res1 = c.create_image(x, -136, image=color[cc], anchor=NW)
        res.append({"color": cc, "img": res1})
        x += 136
    c.after(time, spawn_squ)
c.after(time, spawn_squ)


def Move_squ():
    global vy, time
    for i in range(len(res)):
        res1 = res[i]["img"]
        c.tag_raise(aim2, res1)
        c.move(res1, 0, vy)
    for j in range(len(bullet)):
        bullet1 = bullet[j]
        bullet1.ty += vy
    c.after(time, Move_squ)
c.after(time, Move_squ)


def spawn_bullet_green(event):
    for i in range(len(res)):
        res1 = res[i]["img"]
        x, y = c.coords(res1)
        x1, y1 = c.coords(aim2)
        x1 += 68
        y1 += 68
        if x < x1 <= x + 136 and y <= y1 <= y + 136:
            bullet1 = BulletClass(x1, y1,
                                  c.create_image(202, 669, image=bullet_creat_green, anchor=NW))
            c.tag_lower(bullet1.image)
            bullet.append(bullet1)


def spawn_bullet_blue(event):
    for i in range(len(res)):
        res1 = res[i]["img"]
        x, y = c.coords(res1)
        c.tag_raise(base1, res1)
        if event.x > x and event.x <= x + 136 and event.y >= y and event.y <= y + 136:
            bullet2 = c.create_image(496, 669, image=bullet_creat_blue, anchor=NW)
            c.tag_lower(bullet2)
            bullet_blue.append({"fill": bullet2})


def Move_two_bul(event):
    spawn_bullet_blue(event)
    spawn_bullet_green(event)


c.bind("<Button-1>", Move_two_bul)


def Move_bullet():
    t1 = []
    for i in range(len(bullet)):
        bullet1 = bullet[i]
        x3, y3 = c.coords(bullet1.image)
        s = (bullet1.tx - x3) ** 2 + (y3 - bullet1.ty) ** 2
        s2 = math.sqrt(s)
        coef = 35 / s2
        dy = -int((y3 - bullet1.ty)) * coef
        c.move(bullet1.image, int((bullet1.tx - x3) * coef), dy)
        x3, y3 = c.coords(bullet1.image)
        if x3 + 80 < 0 or y3 + 20 < 0 or dy > 0:
            t1.append(i)
    n = 0
    for j in range(len(t1)):
        b1 = bullet[t1[j] - n]
        del bullet[t1[j] - n]
        c.delete(b1.image)
        n += 1
    c.after(6, Move_bullet)
c.after(6, Move_bullet)


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
        bullet1 = bullet[i]
        x, y = c.coords(bullet1.image)
        if y < 660:
            c.tag_raise(bullet1.image)
    for j in range(len(bullet_blue)):
        bullet2 = bullet_blue[j]["fill"]
        x1, y1 = c.coords(bullet2)
        if y1 < 600:
            c.tag_raise(bullet2)
    c.after(50, Layer)
c.after(50, Layer)


def Player():
    t1 = []
    t2 = []
    for j in range(len(bullet)):
        bullet1 = bullet[j]
        x1, y1 = c.coords(bullet1.image)
        for i in range(len(res)):
            res1 = res[i]["img"]
            x2, y2 = c.coords(res1)
            if 0 < x1 - bullet1.tx + 40 < 136 and 0 < y1 - bullet1.ty + 20 < 136 \
                    and 0 < x1 - x2 < 136 and 0 < y1 - y2 < 136:
                res2 = res[i]["color"]
                if res2 == "green":
                    t1.append(i)
                t2.append(j)
                break
        n = 0
        for h in range(len(t1)):
            r1 = res[t1[h] - n]["img"]
            del res[t1[h] - n]['color']
            if not ('color' in res[t1[h] - n]):
                del res[t1[h] - n]
                c.delete(r1)
            n += 1
    n = 0
    for k in range(len(t2)):
        b1 = bullet[t2[k] - n]
        del bullet[t2[k] - n]
        c.delete(b1.image)
        n += 1
    c.after(50, Player)


c.after(50, Player)


def Player2():
    n = 0
    S = 0
    v = 0
    for j in range(len(bullet_blue)):
        for i in range(len(res)):
            bullet1 = bullet_blue[j - n]["fill"]
            x1, y1 = c.coords(bullet1)
            res1 = res[i]["img"]
            x2, y2 = c.coords(res1)
            if x2 < x1 < x2 + 136 and y2 <= y1 <= y2 + 136:
                res2 = res[i]["color"]
                if res2 == "blue":
                    c.delete(res[i]["img"])
                    c.delete(bullet_blue[j - n]["fill"])
                    del res[i]['color']
                    del bullet_blue[j - n]["fill"]
                    n += 1
                    if not 'color' in res[i]:
                        del res[i]
                    if not 'fill' in bullet_blue[j]:
                        del bullet_blue[j]
                        break
                else:
                    c.delete(bullet[j - S]["fill"])
                    del bullet[j - S]["fill"]
                    if not 'fill' in bullet[j]:
                        del bullet[j]
                    if v == 0:
                        h_p = c.create_image((80 * v) + 10, 950, image=black_hp, anchor=NW)
                    if v == 1:
                        h_p2 = c.create_image((80 * v) + 10, 950, image=black_hp, anchor=NW)
                    if v == 2:
                        h_p3 = c.create_image((80 * v) + 10, 950, image=black_hp, anchor=NW)
                    if v == 3:
                        h_p4 = c.create_image((80 * v) + 10, 950, image=black_hp, anchor=NW)
                    if v == 4:
                        h_p5 = c.create_image((80 * v) + 10, 950, image=black_hp, anchor=NW)
                    v += 1
                    break
    c.after(50, Player2)
c.after(50, Player2)

mainloop()
