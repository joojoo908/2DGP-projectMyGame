from pico2d import *
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key==SDLK_SPACE
def dash_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key==SDLK_d
def damage(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key==SDLK_l
def attack(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key==SDLK_a
def die(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key==SDLK_k

def skill(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key==SDLK_1 or
            e[1].key==SDLK_2)

def time_out(e):
    return e[0]=='TIME_OUT'
def run_over(e):
    return e[0]=='RUN_OVER'
def damage_over(e):
    return e[0]=='DAMAGE_OVER'
def dash_over(e):
    return e[0]=='DASH_OVER'
def death(e):
    return e[0] == 'DEATH'
def idle(e):
    return e[0] == 'IDLE'
def mouse_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN

def move(e):
    return e[0] == 'MOVE'
def atk(e):
    return e[0] == 'ATK'
def dmg(e):
    return e[0] == 'DMG'

class StateMachine:
    def __init__(self,o):
        self.o = o
        self.event_que=[]

    def start(self , state):
        self.cur_state = state
        self.cur_state.enter(self.o,('start',0))
        pass
    def add_event(self,e):
        self.event_que.append(e)
    def set_transitions(self,transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            event=self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.o)
    def handle_event(self,e):
        for event,next_state in self.transitions[self.cur_state].items():
            if event(e):
                self.cur_state.exit(self.o,e)
                self.cur_state = next_state
                self.cur_state.enter(self.o,e)