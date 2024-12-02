from pico2d import *
import math
import random

#from Ground import Ground

WIDTH, HEIGHT = 1400 , 1000
click =False;
x,y =0,0
viewX , viewY = 0,0
tilesize = 100
file_map = 'tiles.txt'
tiles = []
tile_dict = {}
world = []
tt ,tn = 0,0
tile_object =0

def save_tiles(filename, world):
    with open(filename, 'w') as f:
        for (x, y), ground in world.items():
            f.write(f"({x}, {y}, {ground.tiletype}, {ground.tilenum})\n")

def load_tiles(filename):
    tiles = {}
    with open(filename, 'r') as f:
        for line in f:
            tile = eval(line.strip())
            x, y, tiletype, tilenum = tile
            tiles[(x, y)] = Ground(x, y, tiletype, tilenum)
    return tiles

class Ground:
    def __init__(self,x,y,tiletype,tilenum):
        self.x,self.y = x,y
        self.frame=0
        self.framecnt=0
        self.tiletype=tiletype
        self.tilenum=tilenum

        self.image = load_image('Ground.png')
        self.water = load_image('Water.png')
        self.cliff = load_image('Cliff.png')
        self.ground_ani = load_image('Ground_ani.png')
        self.water_ani = load_image('Water_ani.png')
    def update(self):
        if self.tiletype==1 or self.tiletype==4:
            self.framecnt+=1
            if self.framecnt>9:
                self.frame = (self.frame+1)%8
                self.framecnt =0
        
        pass
    def draw(self,viewX,viewY):
         #self.image.draw(self.x,self.y)
        if self.tiletype==0:
            self.image.clip_composite_draw(0*176 + (self.tilenum%11)*16 , 2*80 + (4 - self.tilenum//11) *16, 16 + 0*176 , 16+ 0*80
                                           ,0,'i',WIDTH//2-viewX+ self.x+tilesize//2 ,HEIGHT//2 -viewY + self.y +tilesize//2 ,
                                           tilesize,tilesize)
        elif self.tiletype==1:
            self.water.clip_composite_draw(self.frame*176 +(self.tilenum%11)*16 , 1*80 +(4 - self.tilenum//11)*16 , 16 + 0*176 , 16+ 0*80 ,
                                           0,'i', WIDTH//2-viewX+ self.x +tilesize//2 ,HEIGHT//2 -viewY + self.y+tilesize//2, tilesize,tilesize)
        elif self.tiletype==2:
            self.cliff.clip_composite_draw(0*112 + (self.tilenum%7)*16 , 0*80 +(7 - self.tilenum//7)*16 , 16 + 0*176 , 16+ 0*80 ,
                                           0,'i', WIDTH//2-viewX+ self.x +tilesize//2 ,HEIGHT//2 -viewY + self.y+tilesize//2, tilesize,tilesize)
        elif self.tiletype==3:
            self.image.clip_composite_draw(0*176 + (self.tilenum%11)*16 , 0*80 + (4 - self.tilenum//11) *16, 16 + 0*176 , 16+ 0*80
                                           ,0,'i',WIDTH//2-viewX+ self.x+tilesize//2 ,HEIGHT//2 -viewY + self.y +tilesize//2 ,
                                           tilesize,tilesize)
        elif self.tiletype==4:
            if self.tilenum<5:
                self.water_ani.clip_composite_draw(self.frame*16 , (4 - self.tilenum)*16 , 16 , 16 ,
                                           0,'i', WIDTH//2-viewX+ self.x +tilesize//2 ,HEIGHT//2 -viewY + self.y+tilesize//2, tilesize,tilesize)
            else:
                self.ground_ani.clip_composite_draw( (self.frame%2)*16*5 +(self.tilenum%5)*16 , (6 - (self.tilenum//5) )*16  , 16 , 16 ,
                                           0,'i', WIDTH//2-viewX+ self.x +tilesize//2 ,HEIGHT//2 -viewY + self.y+tilesize//2, tilesize,tilesize)
    def drawback(self):
        self.image.clip_composite_draw(0*176 + (12%11)*16 , 2*80 + (4 - 12//11) *16, 16 + 0*176 , 16+ 0*80
                                           ,0,'i',WIDTH//2, HEIGHT//2,
                                           WIDTH,HEIGHT)

class Object:
    pass

def get_ground(x, y):
    # x, y에 해당하는 Ground 객체 반환
    return world.get((x, y))
    
def handle_events():
    global move
    global loop
    global x,y
    global click
    global viewX,viewY
    global tt,tn
    global tile_object
    global file_map ,tiles
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            loop = 0
        move=tilesize;
        if event.type == SDL_KEYDOWN and event.key==SDLK_a:
            viewX-=move
        elif event.type == SDL_KEYDOWN and event.key==SDLK_d:
            viewX+=move
        if event.type == SDL_KEYDOWN and event.key==SDLK_s:
            viewY-=move
        elif event.type == SDL_KEYDOWN and event.key==SDLK_w:
            viewY+=move
        #타일맵 저
        if event.type == SDL_KEYDOWN and event.key==SDLK_c:
            tile_object = not tile_object
        
        if event.type == SDL_KEYDOWN and event.key==SDLK_p:
            print(", ".join(f"{o.x}, {o.y}, {o.tiletype}, {o.tilenum}" for o in world))
        elif event.type == SDL_KEYDOWN and event.key==SDLK_c:
            print('tiletype: ',tt,'tilenum: ', tn)
            
        if event.type == SDL_KEYDOWN and event.key==SDLK_2:
            tt=(tt+1)
            print('tiletype: ',tt,'tilenum: ', tn)
        elif event.type == SDL_KEYDOWN and event.key==SDLK_1:
            tt=(tt-1)
            print('tiletype: ',tt,'tilenum: ', tn)
        elif event.type == SDL_KEYDOWN and event.key==SDLK_4:
            tn=(tn+1)%55
            print('tiletype: ',tt,'tilenum: ', tn)
        elif event.type == SDL_KEYDOWN and event.key==SDLK_6:
            tn=(tn+5)%55
            print('tiletype: ',tt,'tilenum: ', tn)
        elif event.type == SDL_KEYDOWN and event.key==SDLK_3:
            tn=(tn-1)%55
            print('tiletype: ',tt,'tilenum: ', tn)
        elif event.type == SDL_KEYDOWN and event.key==SDLK_5:
            tn=(tn-5)%55
            print('tiletype: ',tt,'tilenum: ', tn)
            
        if event.type == SDL_MOUSEMOTION:
            x,y = event.x , HEIGHT -1 -event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            click =True
        elif event.type == SDL_MOUSEBUTTONUP:
            click =False
        if click:
            ground = get_ground(
                (x + viewX) - (x + viewX) % tilesize - WIDTH // 2,
                (y + viewY) - (y + viewY) % tilesize - HEIGHT // 2
            )
            if ground:
                if tt==-1:
                    if (ground.x, ground.y) in world:
                        del world[(ground.x, ground.y)]  # 삭제
                        print('erase')
                else:
                    ground.tiletype = tt
                    ground.tilenum = tn
                    print('change')
            else:
                ground = Ground(
                    (x + viewX) - (x + viewX) % tilesize - WIDTH // 2,
                    (y + viewY) - (y + viewY) % tilesize - HEIGHT // 2,
                    tt, tn
                )
                world[(ground.x, ground.y)] = ground  # 딕셔너리에 추가


def reset_world():
    global loop
    global world
    global choiceground
    global tiles
    global background

    loop=True
    #world=[]
    background = Ground(0,0,0,0)
    
    choiceground = Ground(viewX+600-50,viewY+400-50,tt,tn)

    world = load_tiles(file_map)
    
def update_world():
    # for ground in world.values():
    #     ground.update()
    for keyx in range( (viewX -viewX%100)- WIDTH // 2 ,(viewX -viewX%100)+ WIDTH // 2 ,100):
        for keyy in range((viewY - viewY % 100) - HEIGHT // 2, (viewY - viewY % 100) + HEIGHT // 2, 100):
            ground = world.get((keyx,keyy))
            if ground:
                ground.update()
    choiceground.x ,choiceground.y = viewX+600-50 ,viewY+400-50
    choiceground.tiletype , choiceground.tilenum = tt ,tn
        
def render_world():
    clear_canvas()
    #background.drawback()

    for keyx in range( (viewX -viewX%100)- WIDTH // 2 ,(viewX -viewX%100)+ WIDTH // 2 ,100):
        for keyy in range((viewY - viewY % 100) - HEIGHT // 2, (viewY - viewY % 100) + HEIGHT // 2, 100):
            ground = world.get((keyx,keyy))
            if ground:
                ground.draw(viewX, viewY)

    choiceground.draw(viewX,viewY)
    update_canvas()


open_canvas(WIDTH, HEIGHT)

reset_world()

while loop:
    handle_events()
    update_world()
    render_world()
    #print (viewX,viewY)
    delay(0.01)
    
save_tiles(file_map, world)
print('save')
close_canvas()

