import pygame
import random
from settings import Settings
from button import Button
from mysprite import MySprite
from imagelist import ImageList


clock = pygame.time.Clock()
FPS = 60

scr_x=640 ; scr_y=480
snake_x, snake_y, snake_w, snake_h = 0, 0, 10, 10

pygame.init()

pygame.display.set_caption('Snake game')

screen = pygame.display.set_mode((scr_x, scr_y), pygame.RESIZABLE)
enemy_images = ImageList("images\\enemy\\enemy", 100, 100)
apple_images = ImageList("images\\apple\\apple", 100, 100)
snake_head_img = ImageList("images\\snake\\head\\snake_head", 100, 100)
snake_body_img = ImageList("images\\snake\\body\\snake_body", 100, 100)

snake_head = MySprite(snake_x, snake_y, snake_w, snake_h, snake_head_img, screen)
snake_body = MySprite(snake_x, snake_y, snake_w, snake_h, snake_body_img, screen)

apple_surf = pygame.Surface((10, 10))
apple_surf.fill((255, 0, 0))

bg_surf = pygame.transform.scale(pygame.image.load('images\\main_gui\\bg.jpg').convert_alpha(), (screen.get_width(), screen.get_height()))
bg_rect = bg_surf.get_rect(center=(screen.get_width()/2, screen.get_height()/2))


font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 75)


def spawn_apple():
    ax = 10*random.randint(0, round(screen.get_width()/10))
    ay = 10*random.randint(0, round(screen.get_height()/10))
    return (ax, ay)


def main_menu(screen, bg_surf, bg_rect):
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        play_button = Button((screen.get_width()/2, 100), font, 'Play')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.pressed(mouse_pos):
                    main_game_loop(screen)
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                bg_surf = pygame.transform.scale(pygame.image.load('images\\main_gui\\bg.jpg').convert_alpha(), (screen.get_width(), screen.get_height()))
                bg_rect = bg_surf.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()


        screen.blit(bg_surf, bg_rect)
        play_button.draw(screen)


        pygame.display.flip()
        clock.tick(FPS)


def main_game_loop(screen):
    alive = True
    fc = 0
    snake_x = [0]
    snake_y = [0]
    direction_x = 1
    direction_y = 0
    eaten = False
    ax = 0
    ay = 0
    input_num = 0
    apple_list = []
    snake_length = 1


    while alive:
        input_num = 0
        fc += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                bg_surf = pygame.transform.scale(pygame.image.load('images\\main_gui\\bg.jpg').convert_alpha(), (screen.get_width(), screen.get_height()))
                bg_rect = bg_surf.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    alive = False
                if input_num == 0:
                    if direction_y != 1 and event.key == pygame.K_w:
                        direction_x = 0
                        direction_y = -1
                        input_num = 1
                    if direction_y != -1 and event.key == pygame.K_s:
                        direction_x = 0
                        direction_y = 1
                        input_num = 1
                    if direction_x != -1 and event.key == pygame.K_d:
                        direction_x = 1
                        direction_y = 0
                        input_num = 1
                    if direction_x != 1 and event.key == pygame.K_a:
                        direction_x = -1
                        direction_y = 0
                        input_num = 1
        if snake_length == 1:
            snake_head.move(10*direction_x, 10*direction_y, 1)
        else:
            snake_head.move(10*direction_x, 10*direction_y, 1)
            for i in len(snake_length):
                snake_body.move((i + 2)10*direction_x, 10*direction_y, 1)
        """
        if not fc%6:
            if snake_x[0] + direction_x in snake_x and snake_y[0] + direction_y in snake_y:
                alive = False
            elif snake_x[0] + direction_x < 0 or snake_y[0] + direction_y < 0 or snake_x[0] + direction_x > (screen.get_width()-10)/10 or snake_y[0] + direction_y > (screen.get_height()-10)/10:
                alive = False
            else:
                seg_count = 0
                for x in snake_x:
                    for y in snake_y:
                        if seg_count == 0:
                            snake_head.move(direction_x, direction_y, 1)
                            snake_head.draw()
                        else:
                            snake_body.move(direction_x, direction_y, 1)
                            snake_body.draw()
        

            if not eaten:
                snake_x.pop()
                snake_y.pop()
        
            eaten = False
        """

        screen.fill((0, 0, 0))

        if len(apple_list) <= 0:
            ax, ay = spawn_apple()
            apple_list.append(MySprite(ax, ay, apple_surf.width, apple_surf.height, apple_images, screen))
            apple_list[-1].set_animation(0, 2, 1, True)

            print(apple_list)
        
        for apple in apple_list:
            apple.draw()
        
        snake_head.draw()
        snake_body.draw()


        '''
            if 10*snake_x[seg] == ax and 10*snake_y[seg] == ay:
                eaten = True
                print((10*snake_x[seg], 10*snake_y[seg]))
                apple_list.remove((10*snake_x[seg], 10*snake_y[seg]))
        '''


        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu(screen, bg_surf, bg_rect)

pygame.quit()