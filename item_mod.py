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
        elif event.type == SDL_MOUSEBUTTONDOWN:
            print(event.x,event.y)
            if 400-50<event.x<500-50 and 300-50<event.y<400-50:
                play_mod.p1.skills[0]=1
            elif 700 - 50 < event.x < 800 - 50 and 300 - 50 < event.y < 400 - 50:
                play_mod.p1.skills[1] = 1
            elif 1000 - 50 < event.x < 1100 - 50 and 300 - 50 < event.y < 400 - 50:
                play_mod.p1.skills[2] = 1
            elif 400 - 50 < event.x < 500 - 50 and 600-50<event.y<700-50:
                play_mod.p1.skills[3] = 1
            elif 700 - 50 < event.x < 800 - 50 and 600-50<event.y<700-50:
                play_mod.p1.skills[4] = 1
            elif 1000-50<event.x<1100-50 and 600-50<event.y<700-50:
                play_mod.p1.skills[5]=1


def pause():
    pass

def resume():
    pass