import pygame
import random

clock = pygame.time.Clock()
FPS = 10

scr_x=640 ; scr_y=480
fullscreen = False
done = False
x, y = 0, 0
eaten = False
ax = 0
ay = 0

pygame.init()

pygame.display.set_caption('Snake game')

if fullscreen: screen = pygame.display.set_mode((scr_x, scr_y), pygame.FULLSCREEN)
else: screen = pygame.display.set_mode((scr_x, scr_y), pygame.RESIZABLE)

player_surf = pygame.Surface((10, 10))
player_surf.fill((0, 255, 0))

apple_surf = pygame.Surface((10, 10))
apple_surf.fill((255, 0, 0))

snake_x = [0]
snake_y = [0]
direction_x = 1
direction_y = 0

apple_list = []

def apple():
    ax = 10*random.randint(0, round(scr_x/10))
    ay = 10*random.randint(0, round(scr_y/10))
    return (ax, ay)

    

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            
            if event.key == pygame.K_w:
                direction_x = 0
                direction_y = -1
            if event.key == pygame.K_s:
                direction_x = 0
                direction_y = 1
            if event.key == pygame.K_d:
                direction_x = 1
                direction_y = 0
            if event.key == pygame.K_a:
                direction_x = -1
                direction_y = 0

    if snake_x[0] + direction_x in snake_x and snake_y[0] + direction_y in snake_y:
        done = True
    elif snake_x[0] + direction_x < 0 or snake_y[0] + direction_y < 0 or snake_x[0] + direction_x > (scr_x-10)/10 or snake_y[0] + direction_y > (scr_y-10)/10:
        done = True
    else:
        snake_y.insert(0, snake_y[0] + direction_y)
        snake_x.insert(0, snake_x[0] + direction_x)


    if not eaten:
        snake_x.pop()
        snake_y.pop()
    
    eaten = False

    screen.fill((0, 0, 0))
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