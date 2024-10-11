from pico2d import *
import math
import random

WIDTH, HEIGHT = 1400 , 1000
click =False;
x,y =0,0
viewX , viewY = 0,0
world =[]

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
    global x,y
    global click
    global viewX,viewY
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            key = 0
        elif event.type == SDL_MOUSEMOTION:
            move=10;
            x,y = event.x , HEIGHT -1 -event.y
            if x<200:
                viewX-=move
            elif x>1200:
                viewX+=move
            if y<200:
                viewY-=move
            elif y>800:
                viewY+=move
            
        elif event.type == SDL_MOUSEBUTTONDOWN:
            print(x,y)
            ground =Ground((x+viewX) - (x+viewX)%50 - WIDTH//2 ,(y+viewY)-(y+viewY) %50 - HEIGHT//2,0,0)
            world.append(ground)
        elif event.type == SDL_KEYDOWN and event.key==SDLK_c:
            for o in world:
                o.printself()
            
def reset_world():
    global key
    global world

    key=True
    #world=[]

    ground =Ground(0,0,0,0)
    world.append(ground)
    ground =Ground(50,0,1,0)
    world.append(ground)

    #p1 = player()
    #world.append(p1)
    
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
    #print (viewX,viewY)
    delay(0.01)

close_canvas()
