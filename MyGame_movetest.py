
from pico2d import *
import math
import random

class player:
    def __init__(self):
        self.x,self.y = 500,500
        self.framex = 0
        self.framey = 11
        self.image = load_image('red_hood.png')

    def update(self):
        self.framex = (self.framex+1)%12
        if self.framex==1:
            self.framey = (self.framey-1)%11
        #self.x+=5
    def draw(self):
        size = 112
        self.image.clip_composite_draw(self.framex*size, self.framey*133 ,size,133 ,0,'i',self.x,self.y,300,300)
        #self.image.clip_draw(self.frame*120 , 0, 120,300 , self.x,self.y)

def handle_events():
    global move
    global key
    global up, down , r ,l
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            key = 0
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


WIDTH, HEIGHT = 1280 , 1024
open_canvas(WIDTH, HEIGHT)

reset_world()

while key:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()


