from skill import Mop_atk1

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

Time_PER_ACTION =1
ACTION_PER_TIME =1.0/Time_PER_ACTION
FRAME_PER_ACTION=8

import random
import math
from state_machine import *
import frame_work
import game_world
import play_mod
from pico2d import *
from skill import *

def len(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def angle(x1,y1,x2,y2):
    return math.atan2((y2-y1),(x2-x1))

WIDTH, HEIGHT = 1400 , 1000

class Monster:
    def __init__(self,x,y,type):
        self.x, self.y = x,y
        self.viewX, self.viewY = 0, 0
        if type == 1:
            self.hp =100
            self.idle = load_image('Flying_eye/Flight.png')
            self.move = load_image('Flying_eye/Flight.png')
            self.atk = load_image('Flying_eye/Attack.png')
            self.dmg = load_image('Flying_eye/Take_Hit.png')
            self.death = load_image('Flying_eye/Death.png')

        self.frame = random.randint(0, 7)
        self.dir = 1
        self.atk_mode=0
        self.death_cnt = 0

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {move: Move ,atk:Atk, dmg:Dmg},
            Move: {idle:Idle, atk:Atk, dmg:Dmg},
            Atk: {idle:Idle, dmg:Dmg},
            Dmg:{idle:Idle,death:Death},
            Death:{}
        })

    def update(self,vx,vy):
        self.viewX, self.viewY = vx, vy
        self.state_machine.update()
        x,y = play_mod.p1.return_xy()
        if self.atk_mode:
            if len(x, y, self.x, self.y) > 500:
                self.atk_mode = 0
                self.state_machine.add_event(('IDLE', 0))
            elif len(x, y, self.x, self.y) > 140:
                self.state_machine.add_event(('MOVE', 0))
            else:
                self.state_machine.add_event(('ATK', 0))

        else:
            if len(x,y,self.x,self.y) <500:
                self.atk_mode = 1

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y
        skillsz = 50
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def attack(self):
        attack = Mop_atk1(self.x,self.y,self.viewX,self.viewY)
        game_world.add_object(attack)
        game_world.add_collision_pair('p1:mop_atk', None, attack)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'mop:p1_atk':
            if self.atk_mode!=2:
                self.atk_mode =2
                self.state_machine.add_event(('DMG', 0))
                self.hp -=other.damage
                print('mop hp: ',self.hp)

class Idle:
    @staticmethod
    def enter(self, e):

        pass

    @staticmethod
    def exit(self, e):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAME_PER_ACTION * ACTION_PER_TIME * frame_work.frame_time) % FRAME_PER_ACTION
        x ,y=play_mod.p1.return_xy()
        if x<self.x:
            self.dir=-1
        else:
            self.dir =1

    @staticmethod
    def draw(self):
        mopsize = 500
        if self.dir == 1:
            self.idle.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                        , 0, 'i', WIDTH // 2 - self.viewX + self.x ,
                                        HEIGHT // 2 - self.viewY + self.y , mopsize,mopsize)
        else:
            self.idle.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                        , 0, 'h', WIDTH // 2 - self.viewX + self.x,
                                        HEIGHT // 2 - self.viewY + self.y , mopsize,mopsize)

class Move:
    @staticmethod
    def enter(self, e):

        pass

    @staticmethod
    def exit(self, e):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAME_PER_ACTION * ACTION_PER_TIME * frame_work.frame_time) % FRAME_PER_ACTION
        x, y = play_mod.p1.return_xy()
        if x < self.x:
            self.dir = -1
        else:
            self.dir = 1

        movingx = math.cos(angle(self.x, self.y, x, y)) * RUN_SPEED_PPS * frame_work.frame_time
        movingy = math.sin(angle(self.x, self.y, x, y)) * RUN_SPEED_PPS * frame_work.frame_time

        self.x += movingx
        self.y += movingy

    @staticmethod
    def draw(self):
        mopsize = 500
        if self.dir == 1:
            self.move.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                          , 0, 'i', WIDTH // 2 - self.viewX + self.x,
                                          HEIGHT // 2 - self.viewY + self.y, mopsize, mopsize)
        else:
            self.move.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                          , 0, 'h', WIDTH // 2 - self.viewX + self.x,
                                          HEIGHT // 2 - self.viewY + self.y, mopsize, mopsize)

class Atk:
    @staticmethod
    def enter(self, e):
        self.frame = 0
        pass

    @staticmethod
    def exit(self, e):
        self.attack()
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAME_PER_ACTION * ACTION_PER_TIME * frame_work.frame_time)
        x, y = play_mod.p1.return_xy()
        if x < self.x:
            self.dir = -1
        else:
            self.dir = 1

        if self.frame > 8:
            self.frame = 0
            self.state_machine.add_event(('IDLE', 0))

    @staticmethod
    def draw(self):
        mopsize = 500
        if self.dir == 1:
            self.atk.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                          , 0, 'i', WIDTH // 2 - self.viewX + self.x,
                                          HEIGHT // 2 - self.viewY + self.y, mopsize, mopsize)
        else:
            self.atk.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                          , 0, 'h', WIDTH // 2 - self.viewX + self.x,
                                          HEIGHT // 2 - self.viewY + self.y, mopsize, mopsize)

class Dmg:
    @staticmethod
    def enter(self, e):
        self.frame = 0
        pass

    @staticmethod
    def exit(self, e):
        self.atk_mode=1
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + 4 * ACTION_PER_TIME * frame_work.frame_time)

        if self.frame > 4:
            self.frame = 0
            if self.hp <= 0:
                self.state_machine.add_event(('DEATH', 0))
            self.state_machine.add_event(('IDLE', 0))

    @staticmethod
    def draw(self):
        mopsize = 500
        if self.dir == 1:
            self.dmg.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                          , 0, 'i', WIDTH // 2 - self.viewX + self.x,
                                          HEIGHT // 2 - self.viewY + self.y, mopsize, mopsize)
        else:
            self.dmg.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                          , 0, 'h', WIDTH // 2 - self.viewX + self.x,
                                          HEIGHT // 2 - self.viewY + self.y, mopsize, mopsize)

class Death:
    @staticmethod
    def enter(self, e):
        self.frame = 0
        self.death_cnt = 0
        pass

    @staticmethod
    def exit(self, e):
        pass

    @staticmethod
    def do(self):
        if self.frame < 3:
            self.frame = (self.frame + 4 * ACTION_PER_TIME * frame_work.frame_time)
        else:
            if self.death_cnt <250:
                self.death_cnt = (self.death_cnt + 100 * ACTION_PER_TIME * frame_work.frame_time)
            else:
                game_world.remove_object(self)

    @staticmethod
    def draw(self):
        mopsize = 500
        if self.frame > 3:
            self.death.opacify( int(self.death_cnt) )
        if self.dir == 1:
            self.death.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                          , 0, 'i', WIDTH // 2 - self.viewX + self.x,
                                          HEIGHT // 2 - self.viewY + self.y, mopsize, mopsize)
        else:
            self.death.clip_composite_draw(int(self.frame) * 150, 0, 150, 150
                                          , 0, 'h', WIDTH // 2 - self.viewX + self.x,
                                          HEIGHT // 2 - self.viewY + self.y, mopsize, mopsize)
