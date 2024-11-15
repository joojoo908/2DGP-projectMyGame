from pico2d import load_image

class Pannel:
    def __init__(self):
        self.image = load_image('skill_back.png')

    def draw(self):
        self.image.opacify(100)
        self.image.draw(700, 500)

    def update(self):
        pass