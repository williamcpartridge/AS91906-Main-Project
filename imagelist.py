from os.path import exists
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

if __name__ == "__main__":
    image_obj = ImageList("images\\enemy\\enemy", 20, 20)
    pygame.init()

    screen = pygame.display.set_mode((500, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Snake Game by Me")
    quit_game = False
    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True

        screen.blit(pygame.image.load('images\\enemy\\enemy0.jpg'), (0, 0))

        pygame.display.flip()



    pygame.quit()
    quit()