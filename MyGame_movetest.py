from pico2d import *
import math
import random

#import player

from Ground import Ground
import game_world
from player import Player

WIDTH, HEIGHT = 1400 , 1000
click =False;
mouse_x,mouse_y =0,0
mx,my = 0,0
viewX ,viewY =0,0
#grounds = {}
world =[]
tilesize = 100
#file_map = 'tiles.txt'

key_asdf =[False,False,False,False]

def len(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
def angle(x1,y1,x2,y2):
    return math.atan2((y2-y1),(x2-x1))

# tiles 불러오기 함수

def handle_events():
    global move
    global key
    
    key =True
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            key = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            key = 0
        else:
            p1.handle_event(event)

# 맵 불러오기


def reset_world():
    global key
    global world
    #global grounds
    global tiles
    global background
    global p1

    key=True

    background = Ground(0,0,0,0)

    game_world.ground_add()
    #grounds = load_tiles(file_map)

    p1 = Player()
    world.append(p1)
    
def update_world():
    global viewX, viewY
    game_world.ground_update()
    for o in world:
        o.update(viewX,viewY)
        viewX, viewY = o.viewX, o.viewY
        
def render_world():
    global viewX, viewY
    clear_canvas()
    background.drawback()
    game_world.ground_render(viewX,viewY)
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


