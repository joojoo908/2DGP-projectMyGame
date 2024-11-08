import frame_work
from pico2d import *

import play_mod as start_mod
import logo_mod as start_mod

WIDTH, HEIGHT = 1400 , 1000

open_canvas(WIDTH, HEIGHT)
frame_work.run(start_mod)
close_canvas()