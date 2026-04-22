from os.path import exists
import debug
import pygame

class ImageList():
    def __init__(self, filename, width, height):
        self._images = []
        count = 0
        while exists(filename+str(count)+'.jpg'):
            image = pygame.image.load(filename+str(count)+'.jpg')
            scaled = pygame.transform.smoothscale(image, [width, height])
            self._images.append(scaled)
            count += 1

    def get_images(self):
        return self._images
    
    images = property(get_images, None, None)


# TESTING
debug.DEBUG_LEVEL = 2
if __name__ == "__main__":
    TEST_X = 100
    TEST_Y = 100
    TEST_W = 30
    TEST_H = 30

    image_obj = ImageList("images\\enemy\\enemy", 20, 20)
    pygame.init()

    my_rect = pygame.Rect(TEST_X, TEST_Y, TEST_W, TEST_H)

    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    pygame.display.set_caption("Snake Game by Me")
    quit_game = False
    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True

        screen.blit(image_obj.images[0], my_rect)

        pygame.display.flip()



    pygame.quit()
    quit()