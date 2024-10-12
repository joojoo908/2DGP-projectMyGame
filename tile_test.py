from pico2d import *
import math
import random

WIDTH, HEIGHT = 1400 , 1000
click =False;
x,y =0,0
viewX , viewY = 0,0
tiles =[(0,0,0,0),(50,0,1,0),(100,-50,0,10),(150,-50,0,10),(50,-50,0,10),(0,-50,0,10),(100,0,0,10),(100,50,0,10),(50,50,0,10),(0,50,0,10),(-50,50,0,10)
        ,(-50,0,0,10),(-50,-50,0,10)]
world = []
tt ,tn = 0,0


class Ground:
    global viewX , viewY
    def __init__(self,x,y,tiletype,tilenum):
        self.x,self.y = x,y
        self.frame=0
        self.tiletype=tiletype
        self.tilenum=tilenum
        self.image = load_image('Ground.png')
        self.water = load_image('Water.png')
        self.cliff = load_image('Cliff.png')
    def update(self):
        self.frame = (self.frame+1)%8
        pass
    def draw(self):
         #self.image.draw(self.x,self.y)
        if self.tiletype==0:
            self.image.clip_composite_draw(0*176 + (self.tilenum%11)*16 , 2*80 + (4 - self.tilenum//11) *16, 16 + 0*176 , 16+ 0*80
                                           ,0,'i',WIDTH//2-viewX+ self.x+25 ,HEIGHT//2 -viewY + self.y+25 ,50,50)
        elif self.tiletype==1:
            self.water.clip_composite_draw(self.frame*176 +(self.tilenum%11)*16 , 1*80 +(4 - self.tilenum//11)*16 , 16 + 0*176 , 16+ 0*80 ,
                                           0,'i', WIDTH//2-viewX+ self.x+25 ,HEIGHT//2 -viewY + self.y+25,50,50)
        elif self.tiletype==2:
            pass
    def printself(self):
        print( '(',self.x,',',self.y, ',',self.tiletype, ',', self.tilenum, '),' ,sep='', end='')

def handle_events():
    global move
    global key
    global x,y
    global click
    global viewX,viewY
    global tt,tn
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            key = 0
        move=50;
        if event.type == SDL_KEYDOWN and event.key==SDLK_a:
            viewX-=move
        elif event.type == SDL_KEYDOWN and event.key==SDLK_d:
            viewX+=move
        if event.type == SDL_KEYDOWN and event.key==SDLK_s:
            viewY-=move
        elif event.type == SDL_KEYDOWN and event.key==SDLK_w:
            viewY+=move
        
        if event.type == SDL_KEYDOWN and event.key==SDLK_p:
            for o in world:
                o.printself()
        if event.type == SDL_KEYDOWN and event.key==SDLK_c:
            print('tiletype: ',tt,'tilenum: ', tn)
        if event.type == SDL_KEYDOWN and event.key==SDLK_1:
            tt=(tt+1)%3
        if event.type == SDL_KEYDOWN and event.key==SDLK_2:
            tn=(tn+1)%55
        if event.type == SDL_KEYDOWN and event.key==SDLK_3:
            tn=(tn-1)%55
        if event.type == SDL_KEYDOWN and event.key==SDLK_3:
            tn=(tn+11)%55
        if event.type == SDL_KEYDOWN and event.key==SDLK_4:
            tn=(tn-11)%55
            
        if event.type == SDL_MOUSEMOTION:
            x,y = event.x , HEIGHT -1 -event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            print(x,y)
            ground =Ground((x+viewX) - (x+viewX)%50 - WIDTH//2 ,(y+viewY)-(y+viewY) %50 - HEIGHT//2, tt,tn)
            world.append(ground)

            
def reset_world():
    global key
    global world
    global choiceground

    key=True
    #world=[]
    choiceground = Ground(viewX+650,viewY+450,tt,tn)

    for tile in tiles:
        ground = Ground(*tile)  # unpacking하여 인자로 전달
        world.append(ground)

    #ground =Ground(0,0,0,0)
    #world.append(ground)
    #ground =Ground(50,0,1,0)
    #world.append(ground)

    #p1 = player()
    #world.append(p1)
    
def update_world():
    for o in world:
        o.update()
    choiceground.x ,choiceground.y =viewX+650 ,viewY+450
    choiceground.tiletype , choiceground.tilenum = tt ,tn
        
def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    choiceground.draw()
    update_canvas()


open_canvas(WIDTH, HEIGHT)

reset_world()

while key:
    handle_events()
    update_world()
    render_world()
    #print (viewX,viewY)
    delay(0.1)

close_canvas()
