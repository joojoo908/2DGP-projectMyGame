import frame_work
from pico2d import*
import play_mod
from pygame.examples.cursors import image


def init():
    global image
    global font
    global logo_start_time
    global sound

    font = load_font('ENCR10B.TTF', 128)
    image = load_image('skill_back.png')

    if play_mod.p1.hp>0:
        sound = load_wav('music/Game_clear.mp3')
        sound.set_volume(32)
        #sound.play()
    else:
        sound = load_wav('music/Game_over.mp3')
        sound.set_volume(32)
        #sound.play()
    sound.set_volume(32)
    sound.play()

    logo_start_time=get_time()

def finish():
    global image
    del image

def update():
    #sound.play()
    pass

def draw():
    clear_canvas()
    image.clip_composite_draw(0,0,800,600,0,'',700,500,
                                           1400,1000)
    if play_mod.p1.hp>0:
        font.draw(350, 700, f'Game Clear', (0, 0, 0))
    else:
        font.draw(350, 700, f'Game Over', (0, 0, 0))
    update_canvas()

def handle_events():
    events =get_events()
    for event in events:
        if event.type == SDL_QUIT:
            frame_work.quit()
        elif event.type==SDL_KEYDOWN and event.key ==SDLK_ESCAPE:
            frame_work.quit()
        elif event.type==SDL_KEYDOWN:
            frame_work.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            frame_work.quit()