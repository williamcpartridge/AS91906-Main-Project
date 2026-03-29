import pygame
import random
from settings import Settings

clock = pygame.time.Clock()
FPS = 60

scr_x=640 ; scr_y=480
fullscreen = False
alive = True
x, y = 0, 0
eaten = False
ax = 0
ay = 0
input_num = 0

pygame.init()

pygame.display.set_caption('Snake game')

if fullscreen: screen = pygame.display.set_mode((scr_x, scr_y), pygame.FULLSCREEN)
else: screen = pygame.display.set_mode((scr_x, scr_y), pygame.RESIZABLE)

player_surf = pygame.Surface((10, 10))
player_surf.fill((0, 255, 0))

apple_surf = pygame.Surface((10, 10))
apple_surf.fill((255, 0, 0))

bg_surf = pygame.Surface((10, 10))
bg_surf.fill((10, 200, 10))

snake_x = [0]
snake_y = [0]
direction_x = 1
direction_y = 0
tile  = 1
fc = 0

apple_list = []


def game_init():
    tile = 1
    for x in range(round(scr_x/10)):
        for y in range(round(scr_y/10)):
            if tile % 2 == 0:
                bg_surf.fill((10, 180, 10))
            else:
                bg_surf.fill((30, 160, 30))

            screen.blit(bg_surf, (x*10, y*10))
            tile += 1


def apple():
    ax = 10*random.randint(0, round(scr_x/10))
    ay = 10*random.randint(0, round(scr_y/10))
    return (ax, ay)




    
#game_init()

while alive:
    input_num = 0
    fc += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False
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

    if not fc%6:
        if snake_x[0] + direction_x in snake_x and snake_y[0] + direction_y in snake_y:
            alive = False
        elif snake_x[0] + direction_x < 0 or snake_y[0] + direction_y < 0 or snake_x[0] + direction_x > (scr_x-10)/10 or snake_y[0] + direction_y > (scr_y-10)/10:
            alive = False
        else:
            snake_y.insert(0, snake_y[0] + direction_y)
            snake_x.insert(0, snake_x[0] + direction_x)

        if not eaten:
            snake_x.pop()
            snake_y.pop()
    
        eaten = False

    screen.fill((0, 0, 0))
    #game_init()

    if len(apple_list) <= 0:
        ax, ay = apple()
        apple_list.append((ax, ay))
        print(apple_list)
    
    for i in range(len(apple_list)):
        screen.blit(apple_surf, apple_list[i])

    for seg in range(len(snake_x)):
        screen.blit(player_surf, (10*snake_x[seg], 10*snake_y[seg]))
        if 10*snake_x[seg] == ax and 10*snake_y[seg] == ay:
            eaten = True
            print((10*snake_x[seg], 10*snake_y[seg]))
            apple_list.remove((10*snake_x[seg], 10*snake_y[seg]))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()