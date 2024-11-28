from pico2d import *

from Ground import Ground
import game_world

from player_state import State
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

    state = State(p1.hp,p1.mp)
    game_world.add_object(state, 3)

    monster =Monster(600,0,2)
    game_world.add_object(monster, 1)

    game_world.add_collision_pair('p1:mop', p1, None)
    game_world.add_collision_pair('p1:mop', None, monster)

    game_world.add_collision_pair('p1:mop_atk', p1, None)
    game_world.add_collision_pair('mop:p1_atk', monster, None)

def finish():
    pass

def update():
    global viewX, viewY
    game_world.ground_update()
    game_world.update(viewX, viewY)
    viewX, viewY = p1.viewX, p1.viewY

    game_world.handle_collisions()

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