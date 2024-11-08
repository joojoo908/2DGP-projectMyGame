from pico2d import *

from Ground import Ground
import game_world
from player import Player

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
            key = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            key = 0
        else:
            p1.handle_event(event)


def init():
    global key
    global world
    # global grounds
    global tiles
    global background
    global p1

    key = True

    background = Ground(0, 0, 0, 0)

    game_world.ground_add()
    # grounds = load_tiles(file_map)

    p1 = Player()
    world.append(p1)

def finish():
    pass

def update():
    global viewX, viewY
    game_world.ground_update()
    for o in world:
        o.update(viewX, viewY)
        viewX, viewY = o.viewX, o.viewY


def render_world():
    global viewX, viewY
    clear_canvas()
    background.drawback()
    game_world.ground_render(viewX, viewY)
    for o in world:
        o.draw()
    update_canvas()