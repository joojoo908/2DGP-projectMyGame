from pico2d import *
import math
import random

from Ground import Ground
from state_machine import *


WIDTH, HEIGHT = 1400 , 1000

def len(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
def angle(x1,y1,x2,y2):
    return math.atan2((y2-y1),(x2-x1))

class Player:
    # global viewX ,viewY
    global mouse_x, mouse_y
    # global mx,my
    image = None

    def __init__(self):
        self.x, self.y = 0, 0
        self.viewX, self.viewY = 0, 0
        self.mx,self.my = 0,0
        self.framex = 0
        self.framey = 10
        self.state = 0  # 0:idle 1: move  2: dash 3:attack1
        self.dire = 0  # 방향
        self.framecnt = 0

        self.image = load_image('red_hood.png')
        self.idle = load_image('red_hood_idle.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {mouse_click: Run},
            Run: {run_over: Idle ,mouse_click: Run }
              })

    def handle_event(self ,event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def update(self,vx,vy):
        self.viewX,self.viewY=vx,vy
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

class Idle:
    @staticmethod
    def enter(p1, e):
        p1.framecnt=0;
        pass

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        if p1.framecnt > 4:
            p1.framex = (p1.framex + 1) % 18
            p1.framecnt = 0;
        p1.framecnt += 1

    @staticmethod
    def draw(p1):
        playersize = 1.8
        if p1.dire == 0:
            p1.idle.clip_composite_draw(p1.framex * 80, 0, 80, 80
                                        , 0, 'i', WIDTH // 2 - p1.viewX + p1.x + 15,
                                        HEIGHT // 2 - p1.viewY + p1.y - 15, 140 * playersize, 140 * playersize)
        else:
            p1.idle.clip_composite_draw(p1.framex * 80, 0, 80, 80
                                        , 0, 'h', WIDTH // 2 - p1.viewX + p1.x - 15,
                                        HEIGHT // 2 - p1.viewY + p1.y - 15, 140 * playersize, 140 * playersize)

class Run:
    @staticmethod
    def enter(p1,e):
        p1.framecnt = 0
        p1.mx, p1.my = e[1].x-WIDTH//2 + p1.viewX,  HEIGHT -e[1].y- HEIGHT//2 + p1.viewY+50
        pass

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        if p1.framecnt > 4:
            p1.framex = (p1.framex + 1) % 12
            if p1.framex == 0:
                p1.framey = (p1.framey - 1) % 11
                if p1.framey == 8:
                    p1.framey = 10
                    p1.framex = 1
            p1.framecnt = 0
        p1.framecnt += 1

        speed=5
        mx, my = p1.mx,p1.my
        if len(p1.x, p1.y, mx, my) > speed:
            p1.dire = mx <= p1.x  # 플에이어가 바라보는 방향 설정
            # 플레이어가 일정 범위 밖일때 맵 전체 이동
            if math.cos(angle(p1.x, p1.y, mx, my)) < 0:
                if p1.x <= p1.viewX - 400:
                    p1.viewX += speed * math.cos(angle(p1.x, p1.y, mx, my))
            elif math.cos(angle(p1.x, p1.y, mx, my)) > 0:
                if p1.x >= p1.viewX + 400:
                    p1.viewX += speed * math.cos(angle(p1.x, p1.y, mx, my))
            if math.sin(angle(p1.x, p1.y, mx, my)) < 0:
                if p1.y <= p1.viewY - 200:
                    p1.viewY += speed * math.sin(angle(p1.x, p1.y, mx, my))
            elif math.sin(angle(p1.x, p1.y, mx, my)) > 0:
                if p1.y >= p1.viewY + 300:
                    p1.viewY += speed * math.sin(angle(p1.x, p1.y, mx, my))
            # 플레이어 이동
            p1.x += speed * math.cos(angle(p1.x, p1.y, mx, my))
            p1.y += speed * math.sin(angle(p1.x, p1.y, mx, my))
        else:
            p1.x = mx
            p1.y = my
            p1.state_machine.add_event(('RUN_OVER', 0))

    @staticmethod
    def draw(p1):
        size = 112
        playersize = 1.8
        if p1.dire == 0:
            p1.image.clip_composite_draw(p1.framex * size, p1.framey * 133, size, 133
                                           , 0, 'h', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y,
                                           200 * playersize, 200 * playersize)
        else:
            p1.image.clip_composite_draw(p1.framex * size, p1.framey * 133, size, 133
                                           , 0, 'i', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y,
                                           200 * playersize, 200 * playersize)
        #pass

class Dash:
    pass