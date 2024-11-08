

from Ground import *
file_map = 'tiles.txt'
grounds ={}
WIDTH, HEIGHT = 1400 , 1000

def ground_add():
    global grounds
    grounds = load_tiles(file_map)

def ground_update():
    for ground in grounds.values():
        ground.update()

def ground_render(viewX,viewY):
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

