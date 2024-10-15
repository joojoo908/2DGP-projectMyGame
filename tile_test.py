from pico2d import *
import math
import random

WIDTH, HEIGHT = 1400 , 1000
click =False;
x,y =0,0
viewX , viewY = 0,0
tilesize = 100
file_map = 'tiles.txt'
tiles = []
world = []
tt ,tn = 0,0

def save_tiles(filename, world):
    with open(filename, 'w') as f:
        for ground in world:
            f.write(f"({ground.x}, {ground.y}, {ground.tiletype}, {ground.tilenum})\n")

# tiles 불러오기 함수
def load_tiles(filename):
    tiles = []
    with open(filename, 'r') as f:
        for line in f:
            tile = eval(line.strip())
            tiles.append(tile)
    return tiles

class Ground:
    global viewX , viewY
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
        self.frame = (self.frame+1)%8
        pass
    def draw(self):
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
    global file_map ,tiles
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            key = 0
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
        #if event.type == SDL_KEYDOWN and event.key==SDLK_t:
            #print('save')
            #save_tiles(file_map, tiles)
        
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

#save_tiles(file_map, tiles)
# 파일에서 tiles 불러오기
tiles = load_tiles(file_map)

def reset_world():
    global key
    global world
    global choiceground
    global tiles
    global background

    

    key=True
    #world=[]
    background = Ground(0,0,0,0)
    
    choiceground = Ground(viewX+600-50,viewY+400-50,tt,tn)

    for tile in tiles:
        ground = Ground(*tile)  # unpacking하여 인자로 전달
        world.append(ground)    
    
def update_world():
    for o in world:
        o.update()
    choiceground.x ,choiceground.y =viewX+600-50 ,viewY+400-50
    choiceground.tiletype , choiceground.tilenum = tt ,tn
        
def render_world():
    clear_canvas()
    #background.drawback()
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
    
save_tiles(file_map, world)
print('save')
close_canvas()

