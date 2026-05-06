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

apple_surf = pygame.Surface((10, 10))

screen = pygame.display.set_mode((scr_x, scr_y), pygame.RESIZABLE)
enemy_images = ImageList("images\\enemy\\enemy", 100, 100)
apple_images = ImageList("images\\apple\\apple", apple_surf.width, apple_surf.height)
snake_head_img = ImageList("images\\snake\\head\\snake_head", snake_w, snake_h)
snake_body_img = ImageList("images\\snake\\body\\snake_body", snake_w, snake_h)


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
    direction_x = 1
    direction_y = 0
    store_dirx = 0
    store_diry = 0
    eaten = False
    ax = 0
    ay = 0
    input_num = 0
    apple_list = []
    segments = [MySprite(snake_x, snake_y, snake_w, snake_h, snake_head_img, screen)]


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
                        store_dirx = direction_x
                        store_diry = direction_y
                        direction_x = 0
                        direction_y = -1
                        input_num = 1
                    if direction_y != -1 and event.key == pygame.K_s:
                        store_dirx = direction_x
                        store_diry = direction_y
                        direction_x = 0
                        direction_y = 1
                        input_num = 1
                    if direction_x != -1 and event.key == pygame.K_d:
                        store_dirx = direction_x
                        store_diry = direction_y
                        direction_x = 1
                        direction_y = 0
                        input_num = 1
                    if direction_x != 1 and event.key == pygame.K_a:
                        store_dirx = direction_x
                        store_diry = direction_y
                        direction_x = -1
                        direction_y = 0
                        input_num = 1
        if fc%6:
            for seg in segments:
                print(seg)
                seg.move(10*direction_x, 10*direction_y, 0.1)
                for apple in apple_list:
                    if seg.collide(apple.get_rect()):
                        new = MySprite(snake_x, snake_y, snake_w, snake_h, snake_body_img, screen)
                        new.set_pos(seg.get_x() - store_dirx, seg.get_y() - store_diry)
                        segments.append(new)

        if len(apple_list) <= 0:
            ax, ay = spawn_apple()
            apple_list.append(MySprite(ax, ay, apple_surf.width, apple_surf.height, apple_images, screen))
            apple_list[-1].set_animation(0, 2, 1, True)

        screen.fill((0, 0, 0))

        
        for apple in apple_list:
            apple.draw()
        
        for seg in segments:
            seg.draw()


        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    #main_menu(screen, bg_surf, bg_rect)
    main_game_loop(screen)

pygame.quit()