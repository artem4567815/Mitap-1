from tkinter import *
import random
from PIL import Image, ImageTk

tk = Tk()
tk.geometry("1280x1024")
tk.attributes('-fullscreen', True)
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
background = ImageTk.PhotoImage(Image.open("images/backgr.png").resize((1280, 1024), Image.ANTIALIAS))
cannon_creat_green = ImageTk.PhotoImage(Image.open("images/cannon.png").resize((144,168), Image.ANTIALIAS))
cannon_creat_blue = ImageTk.PhotoImage(Image.open("images/blue_cannon.png").resize((324,168), Image.ANTIALIAS))

bullet_creat_green = ImageTk.PhotoImage(Image.open("images/bullet.png").resize((80,20), Image.ANTIALIAS))
bullet_creat_blue = ImageTk.PhotoImage(Image.open("images/bullet_blue.png").resize((52,88), Image.ANTIALIAS))

cannon_green = c.create_image(170, 669, image=cannon_creat_green, anchor=NW)
cannon_blue = c.create_image(360, 669, image=cannon_creat_blue, anchor=NW)

bac = c.create_image(0, 0, image=background, anchor=NW, tag="DOWN")
c.tag_lower("DOWN")

bullet = []
bullet_blue = []



def spawn_squ():
    x = 30
    for _ in range(N):
        cc = random.choice(list(color))
        res1 = c.create_image(x, -136, image=color[cc], anchor=NW, tag="down")
        #c.tag_lower("down")
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

def spawn_bullet_green(event):
    for i in range(len(res)):
        res1 = res[i]["img"]
        #c.tag_lower("dow")
        x, y = c.coords(res1)
        if event.x > x and event.x <= x + 136 and event.y >= y and event.y <= y + 136:
            bullet1 = c.create_image(202, 669, image=bullet_creat_green, anchor=NW, tag="dow")
            bullet.append({"fill": bullet1})
#c.bind("<Button-1>", spawn_bullet_green)

def spawn_bullet_blue(event):
    for i in range(len(res)):
        res1 = res[i]["img"]
        x, y = c.coords(res1)
        if event.x > x and event.x <= x + 136 and event.y >= y and event.y <= y + 136:
            bullet2= c.create_image(496, 669, image=bullet_creat_blue, anchor=NW, tag="dowj")
            bullet_blue.append({"fill": bullet2})

def Move_two_bul(event):
    spawn_bullet_blue(event)
    spawn_bullet_green(event)
c.bind("<Button-1>", Move_two_bul)
def Move_bullet():
    for i in range(len(bullet)):
        bullet1 = bullet[i]["fill"]
        c.move(bullet1, 0, -2)
    c.after(50, Move_bullet)
c.after(50, Move_bullet)

def Move_bullet_blue():
    for i in range(len(bullet_blue)):
        bullet1 = bullet_blue[i]["fill"]
        c.move(bullet1, 0, -2)
    c.after(50, Move_bullet_blue)
c.after(50, Move_bullet_blue)

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