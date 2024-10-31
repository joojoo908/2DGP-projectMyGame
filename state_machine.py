from pico2d import *
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key==SDLK_SPACE
def dash_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key==SDLK_d
def time_out(e):
    return e[0]=='TIME_OUT'
def run_over(e):
    return e[0]=='RUN_OVER'
def mouse_move(e):
    return 0
def mouse_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN


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