

from Ground import *
file_map = 'tiles.txt'
grounds ={}
world = [[] for _ in range(4)]
collision_pairs ={}
WIDTH, HEIGHT = 1400 , 1000


def back_ground_add():
    global background
    background = Ground(0, 0, 0, 0)

def ground_add():
    global grounds
    grounds = load_tiles(file_map)

def ground_update():
    for ground in grounds.values():
        ground.update()

def ground_render(viewX,viewY):
    background.drawback()
    for keyx in range((int)(viewX - viewX % 100) - WIDTH // 2, (int)(viewX - viewX % 100) + WIDTH // 2+100, 100):
        for keyy in range((int)(viewY - viewY % 100) - HEIGHT // 2, (int)(viewY - viewY % 100) + HEIGHT // 2+100, 100):
            ground = grounds.get((keyx, keyy))
            if ground:
                ground.draw(viewX, viewY)
    pass

def ck_ground(x, y):
    keyx, keyy = x - x % 100, y - y % 100
    ground = grounds.get((keyx, keyy))
    if ground:
        if ground.tiletype == 1 or ground.tiletype == 2:
            return 1
        elif ground.tiletype==4 and ground.tilenum<5:
            return 1

    return 0

def add_collision_pair(group,a,b):
    if group not in collision_pairs:
        print( f'new group {group}')
        collision_pairs[group] = [[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def update(viewX, viewY):
    for layer in world:
        for o in layer:
            o.update(viewX, viewY)

def render():
    for layer in world:
        for o in layer:
            o.draw()

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a,b):
                    a.handle_collision(group,b)
                    b.handle_collision(group,a)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()


# fill here
def collide(a, b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_bb()

    if left_a >right_b: return False
    if left_b >right_a: return False
    if top_a <bottom_b: return False
    if top_b <bottom_a: return False

    return True

    pass





