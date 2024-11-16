

import play_mod
from pico2d import load_image
WIDTH, HEIGHT = 1400, 1000
class State:
    def __init__(self,hp,mp):
        self.hp_bar = hp
        self.mp_bar = mp
        self.cir = load_image('state/Circle.png')
        self.icon = load_image('state/Icon.png')
        self.image = load_image('state/Bar.png')
        self.hp = load_image('state/Hp.png')
        self.mp = load_image('state/Mp.png')

    def draw(self):
        #self.image.opacify(100)
        self.cir.clip_composite_draw(0, 0, 41, 41
        , 0, '', 0+60, HEIGHT-60,100 , 100)
        self.icon.clip_composite_draw(0, 0, 17, 17
                                     , 0, '', 0 + 60, HEIGHT - 60, 50, 50)

        self.hp.clip_composite_draw(0, 0, 128, 16, 0, '',
                    0 + 350 -(150 * 3/2)*( 1- play_mod.p1.hp/self.hp_bar), HEIGHT - 40,
                                    (150 * 3)*(play_mod.p1.hp/self.hp_bar) , 16 * 2)
        self.image.clip_composite_draw(0, 0, 128, 16
                    , 0, '', 0 + 350, HEIGHT - 40, 150 * 3+10, 16 * 2)


        self.mp.clip_composite_draw(0, 0, 128, 16
                , 0, '', 0 + 350 - 37 -(150 * 2.5/2)*(1- play_mod.p1.mp/self.mp_bar) , HEIGHT - 80,
                        150 * 2.5*(play_mod.p1.mp/self.mp_bar), 16 * 2)
        self.image.clip_composite_draw(0, 0, 128, 16
                , 0, '', 0 + 350 - 37, HEIGHT - 80, 150 * 2.5+10, 16 * 2)

    def update(self,x,y):

        pass