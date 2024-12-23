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
import end_mod
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
        self.type=type
        if type == 0:
            self.hp =500
            self.idle = load_image('boss/Idle.png')
            self.move = load_image('boss/Move.png')
            self.atk = load_image('boss/Attack.png')
            self.dmg = load_image('boss/Take_Hit.png')
            self.death = load_image('boss/Death.png')
        elif type == 1:
            self.hp =100
            self.idle = load_image('Flying_eye/Flight.png')
            self.move = load_image('Flying_eye/Flight.png')
            self.atk = load_image('Flying_eye/Attack.png')
            self.dmg = load_image('Flying_eye/Take_Hit.png')
            self.death = load_image('Flying_eye/Death.png')
        elif type==2:
            self.hp = 200
            self.idle = load_image('Skeleton/Idle.png')
            self.move = load_image('Skeleton/Walk.png')
            self.atk = load_image('Skeleton/Attack.png')
            self.dmg = load_image('Skeleton/Take_Hit.png')
            self.death = load_image('Skeleton/Death.png')

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

        self.time = get_time()

    def update(self,vx,vy):
        self.viewX, self.viewY = vx, vy
        self.state_machine.update()
        x,y = play_mod.p1.return_xy()

        if self.type==0:
            if self.hp<300:
                if get_time()-self.time>10:
                    self.time = get_time()
                    print('boss time')
                    for _ in range(10):
                        attack = Boss_atk2(self.x, self.y, self.viewX, self.viewY)
                        game_world.add_object(attack)
                        game_world.add_collision_pair('p1:mop_atk', None, attack)

            if self.atk_mode!=2:
                if len(x, y, self.x, self.y) > 800:
                    self.atk_mode = 0
                    self.state_machine.add_event(('IDLE', 0))
                elif len(x, y, self.x, self.y) > 130:
                    self.state_machine.add_event(('MOVE', 0))
                else:
                    self.state_machine.add_event(('ATK', 0))
            else:
                if len(x,y,self.x,self.y) <800:
                    self.atk_mode = 1
        elif self.type==1:
            if self.atk_mode!=2:
                if len(x, y, self.x, self.y) > 500:
                    self.atk_mode = 0
                    self.state_machine.add_event(('IDLE', 0))
                elif len(x, y, self.x, self.y) > 130:
                    self.state_machine.add_event(('MOVE', 0))
                else:
                    self.state_machine.add_event(('ATK', 0))
            else:
                if len(x,y,self.x,self.y) <500:
                    self.atk_mode = 1
        elif self.type==2:
            if self.atk_mode!=2:
                if len(x, y, self.x, self.y) > 600:
                    self.atk_mode = 0
                    self.state_machine.add_event(('IDLE', 0))
                elif len(x, y, self.x, self.y) > 180:
                    self.state_machine.add_event(('MOVE', 0))
                else:
                    self.state_machine.add_event(('ATK', 0))
            else:
                if len(x,y,self.x,self.y) <600:
                    self.atk_mode = 1

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y
        if self.type==0:
            skillsz = 50
        elif self.type==1:
            skillsz = 50
        elif self.type==2:
            skillsz = 100
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def draw(self):
        self.state_machine.draw()
        #draw_rectangle(*self.get_bb())

    def attack(self):
        if self.type==0:
            self.sound = load_wav('music/boss1.mp3')
            self.sound.set_volume(42)
            self.sound.play()
            attack = Boss_atk1(self.x,self.y,self.viewX,self.viewY)
        elif self.type==1:
            self.sound = load_wav('music/mop1.mp3')
            self.sound.set_volume(42)
            self.sound.play()
            attack = Mop_atk1(self.x,self.y,self.viewX,self.viewY)
        elif self.type==2:
            self.sound = load_wav('music/sward.mp3')
            self.sound.set_volume(32)
            self.sound.play()
            attack = Mop_atk2(self.x, self.y, self.viewX, self.viewY)

        game_world.add_object(attack)
        game_world.add_collision_pair('p1:mop_atk', None, attack)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'mop:p1_atk':
            if self.atk_mode!=2:
                self.atk_mode = 2
                self.state_machine.add_event(('DMG', 0))
                self.damage=other.damage

class Idle:
    @staticmethod
    def enter(self, e):

        pass

    @staticmethod
    def exit(self, e):
        pass

    @staticmethod
    def do(self):
        if self.type==1 or self.type==0:
            maxframe = 8
        else:
            maxframe = 4
        self.frame = (self.frame + FRAME_PER_ACTION * ACTION_PER_TIME * frame_work.frame_time) %maxframe
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
        if self.type==1 or self.type==0:
            maxframe = 8
        else:
            maxframe = 4
        self.frame = (self.frame + FRAME_PER_ACTION * ACTION_PER_TIME * frame_work.frame_time) % maxframe
        x, y = play_mod.p1.return_xy()
        if x < self.x:
            self.dir = -1
        else:
            self.dir = 1
        set_speed = 1
        if self.type==2:
            set_speed=0.7

        movingx = math.cos(angle(self.x, self.y, x, y)) *set_speed* RUN_SPEED_PPS * frame_work.frame_time
        movingy = math.sin(angle(self.x, self.y, x, y)) *set_speed* RUN_SPEED_PPS * frame_work.frame_time

        if not game_world.ck_ground(self.x + movingx, self.y + movingy):
            self.x += movingx
            self.y += movingy

        # self.x += movingx
        # self.y += movingy



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
        if self.type==0:
            self.attack()
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
        self.sound = load_wav('music/mop_dmg.mp3')
        self.sound.set_volume(42)
        self.sound.play()
        self.frame = 0
        pass

    @staticmethod
    def exit(self, e):
        self.atk_mode=1
        self.hp -= self.damage
        print('mop_hp:',self.hp)
        self.damage=0
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + 4 * ACTION_PER_TIME * frame_work.frame_time)
        if self.frame > 4:
            self.frame = 0
            if self.hp <= 0:
                self.state_machine.add_event(('DEATH', 0))
            else:
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
            if self.death_cnt==0:
                play_mod.p1.exp += 100
            if self.death_cnt <250:
                self.death_cnt = (self.death_cnt + 100 * ACTION_PER_TIME * frame_work.frame_time)
            else:
                if self.type==0:
                    play_mod.p1.bgm.set_volume(0)
                    frame_work.change_mode(end_mod)
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
