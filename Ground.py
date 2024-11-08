from pico2d import *

WIDTH, HEIGHT = 1400 , 1000
tilesize = 100

def load_tiles(filename):
    tiles = {}
    with open(filename, 'r') as f:
        for line in f:
            tile = eval(line.strip())
            x, y, tiletype, tilenum = tile
            tiles[(x, y)] = Ground(x, y, tiletype, tilenum)
    return tiles

class Ground:
    #global viewX , viewY
    image = None
    
    def __init__(self,x,y,tiletype,tilenum):
        self.x,self.y = x,y
        self.frame=0
        self.framecnt=0
        self.tiletype=tiletype
        self.tilenum=tilenum

        if Ground.image==None:
            if tiletype==0 or tiletype==3:
                self.image = load_image('Ground.png')
            elif tiletype==1:
                self.image = load_image('Water.png')
            elif tiletype==2:
                self.image = load_image('Cliff.png')
            elif tiletype==4:
                if tilenum<5:
                    self.image = load_image('Water_ani.png')
                else:
                    self.image = load_image('Ground_ani.png')
        
    def update(self):
        if self.tiletype==1 or self.tiletype==4:
            self.framecnt+=0.15
            if self.framecnt>9:
                self.frame = (self.frame+1)%8
                self.framecnt =0
        
        pass
    def draw(self,viewX,viewY):
         #self.image.draw(self.x,self.y)
        if self.tiletype==0:
            self.image.clip_composite_draw(0*176 + (self.tilenum%11)*16 , 2*80 + (4 - self.tilenum//11) *16, 16 + 0*176 , 16+ 0*80
                                           ,0,'i',WIDTH//2-viewX+ self.x+tilesize//2 ,HEIGHT//2 -viewY + self.y +tilesize//2 ,
                                           tilesize,tilesize)
        elif self.tiletype==1:
            self.image.clip_composite_draw(self.frame*176 +(self.tilenum%11)*16 , 1*80 +(4 - self.tilenum//11)*16 , 16 + 0*176 , 16+ 0*80 ,
                                           0,'i', WIDTH//2-viewX+ self.x +tilesize//2 ,HEIGHT//2 -viewY + self.y+tilesize//2, tilesize,tilesize)
        elif self.tiletype==2:
            self.image.clip_composite_draw(0*112 + (self.tilenum%7)*16 , 0*80 +(7 - self.tilenum//7)*16 , 16 + 0*176 , 16+ 0*80 ,
                                           0,'i', WIDTH//2-viewX+ self.x +tilesize//2 ,HEIGHT//2 -viewY + self.y+tilesize//2, tilesize,tilesize)
        elif self.tiletype==3:
            self.image.clip_composite_draw(0*176 + (self.tilenum%11)*16 , 0*80 + (4 - self.tilenum//11) *16, 16 + 0*176 , 16+ 0*80
                                           ,0,'i',WIDTH//2-viewX+ self.x+tilesize//2 ,HEIGHT//2 -viewY + self.y +tilesize//2 ,
                                           tilesize,tilesize)
        elif self.tiletype==4:
            if self.tilenum<5:
                self.image.clip_composite_draw(self.frame*16 , (4 - self.tilenum)*16 , 16 , 16 ,
                                           0,'i', WIDTH//2-viewX+ self.x +tilesize//2 ,HEIGHT//2 -viewY + self.y+tilesize//2, tilesize,tilesize)
            else:
                self.image.clip_composite_draw( (self.frame%2)*16*5 +(self.tilenum%5)*16 , (6 - (self.tilenum//5) )*16  , 16 , 16 ,
                                           0,'i', WIDTH//2-viewX+ self.x +tilesize//2 ,HEIGHT//2 -viewY + self.y+tilesize//2, tilesize,tilesize)

    def drawback(self):
        self.image.clip_composite_draw(0*176 + (12%11)*16 , 2*80 + (4 - 12//11) *16, 16 + 0*176 , 16+ 0*80
                                           ,0,'i',WIDTH//2, HEIGHT//2,
                                           WIDTH,HEIGHT)
