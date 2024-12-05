import frame_work
from pico2d import*
import title_mod

def init():
    global image
    global logo_start_time

    image = load_image('tuk_credit.png')

    logo_start_time=get_time()

def finish():
    global image
    del image

def update():
    global logo_start_time
    if get_time() -logo_start_time >2.0:
        logo_start_time =get_time()
        frame_work.change_mode(title_mod)

def draw():
    clear_canvas()
    image.clip_composite_draw(0,0,800,600,0,'',700,500,
                                           1400,1000)
    update_canvas()

def handle_events():
    events =get_events()