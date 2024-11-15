from pico2d import *

import monster
from Ground import Ground
import game_world
from player import Player
from monster import Monster
import frame_work
import item_mod

WIDTH, HEIGHT = 1400, 1000

mx, my = 0, 0
viewX, viewY = 0, 0

world = []


def handle_events():
    global move
    global key

    key = True
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            frame_work.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            frame_work.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            frame_work.push_mode(item_mod)
        else:
            p1.handle_event(event)

def init():
    global world
    global background
    global p1

    game_world.back_ground_add()
    game_world.ground_add()

    p1 = Player()
    game_world.add_object(p1,1)

    monster =Monster(50,50,1)
    game_world.add_object(monster, 1)

def finish():
    pass

def update():
    global viewX, viewY
    game_world.ground_update()
    game_world.update(viewX, viewY)
    viewX, viewY = p1.viewX, p1.viewY

def draw():
    global viewX, viewY
    clear_canvas()
    game_world.ground_render(viewX, viewY)
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass