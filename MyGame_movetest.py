from pico2d import *
import math
import random

from Ground import Ground

WIDTH, HEIGHT = 1400 , 1000
click =False;
mouse_x,mouse_y =0,0
mx,my = 0,0
viewX ,viewY =0,0
grounds = []
world =[]
tilesize = 100
file_map = 'tiles.txt'

key_asdf =[False,False,False,False]

def len(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
def angle(x1,y1,x2,y2):
    return math.atan2((y2-y1),(x2-x1))

# tiles 불러오기 함수
def load_tiles(filename):
    tiles = []
    with open(filename, 'r') as f:
        for line in f:
            tile = eval(line.strip())
            tiles.append(tile)
    return tiles

class player:
    #global viewX ,viewY
    global mouse_x,mouse_y
    #global mx,my
    global key_asdf
    image =None
    
    def __init__(self):
        self.x,self.y = 0,0
        self.framex = 0
        self.framey = 10
        self.state = 0  # 0:idle 1: move  2: dash 3:attack1
        self.dire =0 # 방향
        self.framecnt = 0
        #if self.image==None:
        self.image = load_image('red_hood.png')
        self.idle = load_image('red_hood_idle.png')

    def Dash(self):
        self.state=2
        self.framecnt=0
        self.framex=0
    def move_p(self,mx,my,speed):
        if math.cos(angle(self.x,self.y,mx,my))<0 :
            if self.x <= viewX -400:
                viewX += speed*math.cos(angle(self.x,self.y,mx,my))
            elif math.cos(angle(self.x,self.y,mx,my))>0 :
                if self.x >= viewX +400:
                    viewX += speed*math.cos(angle(self.x,self.y,mx,my))
            if math.sin(angle(self.x,self.y,mx,my))<0 :
                if self.y <= viewY -200:
                    viewY += speed*math.sin(angle(self.x,self.y,mx,my))
            elif math.sin(angle(self.x,self.y,mx,my))>0 :
                if self.y >= viewY +300:
                    viewY += speed*math.sin(angle(self.x,self.y,mx,my))
            # 플레이어 이동
            self.x += speed*math.cos(angle(self.x,self.y,mx,my))
            self.y += speed*math.sin(angle(self.x,self.y,mx,my))

    def update(self):
        global viewX ,viewY
        global mx,my
        global mouse_x,mouse_y
        #------애니메이션---
        self.framecnt+=1
        if key_asdf[2]:
            self.state=2
            self.framex=0
            key_asdf[2] = False
        if key_asdf[3]:
            self.state=3
            
        if self.state==0: #idle
            if self.framecnt>4:
                self.framex = (self.framex+1)%18
                self.framecnt =0;
        elif self.state==1: #move
            if self.framecnt>4:
                self.framex = (self.framex+1)%12
                if self.framex==0:
                    self.framey = (self.framey-1)%11
                    if self.framey==8:
                        self.framey=10
                        self.framex=1
                self.framecnt=0
        elif self.state==2: #dash
            if self.framecnt>5:
                self.framex = (self.framex+1)
                if self.framex>4:
                    self.state=1
                    key_asdf[2] =False
                self.framecnt=0
        
        #-------이동-----
        speed = 5
        
        if len(self.x,self.y,mx,my) > speed:
            if self.state==2:
                speed =10
            else:
                self.state=1
            self.dire = mx <= self.x # 플에이어가 바라보는 방향 설정
            # 플레이어가 일정 범위 밖일때 맵 전체 이동
            if math.cos(angle(self.x,self.y,mx,my))<0 :
                if self.x <= viewX -400:
                    viewX += speed*math.cos(angle(self.x,self.y,mx,my))
            elif math.cos(angle(self.x,self.y,mx,my))>0 :
                if self.x >= viewX +400:
                    viewX += speed*math.cos(angle(self.x,self.y,mx,my))
            if math.sin(angle(self.x,self.y,mx,my))<0 :
                if self.y <= viewY -200:
                    viewY += speed*math.sin(angle(self.x,self.y,mx,my))
            elif math.sin(angle(self.x,self.y,mx,my))>0 :
                if self.y >= viewY +300:
                    viewY += speed*math.sin(angle(self.x,self.y,mx,my))
            # 플레이어 이동
            self.x += speed*math.cos(angle(self.x,self.y,mx,my))
            self.y += speed*math.sin(angle(self.x,self.y,mx,my))
            
        else:#마우스 클릭x
            if self.state==2:
                speed =10
                self.dire = mouse_x <= self.x 
                if math.cos(angle(self.x,self.y,mouse_x,mouse_y))<0 :
                    if self.x <= viewX -400:
                        viewX += speed*math.cos(angle(self.x,self.y,mouse_x,mouse_y))
                elif math.cos(angle(self.x,self.y,mouse_x,mouse_y))>0 :
                    if self.x >= viewX +400:
                        viewX += speed*math.cos(angle(self.x,self.y,mouse_x,mouse_y))
                if math.sin(angle(self.x,self.y,mouse_x,mouse_y))<0 :
                    if self.y <= viewY -200:
                        viewY += speed*math.sin(angle(self.x,self.y,mouse_x,mouse_y))
                elif math.sin(angle(self.x,self.y,mouse_x,mouse_y))>0 :
                    if self.y >= viewY +300:
                        viewY += speed*math.sin(angle(self.x,self.y,mouse_x,mouse_y))
                self.x += speed*math.cos(angle(self.x,self.y,mouse_x,mouse_y))
                self.y += speed*math.sin(angle(self.x,self.y,mouse_x,mouse_y))
                mx,my=self.x,self.y
            else:
                self.x =mx
                self.y =my
                self.state=0
        
    def draw(self):
        size = 112
        playersize=1.8
        #self.image.opacify(100) #투명화
        if self.state==0:
            if self.dire == 0:
                self.idle.clip_composite_draw(self.framex*80, 0 ,80,80
                                              ,0,'i',WIDTH//2-viewX+ self.x+15, HEIGHT//2 -viewY+ self.y-15 ,140*playersize,140*playersize)
            else:
                self.idle.clip_composite_draw(self.framex*80, 0 ,80,80
                                              ,0,'h',WIDTH//2-viewX+ self.x-15,HEIGHT//2 -viewY+ self.y-15 ,140*playersize,140*playersize)
        elif self.state==1:
            if self.dire == 0:
                self.image.clip_composite_draw(self.framex*size, self.framey*133 ,size,133
                                               ,0,'h',WIDTH//2-viewX+self.x, HEIGHT//2 -viewY + self.y,200*playersize,200*playersize)
            else:
                self.image.clip_composite_draw(self.framex*size, self.framey*133 ,size,133
                                               ,0,'i',WIDTH//2-viewX+self.x, HEIGHT//2 -viewY + self.y,200*playersize,200*playersize)
        elif self.state==2:
            if self.dire == 0:
                self.image.clip_composite_draw((self.framex+4) *size, 6 *133 ,size,133
                                               ,0,'h',WIDTH//2-viewX+self.x, HEIGHT//2 -viewY + self.y,200*playersize,200*playersize)
            else:
                self.image.clip_composite_draw((self.framex+4) *size, 6 *133 ,size,133
                                               ,0,'i',WIDTH//2-viewX+self.x, HEIGHT//2 -viewY + self.y,200*playersize,200*playersize)

def handle_events():
    global move
    global key
    global key_asdf
    global mouse_x,mouse_y
    global click
    global mx,my
    
    key =True
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            key = 0
        elif event.type == SDL_MOUSEMOTION:
            mouse_x,mouse_y = event.x -WIDTH//2 + viewX , HEIGHT -event.y - HEIGHT//2 + viewY+50
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                mx ,my = mouse_x, mouse_y
                #print(viewX,viewY)
        elif event.type == SDL_KEYDOWN:
            if event.key==SDLK_d:
                print('dash')
                key_asdf[2]=True
            elif event.key==SDLK_f:
                print('attack')
                key_asdf[3]=True
        elif event.type == SDL_KEYUP:
            pass

# 맵 불러오기
tiles = load_tiles(file_map)
def reset_world():
    global key
    global world
    global grounds
    global tiles
    global background

    key=True

    background = Ground(0,0,0,0)

    for tile in tiles:
        ground = Ground(*tile)  # unpacking하여 인자로 전달
        grounds.append(ground)

    p1 = player()
    world.append(p1)
    
def update_world():
    for g in grounds:
        g.update()
    for o in world:
        o.update()
        
def render_world():
    clear_canvas()
    background.drawback()
    for g in grounds:
        #카메라 내부만 랜더링 
        if g.x>viewX-WIDTH-100//2 and g.x<viewX+WIDTH//2 and g.y>viewY-HEIGHT//2-100 and g.y<viewY+HEIGHT//2:
            g.draw(viewX ,viewY)
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
    delay(0.01)

close_canvas()


