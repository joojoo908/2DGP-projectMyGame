import frame_work
from pico2d import *

import game_world
import play_mod
from pannel import Pannel

def init():
    global pannel
    pannel =Pannel()
    game_world.add_object(pannel,3)

def finish():
    game_world.remove_object(pannel)

def draw():
    clear_canvas()
    game_world.ground_render(play_mod.viewX, play_mod.viewY)
    game_world.render()
    update_canvas()

def update():
    pass

def handle_events():
    global running
    #global event_boy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            frame_work.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            frame_work.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            frame_work.pop_mode()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_0:
            play_mod.boy.set_item ('None')
            frame_work.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            play_mod.boy.set_item ('Ball')
            frame_work.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            play_mod.boy.set_item ('BigBall')
            frame_work.pop_mode()

def pause():
    pass

def resume():
    pass