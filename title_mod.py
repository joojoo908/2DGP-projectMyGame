import frame_work
from pico2d import*
import play_mod

def init():
    global image
    global logo_start_time
    global font

    font = load_font('ENCR10B.TTF', 32)
    image = load_image('skill_back.png')
    #image = load_image('title.png')

    logo_start_time=get_time()

def finish():
    global image
    del image

def update():
    # global logo_start_time
    # if get_time() -logo_start_time >2.0:
    #     logo_start_time =get_time()
    #     game_framework.quit()
    pass

def draw():
    clear_canvas()
    image.clip_composite_draw(0,0,800,600,0,'',700,500,
                                           1400,1000)
    font.draw(530, 200, f'Click to Start', (0, 0, 0))
    update_canvas()

def handle_events():
    events =get_events()
    for event in events:
        if event.type == SDL_QUIT:
            frame_work.quit()
        elif event.type==SDL_KEYDOWN and event.key ==SDLK_ESCAPE:
            frame_work.quit()
        elif event.type==SDL_KEYDOWN:
            frame_work.change_mode(play_mod)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            frame_work.change_mode(play_mod)