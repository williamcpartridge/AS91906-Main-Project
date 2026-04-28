import pygame
from imagelist import ImageList
import debug
import time

class MySprite():
    def __init__(self, x, y, w, h, images, screen):
        valid = True
        if x >= 0 and x <= screen.get_width():
            self._x = x
        else:
            print("off screen (x)")
            valid = False
        if y >= 0 and y <= screen.get_height():
            self._y = y
        else:
            print("off screen (y)")
            valid = False
        if w > 0:
            self._w = w
        else: 
            print("width too small")
        if h > 0:
            self._h = h
        else: 
            print("Hieght too small")
        self._images = images

        self._screen = screen
        
        self._start_frame = 0
        self._end_frame = 0
        self._current_frame = 0
        self._delay = -1
        self._repeat = 0
        

        if valid == False:
            print("SOMTHING WENT WRONG\n    Parametres:", "\nx:", x, "\ny:", y, "\nwidth:", w, "\nheight:", h)
            exit(0)

    def get_x(self):
        return self._x

    def set_x(self, x):
        if x >= 0 and x < self._screen.get_width():
            self._x = x
        elif x < 0:
            self._x = 0
        else:
            self._x = self._screen.get_width()
        
    def get_y(self):
        return self._y

    def set_y(self, y):
        if y >= 0 and y < self._screen.get_height():
            self._y = y
        elif y < 0:
            self._y = 0
        else:
            self._y = self._screen.get_height() - 1

    x = property(get_x, set_x)
    y = property(get_y, set_y)

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def move(self, dx=None, dy=None):
        if not dx is None:
            self._dx = dx
        if not dy is None:
            self._dy = dy

        self._set_x(self._x, self._dx)
        self._set_y(self._x, self._dy)           

    def set_animation(self, start_frame=0, end_frame=0, delay=0, repeat=-1):
            if start_frame >= 0 and start_frame < len(self._images.images):
                self._start_frame = start_frame
            if end_frame >= 0 and end_frame < len(self._images.images) and start_frame <= end_frame:
                self._end_frame = end_frame
            if delay > 0:
                self._delay = delay
            if repeat > 0:
                self._repeat = repeat

            self._next_frame = time.time() + delay

    def animate(self, reset_animation = False):
        if not self._delay == -1:
            if reset_animation == True:
                self._current_frame = self._start_frame
            else:
                if time.time() > self._next_frame:
                    if self._current_frame < self._end_frame:
                        self._current_frame += 1
                    elif self._repeat > 0:
                        self._current_frame = self._start_frame
                        self._repeat -= 1
            
    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._w, self._h)

    def collide(self, other_rect):
        if isinstance(other_rect, pygame.Rect):
            A = self.get_rect()
            B = self.get_rect()

            if not (A.y > B.y + B.h or A.y + A.h < B.y or A.x > B.x + B.w or A.x + A.w < B.x):
                print("colideee")
            else:
                print("not colide")
                
    def draw(self):
        self._screen.blit(self._images[self._current_frame])


if __name__ == "__main__":
    pygame.init()


# TESTING
debug.DEBUG_LEVEL = 2
if __name__ == "__main__":
    TEST_X = 100
    TEST_Y = 100
    TEST_W = 30
    TEST_H = 30
    pygame.init()
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    images = ImageList("images\\enemy\\enemy", 20, 20)
    sprite1 = MySprite(0, 0, 50, 50, images, screen)
    sprite1.set_animation(0, 2, 50, 1)


    my_rect = pygame.Rect(TEST_X, TEST_Y, TEST_W, TEST_H)
    pygame.display.set_caption("Snake Game by Me")
    quit_game = False
    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True

        sprite1.draw()
        sprite1.animate()

        pygame.display.flip()



    pygame.quit()
    quit()