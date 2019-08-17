from tkinter import Tk as makescreen, Canvas, PhotoImage

class Crab:
    def __init__(self):
        self.image = canvas.create_image(1450, 550, image=mob3image)
        self.maxhp = 10
        self.hp = 10
        self.active = False

    def move(self):
        canvas.move(self.image, -60, 0)

class llama:
    def __init__(self):
        self.image = canvas.create_image(1450, 550, image=mob2image)
        self.maxhp = 30
        self.hp = 30
        self.active = False

    def move(self):
        canvas.move(self.image, -30, 0)

class slime:
    def __init__(self):
        self.image = canvas.create_image(1450, 550, image=mob1image)
        self.maxhp = 20
        self.hp = 20
        self.active = False
        self.jump = False
        self.jumpspeed = -30

    def move(self):
        global gravity
        canvas.move(self.image, -35, 0)

        pos = canvas.coords(self.image)
        if pos[1] > 550:
            self.jump = False
            self.jumpspeed = -30
            canvas.coords(self.image, pos[0], 550)
        else:
            canvas.move(self.image, 0, self.jumpspeed)
            self.jumpspeed += gravity

        if not self.jump:
            self.jump = True

class Boss:

    def __init__(self):
        self.image=canvas.create_image(1500, 500, image=bossimage)
        self.maxhp = 200
        self.hp=200
        self.active = False

    def move(self):
        player_pos = canvas.coords(player)
        boss_pos = canvas.coords(self.image)
        distance = abs(boss_pos[0] - player_pos[0])

        if distance > 100:
            if player_pos[0] < boss_pos[0]:
                canvas.move(self.image, -20, 0)
            else:
                canvas.move(self.image, 20, 0)





def move_left(event):
    global moved_distance
    global boss_battle
    if not game_over:
        player_pos = canvas.coords(player)
        if not boss_battle:
            canvas.move(bg, 30, 0)
            canvas.move(bg2, 30, 0)

            bg_pos = canvas.coords(bg)
            if bg_pos[0] > 2100:
                canvas.move(bg, -2800, 0)
            elif bg_pos[0] < -700:
                canvas.move(bg, 2800, 0)

            bg_pos = canvas.coords(bg2)
            if bg_pos[0] > 2100:
                canvas.move(bg2, -2800, 0)
            elif bg_pos[0] < -700:
                canvas.move(bg2, 2800, 0)
            for mob in active_mob_list:
                canvas.move(mob.image, 30, 0)
            moved_distance -= 30
        elif player_pos[0]>0: canvas.move(player, -30,0)


def move_right(event):
    global moved_distance
    global boss_battle
    global boss
    global jumppower
    if not game_over:
        player_pos = canvas.coords(player)
        if not boss_battle:
            canvas.move(bg, -30, 0)
            canvas.move(bg2, -30, 0)

            bg_pos = canvas.coords(bg)
            if bg_pos[0] > 2100:
                canvas.move(bg, -2800, 0)
            elif bg_pos[0] < -700:
                canvas.move(bg, 2800, 0)

            bg_pos = canvas.coords(bg2)
            if bg_pos[0] > 2100:
                canvas.move(bg2, -2800, 0)
            elif bg_pos[0] < -700:
                canvas.move(bg2, 2800, 0)
            for mob in active_mob_list:
                canvas.move(mob.image, -30, 0)
            moved_distance += 30
            if moved_distance >= 1 * 1400:
                boss_battle = True
                boss = Boss()
                active_mob_list.append(boss)
                jumppower = -50


        elif player_pos[0]<1400: canvas.move(player, 30, 0)


shoot_cooldown = True

def cooldown_reset():
    global shoot_cooldown
    shoot_cooldown = True

def shooting():

    global game_over
    global active_bullet_list
    global inactive_bullet_list

    if not game_over:
         if len(inactive_bullet_list) > 0:
            bullet = inactive_bullet_list[0]
            active_bullet_list.append(bullet)
            del inactive_bullet_list[0]
            canvas.itemconfig(bullet, state='normal')
            player_pos = canvas.coords(player)
            canvas.coords(bullet, (player_pos[0]) + 70, player_pos[1] -5)


def shootevent(event):
    global shoot_cooldown
    if shoot_cooldown:
        shooting()
        shoot_cooldown = False
        canvas.after(900, cooldown_reset)

jump = False
jumppower = -30
jumpspeed = jumppower
gravity = 4
def jumping():
    global jump, jumpspeed, gravity
    jump = True
    pos = canvas.coords(player)
    if pos[1] > 550:
        jump = False
        jumpspeed = jumppower
        canvas.coords(player, pos[0], 550)
    else:
        canvas.move(player, 0, jumpspeed)
        jumpspeed += gravity
        canvas.after(50, jumping)


def jumpevent(event):
    global jump

    if not game_over:
        if not jump:
            jumping()


active_mob_list = []  #empty list
inactive_mob_list = list()
boss = None
game_over = False
moved_distance = 0
boss_battle = False
active_bullet_list = [] #empty list
inactive_bullet_list = list()


def mob_initiate():
    global game_over
    global active_mob_list
    global inactive_mob_list

    if not game_over:
        if len(inactive_mob_list) > 0:
            mob = inactive_mob_list[0]
            mob.hp = mob.maxhp
            active_mob_list.append(mob)
            del inactive_mob_list[0]
            canvas.itemconfig(mob.image, state='normal')
            canvas.coords(mob.image, 1450, 550)

    if not boss_battle:
        canvas.after(3000, mob_initiate)


def game_loop():
    global game_over
    global active_mob_list
    global inactive_mob_list
    global active_bullet_list
    global inactive_bullet_list
    global boss

    if not game_over:
    #monster movement
        for mob in active_mob_list:
            mob.move()
            mob_x = canvas.coords(mob.image)[0]

            if mob_x<0:
                canvas.itemconfig(mob.image, state='hidden')
                inactive_mob_list.append(mob)
                active_mob_list.remove(mob)

        # if boss is not None:
            # boss.move()

     # bullet movement
        for bullet in active_bullet_list:
            canvas.move(bullet, 100, 0)
            bullet_x = canvas.coords(bullet)[0]

            if bullet_x > 1450:
                canvas.itemconfig(bullet, state='hidden')
                inactive_bullet_list.append(bullet)
                active_bullet_list.remove(bullet)


    #player collision
        player_pos = canvas.coords(player)
        for mob in active_mob_list:
            mob_pos = canvas.coords(mob.image)
            diff_x = abs(player_pos[0] - mob_pos[0])
            diff_y = abs(player_pos[1] - (mob_pos[1]))


            if diff_x < 50 and diff_y < 50:  # if there is an intersection player and mob
                canvas.itemconfig(gameover_text, state='normal')
                game_over = True
    #bullet collision
        for mob in active_mob_list:
            mob_pos = canvas.coords(mob.image)
            for bullet in active_bullet_list:
                bullet_pos = canvas.coords(bullet)
                diff_x = abs(bullet_pos[0] - mob_pos[0])
                diff_y = abs(bullet_pos[1] - (mob_pos[1]))


                if diff_x < 70 and diff_y < 60:  # if there is an intersection between bullet and mob
                    canvas.itemconfig(bullet, state='hidden')
                    inactive_bullet_list.append(bullet)
                    active_bullet_list.remove(bullet)
                    mob.hp -= 10
                    if mob.hp <= 0:
                        canvas.itemconfig(mob.image, state='hidden')
                        inactive_mob_list.append(mob)
                        active_mob_list.remove(mob)


    canvas.after(100, game_loop)


if __name__ == '__main__':
    screen = makescreen()
    screen.title('countefeit metalslug')
    screen.resizable(False, False)

    canvas = Canvas(screen, width=1400, height=672)
    canvas.pack()
    screen.update()

#load image

    playergunimage = PhotoImage(file='player.gun.png')
    mob1image = PhotoImage(file='pixil-frame-0-2.png')
    mob2image = PhotoImage(file='pixil-frame-0-4.png')
    mob3image = PhotoImage(file='pixil-frame-0-5.png')
    bgimage = PhotoImage(file='bg.png')
    bg2image = PhotoImage(file='bg2.png')
    bulletimage=PhotoImage(file='bullet.image.png')
    bossimage=PhotoImage(file='boss.png')
    axeupimage = PhotoImage(file='axe up.png')
    axerightimage = PhotoImage(file='axeright.png')
    fireimage = PhotoImage(file='boss bullet.png')

    bg = canvas.create_image(700,336, image=bgimage)
    bg2 = canvas.create_image(2100, 336, image=bg2image)
    player = canvas.create_image(200,550, image=playergunimage)
    gameover_text = canvas.create_text(700, 336, text='GAME OVER', font=('times new roman', 108), fill='black')
    canvas.itemconfig(gameover_text, state='hidden')

    #monster initialization
    for i in range(3):
        inactive_mob_list.append(Crab())
        inactive_mob_list.append(llama())
        inactive_mob_list.append(slime())

        bullet = canvas.create_image(0, 0, image=bulletimage)
        canvas.itemconfig(bullet, state='hidden')
        inactive_bullet_list.append(bullet)

    canvas.bind_all("<Left>", move_left)
    canvas.bind_all("<Right>", move_right)
    canvas.bind_all("<Up>", jumpevent)
    canvas.bind_all("<space>", shootevent)

    game_loop()
    mob_initiate()

    screen.mainloop()

