from pico2d import *

from Ground import Ground
import game_world

import random
from player_state import State
from player import Player
from monster import Monster
import frame_work
import item_mod
import end_mod

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
    global boss

    game_world.back_ground_add()
    game_world.ground_add()

    p1 = Player()
    game_world.add_object(p1,1)
    game_world.add_collision_pair('p1:mop', p1, None)
    game_world.add_collision_pair('p1:mop_atk', p1, None)

    state = State(p1.hp,p1.mp)
    game_world.add_object(state, 3)

    #보스소환
    boss = Monster(-700, -4200, 0)
    game_world.add_object(boss, 1)
    game_world.add_collision_pair('p1:mop', None, boss)
    game_world.add_collision_pair('mop:p1_atk', boss, None)

    #몬스터 소환
    monster =Monster(600,0,1)
    game_world.add_object(monster, 1)
    game_world.add_collision_pair('p1:mop', None, monster)
    game_world.add_collision_pair('mop:p1_atk', monster, None)

    #기본몹들 소환
    monsters = [Monster( -1600 +random.randint(-300, 300),
                        -2500+ random.randint(-300, 300),
                         random.randint(1, 2))for _ in range(5)]
    mops = [Monster(-1300 + random.randint(-500, 500),
             -1300 + random.randint(-500, 500),
             random.randint(1, 2)) for _ in range(7)]
    monsters.extend(mops)
    mops = [Monster(400 + random.randint(-500, 500),
                    -1300 + random.randint(-500, 500),
                    random.randint(1, 2)) for _ in range(7)]
    monsters.extend(mops)
    mops = [Monster(2000 + random.randint(-1000, 1000),
                    -1800 + random.randint(-200, 200),
                    random.randint(1, 2)) for _ in range(5)]
    monsters.extend(mops)
    mops = [Monster(3400 + random.randint(-300, 300),
                    -2300 + random.randint(-500, 500),
                    random.randint(1, 2)) for _ in range(7)]
    monsters.extend(mops)
    mops = [Monster(1200 + random.randint(-1600, 1800),
                    -2700 + random.randint(-200, 200),
                    random.randint(1, 2)) for _ in range(7)]
    monsters.extend(mops)
    for mop in monsters:
        game_world.add_object(mop, 1)
        game_world.add_collision_pair('p1:mop', None, mop)
        game_world.add_collision_pair('mop:p1_atk', mop, None)

def finish():
    pass

def update():
    global viewX, viewY
    game_world.ground_update()
    game_world.update(viewX, viewY)
    viewX, viewY = p1.viewX, p1.viewY

    game_world.handle_collisions()
    if p1.hp<0:
        frame_work.push_mode(end_mod)
    elif boss.hp<0:
        frame_work.push_mode(end_mod)

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