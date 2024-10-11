
from pico2d import *
import math
import random

WIDTH, HEIGHT = 1400 , 1000
click =False;
x,y =0,0
mx,my = 0,0
viewX ,viewY =0,0

def len(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
def angle(x1,y1,x2,y2):
    return math.atan2((y2-y1),(x2-x1))

class player:
    global viewX ,viewY
    global click
    global x,y
    global mx,my
    def __init__(self):
        self.x,self.y = 0,0
        self.framex = 0
        self.framey = 10
        self.state = 0  # 0:idle 1: move
        self.dire =0
        self.image = load_image('red_hood.png')
        self.idle = load_image('red_hood_idle.png')

    def update(self):
        global viewX ,viewY
        #------애니메이션---
        if self.state==0: #idle
            self.framex = (self.framex+1)%18
        elif self.state==1: #move
            self.framex = (self.framex+1)%12
            if self.framex==0:
                self.framey = (self.framey-1)%11
                if self.framey==8:
                    self.framey=10
                    self.framex=1
        #----이동---
        speed = 10
        if len(self.x,self.y,mx,my) > speed:
            self.state=1
            self.dire = mx <= self.x
            if math.cos(angle(self.x,self.y,mx,my))<0 :
                if self.x <= viewX -400:
                    viewX += speed*math.cos(angle(self.x,self.y,mx,my))
            elif math.cos(angle(self.x,self.y,mx,my))>0 :
                if self.x >= viewX +400:
                    viewX += speed*math.cos(angle(self.x,self.y,mx,my))
                    
            if math.sin(angle(self.x,self.y,mx,my))<0 :
                if self.y <= viewY -300:
                    viewY += speed*math.sin(angle(self.x,self.y,mx,my))
            elif math.sin(angle(self.x,self.y,mx,my))>0 :
                if self.y >= viewY +300:
                    viewY += speed*math.sin(angle(self.x,self.y,mx,my))
            self.x += speed*math.cos(angle(self.x,self.y,mx,my))
            self.y += speed*math.sin(angle(self.x,self.y,mx,my))
            
        else:
            self.x =mx
            self.y =my
            self.state=0
            #print(viewX,viewY)
        
    def draw(self):
        size = 112
        #좌측
        if self.state==0:
            if self.dire == 0:
                self.idle.clip_composite_draw(self.framex*80, 0 ,80,80
                                              ,0,'i',WIDTH//2-viewX+ self.x+15, HEIGHT//2 -viewY+ self.y-15 ,140,140)
            else:
                self.idle.clip_composite_draw(self.framex*80, 0 ,80,80
                                              ,0,'h',WIDTH//2-viewX+ self.x-15,HEIGHT//2 -viewY+ self.y-15 ,140,140)
        elif self.state==1:
            if self.dire == 0:
                self.image.clip_composite_draw(self.framex*size, self.framey*133 ,size,133
                                               ,0,'h',WIDTH//2-viewX+self.x, HEIGHT//2 -viewY + self.y,200,200)
            else:
                self.image.clip_composite_draw(self.framex*size, self.framey*133 ,size,133
                                               ,0,'i',WIDTH//2-viewX+self.x, HEIGHT//2 -viewY + self.y,200,200)

                
class Ground:
    global viewX , viewY
    def __init__(self,x,y,tiletype,tilenum):
        self.x,self.y = x,y
        self.frame=0
        self.tiletype=tiletype
        self.tilenum=tilenum
        self.image = load_image('Ground.png')
        self.water = load_image('Water.png')
    def update(self):
        self.frame = (self.frame+1)%8
        pass
    def draw(self):
         #self.image.draw(self.x,self.y)
        if self.tiletype==0:
            self.image.clip_composite_draw(0*176 +1*16 , 2*80 +3*16, 16 + 0*176 , 16+ 0*80
                                           ,0,'i',WIDTH//2-viewX+ self.x+25 ,HEIGHT//2 -viewY + self.y+25 ,50,50)
        elif self.tiletype==1:
            self.water.clip_composite_draw(self.frame*176 +1*16 , 1*80 +3*16, 16 + 0*176 , 16+ 0*80 ,
                                           0,'i', WIDTH//2-viewX+ self.x+25 ,HEIGHT//2 -viewY + self.y+25,50,50)
    def printself(self):
        print( '(',self.x,',',self.y, ',',self.tiletype, ',', self.tilenum, '),')

def handle_events():
    global move
    global key
    global up, down , r ,l
    global x,y
    global click
    global mx,my
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            key = 0
        elif event.type == SDL_MOUSEMOTION:
            x,y = event.x , HEIGHT -1 -event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                mx ,my = -WIDTH//2 + viewX + x, -HEIGHT//2 + viewY +y
                #print(viewX,viewY)
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

def reset_world():
    global key
    global world

    key=True
    world=[]

    ground =Ground(0,0,0,0)
    world.append(ground)

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
    #print(viewX,viewY)
    delay(0.05)

close_canvas()


