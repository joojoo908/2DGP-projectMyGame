Time_PER_ACTION =1
ACTION_PER_TIME =1.0/Time_PER_ACTION

from pico2d import *
import game_world
import frame_work

WIDTH, HEIGHT = 1400 , 1000

class Skill1:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        self.frame =0
        self.viewX, self.viewY = 0, 0
        if Skill1.image == None:
            Skill1.image = load_image('skill/skill_sl.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.clip_composite_draw(int(self.frame)*64, 3*64, 64, 64, 0, 'h',
                WIDTH // 2 - self.viewX + self.x, HEIGHT // 2 - self.viewY + self.y+20,
                500 , 500 )
        draw_rectangle(*self.get_bb())

    def update(self , x,y):
        self.viewX, self.viewY =x,y
        #self.x += self.velocity * 100 * frame_work.frame_time
        self.frame = (self.frame + 10 * ACTION_PER_TIME * frame_work.frame_time)

        if self.frame>10:
            game_world.remove_object(self)

    def get_bb(self):
        x = WIDTH // 2 - self.viewX + self.x
        y = HEIGHT // 2 - self.viewY + self.y + 20
        skillsz=150
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

        pass

    def handle_collision(self, group, other):
        # fill here
        if group == 'boy:ball':
            game_world.remove_object(self)
        if group == 'zombie:ball':
            game_world.remove_object(self)
            #print('hit z')
        pass