import pygame
from imagelist import ImageList

class MySprite():
    def __init__(self, x, y, w, h, images, screen):
        self._screen = screen
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
        self._w = w
        self._h = h
        self._images = images
        self._screen = screen

        if valid == False:
            print("SOMTHING WENT WRONG\n    Parametres:", "\nx:", x, "\ny:", y, "\nwidth:", w, "\nheight:", h)
            exit(0)
            
    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._w, self._h)

    def collide(self, other_rect):
        if isinstance(other_rect, pygame.Rect):
            if

        A = self.get_rect()
        B = self.get_rect()

        if not (A.y > B.y + B.h or A.y + A.h < B.y  or A.x > B.x + B.w or A.x + A.w < B.x):
            print("colideee")
        else:
            print("not colide")



    def draw():
        pass

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    images = ImageList("images\\enemy\\enemy", 20, 20)
    sprite = MySprite(1, 0, 50, 50, images, screen)