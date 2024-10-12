from pico2d import *
import math
import random

WIDTH, HEIGHT = 1400 , 1000
click =False;
x,y =0,0
viewX , viewY = 0,0
tilesize = 50
tiles =[(0,0,0,0),(50,0,1,0),(100,-50,1,12),(150,-50,1,12),(50,-50,0,10),(0,-50,0,10),(100,0,1,1),(100,50,0,10),(50,50,0,10),(0,50,0,10),(-50,50,0,10),
        (-50,0,0,10),(-50,-50,0,10),(150,0,1,1),(200,0,1,1),(250,0,1,2),(250,-50,1,13),(250,-100,1,13),(200,-50,1,12),(100,-100,1,12),(150,-100,1,12),
        (200,-100,1,12),(100,-150,1,12),(150,-150,1,12),(200,-150,1,12)]
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

def get_ground(x, y):
    # 클릭한 위치에 이미 Ground가 있는지 확인하고 해당 Ground를 반환
    for ground in world:
        if (ground.x == (x+viewX)-(x+viewX)%tilesize - WIDTH//2 and
                ground.y == (y+viewY)-(y+viewY)%tilesize - HEIGHT//2):
            return ground
    
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
            print(", ".join(f"({o.x}, {o.y}, {o.tiletype}, {o.tilenum})" for o in world))
        if event.type == SDL_KEYDOWN and event.key==SDLK_c:
            print('tiletype: ',tt,'tilenum: ', tn)
        if event.type == SDL_KEYDOWN and event.key==SDLK_1:
            tt=(tt+1)%3
        if event.type == SDL_KEYDOWN and event.key==SDLK_2:
            tn=(tn+1)%55
        if event.type == SDL_KEYDOWN and event.key==SDLK_3:
            tn=(tn+11)%55
        if event.type == SDL_KEYDOWN and event.key==SDLK_5:
            tn=(tn-1)%55
        if event.type == SDL_KEYDOWN and event.key==SDLK_6:
            tn=(tn-11)%55
            
        if event.type == SDL_MOUSEMOTION:
            x,y = event.x , HEIGHT -1 -event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            #print(x,y)
            ground = get_ground(x, y)
            if ground:
                # 이미 존재하는 타일이 있을 경우, 타일의 타입과 번호 변경
                ground.tiletype = tt
                ground.tilenum = tn
            else:
                # 타일이 없을 경우, 새로운 타일 생성
                ground = Ground((x+viewX) - (x+viewX)%tilesize - WIDTH//2,
                                (y+viewY)-(y+viewY) %tilesize - HEIGHT//2, tt, tn)
                world.append(ground)
            
            #ground =Ground((x+viewX) - (x+viewX)%50 - WIDTH//2 ,(y+viewY)-(y+viewY) %tilesize - HEIGHT//2, tt,tn)
            #world.append(ground)

            
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
