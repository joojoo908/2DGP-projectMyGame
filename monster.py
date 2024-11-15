PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
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

animation_names = ['Walk','Idle','Dead']

WIDTH, HEIGHT = 1400 , 1000

class Monster:

    def __init__(self,x,y,type):
        self.x, self.y = x,y
        self.viewX, self.viewY = 0, 0
        if type == 1:
            self.idle = load_image('Flying_eye/Flight.png')
        self.frame = random.randint(0, 7)
        self.dir = 1

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def update(self,vx,vy):
        self.viewX, self.viewY = vx, vy
        self.state_machine.update()
        pass

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y
        skillsz = 50
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'boy:zombie':
            pass
        if group == 'zombie:ball':
            print('hit ball')
            game_world.remove_object(self)

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
