
from pico2d import *
import math
import random

WIDTH, HEIGHT = 1280 , 1024
click =False;
x,y =0,0

class player:
    global click
    global x,y
    def __init__(self):
        self.x,self.y = 500,500
        self.framex = 0
        self.framey = 10
        self.state = 0  # 0:idle 1: move
        self.dire =0
        self.image = load_image('red_hood.png')
        self.idle = load_image('red_hood_idle.png')

    def update(self):
        #------애니메이션---
        if self.state==0:
            self.framex = (self.framex+1)%18
        elif self.state==1:
            self.framex = (self.framex+1)%12
            if self.framex==0:
                self.framey = (self.framey-1)%11
                if self.framey==8:
                    self.framey=10
                    self.framex=1
        if click:
            self.state=1
        else:
            self.state=0
        if x>=self.x:
            self.dire=0
        else:
            self.dire=1;
        #self.x+=5
    def draw(self):
        size = 112
        #좌측
        if self.state==0:
            if self.dire == 0:
                self.idle.clip_composite_draw(self.framex*80, 0 ,80,80 ,0,'i',self.x+15,self.y-15,140,140)
            else:
                self.idle.clip_composite_draw(self.framex*80, 0 ,80,80 ,0,'h',self.x-15,self.y-15,140,140)
        elif self.state==1:
            if self.dire == 0:
                self.image.clip_composite_draw(self.framex*size, self.framey*133 ,size,133 ,0,'h',self.x,self.y,200,200)
            else:
                self.image.clip_composite_draw(self.framex*size, self.framey*133 ,size,133 ,0,'i',self.x,self.y,200,200)
        #우측
        #self.image.clip_composite_draw(self.framex*size, self.framey*133 ,size,133 ,0,'h',self.x,self.y,300,300)
        #self.image.clip_draw(self.frame*120 , 0, 120,300 , self.x,self.y)

def handle_events():
    global move
    global key
    global up, down , r ,l
    global x,y
    global click
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            key = 0
        elif event.type == SDL_MOUSEMOTION:
            x,y = event.x , HEIGHT -1 -event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            click = not click;
            print(x,y)
        elif event.type == SDL_KEYDOWN:
            key =True
            if event.key==SDLK_RIGHT:
                r=1;
            if event.key==SDLK_LEFT:
                l=1
            if event.key==SDLK_UP:
                up=1
            if event.key==SDLK_DOWN:
                down =1
            if event.key==SDLK_ESCAPE:
                key=0
        elif event.type == SDL_KEYUP:
            if event.key==SDLK_RIGHT:
                r=0
            if event.key==SDLK_LEFT:
                l=0
            if event.key==SDLK_UP:
                up=0
            if event.key==SDLK_DOWN:
                down =0
            if up==0 and down==0 and r==0 and l==0:
                key=0;

def reset_world():
    global key
    global world

    key=True
    world=[]

    p1 = player()
    world.append(p1)
    
def update_world():
    for o in world:
        o.update()
        
def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas(WIDTH, HEIGHT)

reset_world()

while key:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()


