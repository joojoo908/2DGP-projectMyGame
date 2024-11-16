from pico2d import load_image
import play_mod

class Pannel:
    def __init__(self):
        self.image = load_image('skill_back.png')
        self.sk1= load_image('state/skill1.png')
        self.sk =load_image('state/skills.png')
        self.sk3 =load_image('state/skill3.png')

    def draw(self):
        self.image.opacify(100)
        self.image.clip_composite_draw(0, 0, 256, 256, 0, '',
                    700,500 , 1000, 800)

        self.sk.opacify(150 - 140*play_mod.p1.skills[0] )
        self.sk.clip_composite_draw(16 * 11, 16 * 3, 16, 16, 0, 'h',
                                    400, 700, 100, 100)
        self.sk.opacify(150 - 140*play_mod.p1.skills[1])
        self.sk.clip_composite_draw(16*4, 16*1, 16, 16, 0, 'h',
                                    700, 700, 100, 100)
        self.sk.opacify(150 - 140*play_mod.p1.skills[2])
        self.sk.clip_composite_draw(16 * 0, 16 * 2, 16, 16, 0, 'h',
                                    1000, 700, 100, 100)

        self.sk.opacify(150 - 140*play_mod.p1.skills[3])
        self.sk.clip_composite_draw(16 * 4, 16 * 0, 16, 16, 0, 'h',
                                    400, 400, 100, 100)
        self.sk.opacify(150 - 140*play_mod.p1.skills[4])
        self.sk.clip_composite_draw(16 * 2, 16 * 0, 16, 16, 0, 'h',
                                    700, 400, 100, 100)
        self.sk.opacify(150 - 140*play_mod.p1.skills[5])
        self.sk.clip_composite_draw(16 * 3, 16 * 1, 16, 16, 0, 'h',
                                    1000, 400, 100, 100)

    def update(self):
        pass