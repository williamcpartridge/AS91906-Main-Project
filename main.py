import pygame

clock = pygame.time.Clock()
FPS = 60

scr_x=640 ; scr_y=480
fullscreen = False
done = False
x, y = 0, 0

pygame.init()

pygame.display.set_caption('Snake game')

if fullscreen: screen = pygame.display.set_mode((scr_x, scr_y), pygame.FULLSCREEN)
else: screen = pygame.display.set_mode((scr_x, scr_y), pygame.RESIZABLE)

player_surf = pygame.Surface((10, 10))
player_surf.fill((0, 255, 0))

snake_x = [0]
snake_y = [0]

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            
            if event.key == pygame.K_w:
                snake_y.insert(0, snake_y[0] - 1)
                snake_x.insert(0, snake_x[0])
            if event.key == pygame.K_s:
                snake_y.insert(0, snake_y[0] + 1)
                snake_x.insert(0, snake_x[0])
            if event.key == pygame.K_d:
                snake_x.insert(0, snake_x[0] + 1)
                snake_y.insert(0, snake_y[0])
            if event.key == pygame.K_a:
                snake_x.insert(0, snake_x[0] - 1)
                snake_y.insert(0, snake_y[0])
        
    print(snake_x, snake_y)

    

    screen.fill((0, 0, 0))
    for seg in range(len(snake_x)):
        screen.blit(player_surf, (10*snake_x[seg], 10*snake_y[seg]))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()