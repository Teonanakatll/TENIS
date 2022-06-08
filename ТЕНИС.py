from tkinter import *
from random import randint
from time import sleep
from winsound import Beep

# Анимация уровня
def animeUp():
    global anim, animeAfter, lev

    if (anim == 2):
        lev = cnv.create_text(WIDTH // 2, 200, text=f"Уровень {level}", font="Purisa 50",
                    fill="#ff00ff")
    
    anim -= 1
    print(anim)
    if (anim > 0):
        animeAfter = cnv.after(1000, animeUp)
    else:
        cnv.after_cancel(animeAfter)
        cnv.delete(lev)
        anim = 2
 
    

# Уровни
def levelUp():
    global level, vectorX, vectorY, move

    level += 1
    if (level < 5):
        move -= 5
        animeUp()

    

# Новый раунд
def newRound():
    global start, ball
    if (scL > 0 or scR > 0):
        ball = cnv.create_image(WIDTH // 2, HEIGHT // 2, image=circle)
        cnv.update()
        for i in range(len(stStart)):
            stringStart = stStart[i]
            start = cnv.create_text(WIDTH // 2, 200,text=stringStart,
                        font="Purisa 30", fill="#fff800")
            cnv.update()
            sleep(1.0)        
            cnv.delete(start)
    
        
    score()
    vector()
    moveBall()

# Счёт
def score():
    global scoreL, scoreR
    if (scL > 0 or scR > 0):
        cnv.delete(scoreL, scoreR)
    scoreL = cnv.create_text(450, 50, text=scL, font="Purisa 40", fill="#fff800")
    scoreR = cnv.create_text(750, 50, text=scR, font="Purisa 40", fill="#fff800")

# Старт игры
def startGame(event):
    global start
    cnv.unbind("<space>")
    cnv.delete(start)
    for i in range(len(stStart)):
        stringStart = stStart[i]
        start = cnv.create_text(WIDTH // 2, 200,text=stringStart,
                        font="Purisa 30", fill="#fff800")
        cnv.update()
        sleep(1.0)        
        cnv.delete(start)
    newRound()
    
# Движение досок
def moveBoards(key):
    yL = cnv.coords(boardL)[1]
    yR = cnv.coords(boardR)[1]
    
    if (key == 0):
        if (yR > 100):
            cnv.move(boardR, 0, -player)
        else:
            return 0
    elif (key == 1):
        if (yR < 600):
            cnv.move(boardR, 0, player)
        else:
            return 0

    elif (key == 2):
        if (yL > 100):
            cnv.move(boardL, 0, -player)
        else:
            return 0
    elif (key == 3):
        if (yL < 600):
            cnv.move(boardL, 0, player)
        else:
            return 0


# Движение шара
def moveBall():
    global ballAfter, vectorX, vectorY, scL, scR, hit
    cnv.move(ball, vectorX, vectorY)
    
    x = cnv.coords(ball)[0]
    y = cnv.coords(ball)[1]

    yL = cnv.coords(boardL)[1]
    yR = cnv.coords(boardR)[1]   

    if (x >= WIDTH - 55 or x <= 55):
        if (y > yL - 100 and y < yL + 100) or (y > yR - 100 and y < yR + 100):
            vectorX = -vectorX
            
            hit += 1
            print(hit)
            if (hit == 3):
                
                hit = 0
                levelUp()
                
    elif (y > HEIGHT - 32 or y < 32):
        vectorY = -vectorY
    ballAfter = cnv.after(move, moveBall)
        
    if (x < -32 or x > 1232):
        if (x < -32):
            scL += 1
            cnv.delete(ball)
        elif (x > 1232):
            scR += 1
            cnv.delete(ball)
        
        score()
        cnv.after_cancel(ballAfter)
        newRound()
    
    
     

# Расчитываем направление шара
def vector():
    global vectorX, vectorY

    a = randint(0, 1)
    b = randint(0, 1)
    if (a == 1):
        vectorX = -vectorX
    if (b == 1):
        vectorY = -vectorY
    
    

root = Tk()

WIDTH = 1200
HEIGHT = 700

root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Тенис")
root.iconbitmap("ico.ico")
root.resizable(False, False)

# Создаем виджет
cnv = Canvas(root, width=WIDTH, height=HEIGHT)
cnv.config(highlightthickness=0)
cnv.place(x=0, y=0)
cnv.focus_set()

# Фон
back = PhotoImage(file="Buddha.png")
cnv.create_image(WIDTH // 2, HEIGHT // 2, image=back)

# Шар
circle = PhotoImage(file="circle.png")
ball = cnv.create_image(WIDTH // 2, HEIGHT // 2, image=circle)

# Константы кнопок
UPKEY = 0
DOWNKEY = 1
WKEY = 2
SKEY = 3

# Клавиши управления
cnv.bind("<Up>", lambda e, x = UPKEY: moveBoards(x))
cnv.bind("<Down>", lambda e, x = DOWNKEY: moveBoards(x))
cnv.bind("<w>", lambda e, x = WKEY: moveBoards(x))
cnv.bind("<s>", lambda e, x = SKEY: moveBoards(x))
cnv.bind("<space>", startGame)

# Скорость шара и досок
vectorX = 8
vectorY = 8
player = 70

# Переменные счёта
scL = 0
scR = 0

# Переменная и список начала
stringStart = "Для начала игры нажмите пробел"

stStart = ["3", "2", "1", "Поехали!"]

# Лейблы счёта и старта
start = cnv.create_text(WIDTH // 2, 200,text=stringStart,
                        font="Purisa 30", fill="#fff800")
#scoreL = cnv.create_text(450, 50, text="", font="Purisa 40", fill="#fff800")
#scoreR = cnv.create_text(750, 50, text="", font="Purisa 40", fill="#fff800")

# Количество отбитий
hit = 0

# Уровень
level = 0

# Доски
boa = PhotoImage(file="bo.png")
boardL = cnv.create_image(11, HEIGHT // 2, image=boa)
boardR = cnv.create_image(1189, HEIGHT // 2, image=boa)

# Скорость шара
move = 30

# Aнимация уровня
anim = 2

lev = cnv.create_text(WIDTH // 2, anim, text="", font="Purisa 50",
                    fill="#ff00ff")



# Запущена ли игра?
playGame = False

root.mainloop()
