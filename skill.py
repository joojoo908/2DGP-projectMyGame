Time_PER_ACTION =1
ACTION_PER_TIME =1.0/Time_PER_ACTION

PIXEL_PER_METER =(10.0/0.3)
ARROW_SPEED_KMPH = 100.0
ARROW_SPEED_MPM = (ARROW_SPEED_KMPH*1000.0/60.0)
ARROW_SPEED_MPS = (ARROW_SPEED_MPM/60.0)
ARROW_SPEED_PPS =(ARROW_SPEED_MPS*PIXEL_PER_METER)

import random
from pico2d import *
import game_world
import frame_work
import play_mod

WIDTH, HEIGHT = 1400 , 1000

class Skill1:
    image = None

    def __init__(self, x = 400, y = 300, vx=0,vy=0):
        self.frame =0
        self.viewX, self.viewY = vx, vy
        self.damage =40
        if Skill1.image == None:
            Skill1.image = load_image('skill/skill_sl.png')
        self.x, self.y = x, y

    def draw(self):
        self.image.clip_composite_draw(int(self.frame)*64, 3*64, 64, 64, 0, 'h',
                WIDTH // 2 - self.viewX + self.x, HEIGHT // 2 - self.viewY + self.y+20,
                500 , 500 )
        draw_rectangle(*self.get_bb())

    def update(self , x,y):
        self.viewX, self.viewY =x,y
        #self.x += self.velocity * 100 * frame_work.frame_time
        self.frame = (self.frame + 10 * ACTION_PER_TIME * frame_work.frame_time)

        if self.frame>10:
            game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y + 20
        skillsz=150
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def handle_collision(self, group, other):
        # fill here
        if group == 'boy:ball':
            game_world.remove_object(self)
        if group == 'zombie:ball':
            game_world.remove_object(self)
            #print('hit z')
        pass

class Skill2:
    image = None

    def __init__(self, x = 400, y = 300, vx=0,vy=0,dire=0):
        self.frame =0
        self.viewX, self.viewY = vx, vy
        self.damage =80
        if Skill2.image == None:
            Skill2.image = load_image('skill/B.png')
        self.x, self.y = x, y
        self.dire = 1 if dire else -1

    def draw(self):
        self.image.clip_composite_draw(int(self.frame)*64, 4*64, 64, 64, 0, 'h',
                WIDTH // 2 - self.viewX + self.x -100*self.dire, HEIGHT // 2 - self.viewY + self.y+120,
                300 , 500 )
        draw_rectangle(*self.get_bb())

    def update(self , x,y):
        self.viewX, self.viewY =x,y
        self.frame = (self.frame + 10 * ACTION_PER_TIME * frame_work.frame_time)

        if self.frame>10:
            game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x-100*self.dire
        y = HEIGHT // 2 - self.viewY + self.y + 120
        skillsz=200
        return x - skillsz/2, y - skillsz, x + skillsz/2, y + skillsz

    def handle_collision(self, group, other):

        pass

class Skill3:
    image = None

    def __init__(self, x = 400, y = 300, vx=0,vy=0):
        self.frame =0
        self.viewX, self.viewY = vx, vy
        self.damage =0
        if self.image == None:
            self.image = load_image('skill/D.png')
        self.x, self.y = x, y
        #self.dire = 1 if dire else -1

    def draw(self):
        self.image.clip_composite_draw(int(self.frame)*64, 1920-64*2, 64, 64, 0, 'h',
                WIDTH // 2 - self.viewX + self.x , HEIGHT // 2 - self.viewY + self.y,
                300 , 300 )

    def update(self , x,y):
        self.viewX, self.viewY =x,y
        self.frame = (self.frame + 10 * ACTION_PER_TIME * frame_work.frame_time)

        if self.frame>10:
            game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y
        skillsz=200
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def handle_collision(self, group, other):

        pass

class Skill4:
    image = None

    def __init__(self, x = 400, y = 300, vx=0,vy=0):
        self.frame =0
        self.viewX, self.viewY = vx, vy
        self.damage =0
        if self.image == None:
            self.image = load_image('skill/skill_sl.png')
        self.x, self.y = x, y

    def draw(self):
        self.image.clip_composite_draw(int(self.frame)%10*64, 6*64, 64, 64, 0, 'h',
                WIDTH // 2 - self.viewX + self.x , HEIGHT // 2 - self.viewY + self.y,
                200 , 200 )
        #draw_rectangle(*self.get_bb())

    def update(self, x,y):
        self.viewX, self.viewY =x,y
        self.x , self.y = play_mod.p1.x ,play_mod.p1.y
        self.frame = ( self.frame + 10 * ACTION_PER_TIME * frame_work.frame_time)

        if self.frame>24:
            play_mod.p1.invincible = 0
            game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y + 20
        skillsz=150
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def handle_collision(self, group, other):
        # fill here
        if group == 'boy:ball':
            game_world.remove_object(self)
        if group == 'zombie:ball':
            game_world.remove_object(self)
            #print('hit z')
        pass

class Skill5:
    image = None

    def __init__(self, x = 400, y = 300, vx=0,vy=0):
        self.startframe= 0
        self.frame =self.startframe
        self.viewX, self.viewY = vx ,vy
        self.damage =30
        if self.image == None:
            self.image = load_image('skill/skill_sl.png')
        self.x, self.y = x+ random.randint(-300, 300), y+ random.randint(-300, 300)

    def draw(self):
        self.image.clip_composite_draw(int(self.frame)%10*64, 4*64, 64, 64, 0, 'h',
                WIDTH // 2 - self.viewX + self.x, HEIGHT // 2 - self.viewY + self.y+20,
                300 , 300 )
        #draw_rectangle(*self.get_bb())

    def update(self , x,y):
        self.viewX, self.viewY =x,y
        #self.x += self.velocity * 100 * frame_work.frame_time
        self.frame = (self.frame + 10 * ACTION_PER_TIME * frame_work.frame_time)

        if self.frame>self.startframe+30:
            game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y + 20
        skillsz=100
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def handle_collision(self, group, other):
        # fill here
        if group == 'boy:ball':
            game_world.remove_object(self)
        if group == 'zombie:ball':
            game_world.remove_object(self)
            #print('hit z')
        pass

class Skill6:
    image = None

    def __init__(self, x = 400, y = 300, vx=0,vy=0,angle=0):
        self.frame =0
        self.viewX, self.viewY = vx, vy
        self.damage =150
        if self.image == None:
            self.image = load_image('skill/C.png')
        self.x, self.y = x, y
        self.angle = angle

    def draw(self):
        self.image.clip_composite_draw(int(self.frame)%6*64, 21*64, 64, 64, 3.14+self.angle, 'h',
                WIDTH // 2 - self.viewX + self.x, HEIGHT // 2 - self.viewY + self.y,
                200 , 50 )
        draw_rectangle(*self.get_bb())

    def update(self , x,y):
        self.viewX, self.viewY =x,y
        self.x +=math.cos(self.angle) * ARROW_SPEED_PPS * frame_work.frame_time
        self.y +=math.sin(self.angle) * ARROW_SPEED_PPS * frame_work.frame_time
        self.frame = (self.frame + 10 * ACTION_PER_TIME * frame_work.frame_time)

        if self.frame>20:
            game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y
        skillsz=50
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def handle_collision(self, group, other):
        if group == 'mop:p1_atk':
            pass
            #game_world.remove_object(self)
            #print('atk')
        pass

class Mop_atk1:
    image = None

    def __init__(self, x = 400, y = 300, vx =0,vy =0):
        self.frame =0
        self.viewX, self.viewY = vx,vy
        self.damage =15
        self.x, self.y = x, y

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self , x,y):
        self.viewX, self.viewY = x,y
        #self.frame = (self.frame + 1 * ACTION_PER_TIME * frame_work.frame_time)

        #if self.frame>1:
        game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y
        skillsz=100
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def handle_collision(self, group, other):
        # fill here
        if group == 'mop:p1_atk':
            game_world.remove_object(self)

class Mop_atk2:
    image = None

    def __init__(self, x = 400, y = 300, vx =0,vy =0):
        self.frame =0
        self.viewX, self.viewY = vx,vy
        self.damage =20
        self.x, self.y = x, y

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self , x,y):
        self.viewX, self.viewY = x,y
        #self.frame = (self.frame + 1 * ACTION_PER_TIME * frame_work.frame_time)

        #if self.frame>1:
        game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y
        skillsz=200
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def handle_collision(self, group, other):
        # fill here
        if group == 'mop:p1_atk':
            game_world.remove_object(self)

class Boss_atk1:
    image = None

    def __init__(self, x = 400, y = 300, vx =0,vy =0):
        self.frame =0
        self.viewX, self.viewY = vx,vy
        self.damage =15
        self.x, self.y = x, y

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self , x,y):
        self.viewX, self.viewY = x,y
        #self.frame = (self.frame + 1 * ACTION_PER_TIME * frame_work.frame_time)

        #if self.frame>1:
        game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y
        skillsz=100
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def handle_collision(self, group, other):
        # fill here
        if group == 'mop:p1_atk':
            game_world.remove_object(self)
