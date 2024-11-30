PIXEL_PER_METER =(10.0/0.3)
RUN_SPEED_KMPH = 50.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
RUN_SPEED_PPS =(RUN_SPEED_MPS*PIXEL_PER_METER)

Time_PER_ACTION =1
ACTION_PER_TIME =1.0/Time_PER_ACTION
FRAME_PER_ACTION=18
FRAME_PER_ACTION_run=24
FRAME_PER_ACTION_dash=4

import game_world
from state_machine import *
import pygame
import frame_work
from skill import *

WIDTH, HEIGHT = 1400 , 1000

def len(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
def angle(x1,y1,x2,y2):
    return math.atan2((y2-y1),(x2-x1))

class Player:

    def __init__(self):
        self.hp=100
        self.mp=100
        self.x, self.y = 0, 0
        self.viewX, self.viewY = 0, 0
        self.mx,self.my = 0,0
        self.framex = 0
        self.dire = 1  # 방향
        self.skillnum = 0
        self.skillpoint=8
        self.skills=[1,1,1,1,1,1]
        self.invincible=0

        self.image = load_image('red_hood.png')
        self.idle = load_image('red_hood_idle.png')
        self.mouse = load_image('Mouse.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {mouse_click: Run , dash_down:Dash ,damage:Damaged, die:Death ,attack:Attack,dmg:Damaged,
                   skill:Skill},
            Run: {run_over: Idle ,mouse_click: Run, dash_down:Dash ,damage:Damaged,
                  attack:Attack, dmg:Damaged,skill:Skill  },
            Dash: {dash_over:Idle,damage:Damaged,dash_down:Dash ,mouse_click: Run,attack:Attack,dmg:Damaged},
            Damaged: { mouse_click: Run, dash_down:Dash,damage_over:Idle,
                      death:Death },
            Death: {},
            Attack:{idle:Idle ,dmg:Damaged},
            Skill:{idle:Idle,dmg:Damaged}
              })

    def handle_event(self ,event):
        self.state_machine.add_event(('INPUT', event))
        pass
    def update(self,vx,vy):
        if self.mp<100:
            self.mp+= (30 * ACTION_PER_TIME * frame_work.frame_time)
        self.viewX,self.viewY=vx,vy
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.dire:
            x = WIDTH // 2 - self.viewX + self.x +20
        else:
            x = WIDTH // 2 - self.viewX + self.x - 20
        y = HEIGHT // 2 - self.viewY + self.y
        skillsz = 50
        return x - skillsz, y - skillsz, x + skillsz, y + skillsz

    def return_xy(self):
        return self.x,self.y

    def skill(self,num):
        if num==1:
            skill =Skill1(self.x, self.y,self.viewX,self.viewY)
        elif num == 2:
            skill = Skill2(self.x, self.y, self.viewX, self.viewY,self.dire)
        elif num == 3:
            skill = Skill3(self.x, self.y, self.viewX, self.viewY)
        elif num==4:
            skill =Skill4(self.x, self.y,self.viewX,self.viewY)
        elif num==5:
            skill =Skill5(self.x, self.y,self.viewX,self.viewY)
        elif num==6:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mx ,my =mouse_x - WIDTH // 2 + self.viewX, HEIGHT - mouse_y - HEIGHT // 2 + self.viewY
            ang = angle(self.x, self.y, mx, my)
            skill =Skill6(self.x, self.y,self.viewX,self.viewY,ang)
            skill2 =Skill6(self.x, self.y,self.viewX,self.viewY,ang+3.14/180*15)
            skill3 =Skill6(self.x, self.y,self.viewX,self.viewY,ang-3.14/180*15)
            game_world.add_object(skill2)
            game_world.add_object(skill3)
            game_world.add_collision_pair('mop:p1_atk', None, skill2)
            game_world.add_collision_pair('mop:p1_atk', None, skill3)

        game_world.add_object(skill)
        if num != 3 and num!=4:
            game_world.add_collision_pair('mop:p1_atk', None, skill)

    def handle_collision(self, group, other):
        if group == 'p1:mop':
            pass
        if group == 'p1:mop_atk':
            if self.invincible:
                pass
            else:
                self.state_machine.add_event(('DMG', 0))
                self.hp -= other.damage
            pass

class Idle:
    @staticmethod
    def enter(p1, e):
        p1.framex=0
        p1.framecnt=0
        pass

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        print(p1.x,p1.y)
        #if p1.framecnt > p1.maxcnt-5:
        p1.framex = (p1.framex + FRAME_PER_ACTION * ACTION_PER_TIME * frame_work.frame_time) % FRAME_PER_ACTION

    @staticmethod
    def draw(p1):
        playersize = 1.8
        if p1.dire == 0:
            p1.idle.clip_composite_draw(int(p1.framex) * 80, 0, 80, 80
                                        , 0, 'i', WIDTH // 2 - p1.viewX + p1.x + 15,
                                        HEIGHT // 2 - p1.viewY + p1.y - 15+30, 140 * playersize, 140 * playersize)
        else:
            p1.idle.clip_composite_draw(int(p1.framex) * 80, 0, 80, 80
                                        , 0, 'h', WIDTH // 2 - p1.viewX + p1.x - 15,
                                        HEIGHT // 2 - p1.viewY + p1.y - 15+30, 140 * playersize, 140 * playersize)

class Run:
    @staticmethod
    def enter(p1,e):
        p1.m_cnt=0;
        p1.framecnt = 0
        p1.mx, p1.my = e[1].x-WIDTH//2 + p1.viewX,  HEIGHT -e[1].y- HEIGHT//2 + p1.viewY
        pass

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.framex = (p1.framex + FRAME_PER_ACTION_run * ACTION_PER_TIME * frame_work.frame_time) %24

        p1.m_cnt+=1

        mx, my = p1.mx,p1.my
        if len(p1.x, p1.y, mx, my) > RUN_SPEED_PPS * frame_work.frame_time:
            p1.dire = mx <= p1.x  # 플에이어가 바라보는 방향 설정
            # 플레이어가 일정 범위 밖일때 맵 전체 이동
            if math.cos(angle(p1.x, p1.y, mx, my)) < 0:
                if p1.x <= p1.viewX - 400:
                    p1.viewX += math.cos(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time
            elif math.cos(angle(p1.x, p1.y, mx, my)) > 0:
                if p1.x >= p1.viewX + 400:
                    p1.viewX += math.cos(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time

            if math.sin(angle(p1.x, p1.y, mx, my)) < 0:
                if p1.y <= p1.viewY - 200:
                    p1.viewY += math.sin(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time
            elif math.sin(angle(p1.x, p1.y, mx, my)) > 0:
                if p1.y >= p1.viewY + 300:
                    p1.viewY += math.sin(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time
            # 플레이어 이동
            movingx =math.cos(angle(p1.x, p1.y, mx, my)) * RUN_SPEED_PPS * frame_work.frame_time
            movingy =math.sin(angle(p1.x, p1.y, mx, my)) * RUN_SPEED_PPS * frame_work.frame_time

            if not game_world.ck_ground(p1.x+movingx, p1.y+movingy):
                p1.x += movingx
                p1.y += movingy

        else:
            p1.x = mx
            p1.y = my
            p1.state_machine.add_event(('RUN_OVER', 0))

    @staticmethod
    def draw(p1):
        p1.mouse.clip_draw( (p1.m_cnt//30%4)*64 ,64*2,64,64,WIDTH // 2 - p1.viewX + p1.mx, HEIGHT // 2 - p1.viewY + p1.my)

        #print(p1.x,p1.y)
        size = 112
        playersize = 1.8
        if p1.dire == 0:
            p1.image.clip_composite_draw(int(p1.framex)%12 * size, (10-int(p1.framex)//12) * 133, size, 133
                                           , 0, 'h', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y+30,
                                           200 * playersize, 200 * playersize)
        else:
            p1.image.clip_composite_draw(int(p1.framex)%12 * size, (10-int(p1.framex)//12)  * 133, size, 133
                                           , 0, 'i', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y+30,
                                           200 * playersize, 200 * playersize)
        #pass

class Dash:
    @staticmethod
    def enter(p1, e):
        p1.framecnt = 0
        p1.framex = 0
        mouse_x,mouse_y = pygame.mouse.get_pos()
        p1.mx, p1.my = mouse_x - WIDTH // 2 + p1.viewX, HEIGHT - mouse_y - HEIGHT // 2 + p1.viewY

        #p1.mx, p1.my = e[1].x-WIDTH//2 + p1.viewX,  HEIGHT -e[1].y- HEIGHT//2 + p1.viewY+50

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.framex = (p1.framex + FRAME_PER_ACTION_dash*2 * ACTION_PER_TIME * frame_work.frame_time)
        if p1.framex > 4:
            p1.state_machine.add_event(('DASH_OVER', 0))
            p1.framex=0

        speed = 2
        mx, my = p1.mx, p1.my
        if len(p1.x, p1.y, mx, my) > RUN_SPEED_PPS * frame_work.frame_time*2:
            p1.dire = mx <= p1.x  # 플에이어가 바라보는 방향 설정
            # 플레이어가 일정 범위 밖일때 맵 전체 이동
            if math.cos(angle(p1.x, p1.y, mx, my)) < 0:
                if p1.x <= p1.viewX - 400:
                    p1.viewX += speed * math.cos(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time
            elif math.cos(angle(p1.x, p1.y, mx, my)) > 0:
                if p1.x >= p1.viewX + 400:
                    p1.viewX += speed * math.cos(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time
            if math.sin(angle(p1.x, p1.y, mx, my)) < 0:
                if p1.y <= p1.viewY - 200:
                    p1.viewY += speed * math.sin(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time
            elif math.sin(angle(p1.x, p1.y, mx, my)) > 0:
                if p1.y >= p1.viewY + 200:
                    p1.viewY += speed * math.sin(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time
            # 플레이어 이동
            movingx = math.cos(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time*2
            movingy = math.sin(angle(p1.x, p1.y, mx, my))* RUN_SPEED_PPS * frame_work.frame_time*2

            if not game_world.ck_ground(p1.x + movingx, p1.y + movingy):
                p1.x += movingx
                p1.y += movingy
                p1.mx += movingx
                p1.my += movingy
        else:
            p1.x = mx
            p1.y = my

    @staticmethod
    def draw(p1):
        size = 112
        playersize = 1.8
        if p1.dire == 0:
            p1.image.clip_composite_draw((int(p1.framex) + 4) * size, 6 * 133, size, 133
                                           , 0, 'h', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y+30,
                                           200 * playersize, 200 * playersize)
        else:
            p1.image.clip_composite_draw((int(p1.framex) + 4) * size, 6 * 133, size, 133
                                           , 0, 'i', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y+30,
                                           200 * playersize, 200 * playersize)

class Damaged:
    @staticmethod
    def enter(p1, e):
        p1.framecnt = 0
        p1.framex =0
        print('hp:',p1.hp)
        pass

    @staticmethod
    def exit(p1, e):
        pass

    @staticmethod
    def do(p1):
        p1.framex = (p1.framex + 6 * ACTION_PER_TIME*2 * frame_work.frame_time)
        if p1.framex>6:
            if p1.hp <= 0:
                p1.state_machine.add_event(('DEATH', 0))
            p1.state_machine.add_event(('DAMAGE_OVER', 0))

        pass

    @staticmethod
    def draw(p1):
        size = 112
        playersize = 1.8
        if p1.dire == 0:
            p1.image.clip_composite_draw(int(p1.framex ) * size, 0, size, 133
                                         , 0, 'h', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y+30,
                                         200 * playersize, 200 * playersize)
        else:
            p1.image.clip_composite_draw(int(p1.framex) * size, 0, size, 133
                                         , 0, 'i', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y+30,
                                         200 * playersize, 200 * playersize)

class Death:
    @staticmethod
    def enter(p1, e):
        p1.framecnt = 0

        pass

    @staticmethod
    def exit(p1, e):

        pass

    @staticmethod
    def do(p1):
        if p1.framex< 250:
            p1.framex = (p1.framex + 100 * ACTION_PER_TIME * frame_work.frame_time)
        else:
            print('end')
            pass

    @staticmethod
    def draw(p1):
        size = 112
        playersize = 1.8
        p1.image.opacify( int(p1.framex))
        if p1.dire == 0:
            p1.image.clip_composite_draw(6 * size, 0, size, 133
                                         , 0, 'h', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y+30,
                                         200 * playersize, 200 * playersize)
        else:
            p1.image.clip_composite_draw(6 * size, 0, size, 133
                                         , 0, 'i', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y+30,
                                         200 * playersize, 200 * playersize)
        pass

class Attack:
    @staticmethod
    def enter(p1, e):
        p1.framecnt = 0
        p1.framex = 8
        p1.framey = 0


    @staticmethod
    def exit(p1, e):
        p1.framex = 0
        p1.framecnt =0
        pass

    @staticmethod
    def do(p1):
        p1.framex = (p1.framex + 68 * ACTION_PER_TIME/4 * frame_work.frame_time)
        if p1.framex >68:
            p1.framex = 8
            p1.state_machine.add_event(('IDLE', 0))



    @staticmethod
    def draw(p1):
        size = 112
        playersize = 1.8
        if p1.dire == 0:
            p1.image.clip_composite_draw(int(p1.framex)%12 * size, (6-int(p1.framex)//12) * 133, size, 133
                                         , 0, 'h', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y + 30,
                                         200 * playersize, 200 * playersize)
        else:
            p1.image.clip_composite_draw(int(p1.framex )%12 * size, (6-int(p1.framex)//12) * 133, size, 133
                                         , 0, 'i', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y + 30,
                                         200 * playersize, 200 * playersize)

class Skill:
    @staticmethod
    def enter(p1, e):
        if skill(e):
            if (e[1].key == SDLK_1):
                if p1.mp>=20 and p1.skills[0]:
                    p1.mp -= 20
                    p1.skillnum = 1
                    p1.skill(p1.skillnum)
                    p1.framex = 20
                else:
                    p1.state_machine.add_event(('IDLE', 0))
            elif (e[1].key == SDLK_2):
                if p1.mp>=20 and p1.skills[1]:
                    p1.mp -= 20
                    p1.skillnum=2
                    p1.framex = 52
                else:
                    p1.state_machine.add_event(('IDLE', 0))
            elif (e[1].key == SDLK_3):
                if p1.mp>=20 and p1.skills[2]:
                    p1.mp -= 20
                    p1.skillnum=3
                    p1.skill(p1.skillnum)
                else:
                    p1.state_machine.add_event(('IDLE', 0))
            elif (e[1].key == SDLK_4):
                if p1.mp >= 40 and p1.skills[3]:
                    p1.mp -= 40
                    p1.skillnum = 4
                    p1.invincible = 1
                    p1.skill(p1.skillnum)
                else:
                    p1.state_machine.add_event(('IDLE', 0))
            elif (e[1].key == SDLK_5):
                if p1.mp >= 50 and p1.skills[4]:
                    p1.mp -= 50
                    p1.skillnum = 5
                    p1.framex = 20
                    for i in range(5):
                        p1.skill(p1.skillnum)
                else:
                    p1.state_machine.add_event(('IDLE', 0))
            elif (e[1].key == SDLK_6):
                if p1.mp >= 70 and p1.skills[5]:
                    p1.mp -= 70
                    p1.skillnum = 6
                    p1.framex = -24
                else:
                    p1.state_machine.add_event(('IDLE', 0))

    @staticmethod
    def exit(p1, e):
        if p1.skillnum==2:
            p1.skill(p1.skillnum)
        if p1.skillnum==3:
            if p1.hp<=90:
                p1.hp+=10
        if p1.skillnum==6:
            p1.skill(p1.skillnum)
            pass
        p1.skillnum=0

    @staticmethod
    def do(p1):
        p1.framex = (p1.framex + 68 * ACTION_PER_TIME / 4 * frame_work.frame_time)
        if p1.skillnum==1:
            if p1.framex > 20+12:
                p1.state_machine.add_event(('IDLE', 0))
        elif p1.skillnum==2:
            if p1.framex > 52+17:
                p1.state_machine.add_event(('IDLE', 0))
        elif p1.skillnum==3:
            p1.state_machine.add_event(('IDLE', 0))
        elif p1.skillnum==4:
            p1.state_machine.add_event(('IDLE', 0))
        elif p1.skillnum==5:
            if p1.framex > 20+36:
                p1.state_machine.add_event(('IDLE', 0))
        elif p1.skillnum==6:
            if p1.framex > -13:
                p1.state_machine.add_event(('IDLE', 0))


    @staticmethod
    def draw(p1):
        size = 112
        playersize = 1.8
        if p1.dire == 0:
            p1.image.clip_composite_draw(int(p1.framex) % 12 * size, (6 - int(p1.framex) // 12) * 133, size, 133
                                         , 0, 'h', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y + 30,
                                         200 * playersize, 200 * playersize)
        else:
            p1.image.clip_composite_draw(int(p1.framex) % 12 * size, (6 - int(p1.framex) // 12) * 133, size, 133
                                         , 0, 'i', WIDTH // 2 - p1.viewX + p1.x, HEIGHT // 2 - p1.viewY + p1.y + 30,
                                         200 * playersize, 200 * playersize)


