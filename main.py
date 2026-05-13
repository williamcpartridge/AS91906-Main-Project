import pygame
import random
from settings import Settings
from button import Button
from mysprite import MySprite
from imagelist import ImageList
from tilespawn import TileSpawn


clock = pygame.time.Clock()
FPS = 60

cell_width, cell_height = 40, 40
cell_cx, cell_cy = 6, 5

snake_x, snake_y = cell_width+(cell_width/2), cell_height/2
scr_x=cell_width*cell_cx ; scr_y=cell_width*cell_cy


pygame.init()

pygame.display.set_caption('Snake game')

apple_surf = pygame.Surface((cell_width, cell_height))

screen = pygame.display.set_mode((scr_x, scr_y), pygame.RESIZABLE)
enemy_images = ImageList("images\\enemy\\enemy", 100, 100)
apple_images = ImageList("images\\apple\\apple", apple_surf.get_width(), apple_surf.get_height())
snake_head_img = ImageList("images\\snake\\head\\snake_head", cell_width, cell_height)
snake_body_img = ImageList("images\\snake\\body\\snake_body", cell_width, cell_height)

tiles = TileSpawn(cell_cx, cell_cy, cell_width, cell_height, screen)

bg_surf = pygame.transform.scale(pygame.image.load('images\\main_gui\\bg.jpg').convert_alpha(), (screen.get_width(), screen.get_height()))
bg_rect = bg_surf.get_rect(center=(screen.get_width()/2, screen.get_height()/2))


font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 75)

def get_cell_x(x):
    return int(x/cell_width)

def get_cell_y(y):
    return int(y/cell_height)

def spawn_apple():
    ax = (cell_width*random.randint(0, cell_cx - 1)) + apple_surf.get_width()/2
    ay = (cell_height*random.randint(0, cell_cy - 1)) + apple_surf.get_height()/2
    return (ax, ay)


def main_menu(screen, bg_surf, bg_rect):
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        play_button = Button((screen.get_width()/2, 2*(screen.get_height()/8)), font, 'Play')
        exit_button = Button((screen.get_width()/2, 6*(screen.get_height()/8)), font, 'Exit')
        settings_button = Button((screen.get_width()/2, 4*(screen.get_height()/8)), font, 'Settings')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.pressed(mouse_pos):
                    main_game_loop(screen)
                if exit_button.pressed(mouse_pos):
                    print("bye bye")
                    pygame.quit()
                if settings_button.pressed(mouse_pos):
                    print("Settings")
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                bg_surf = pygame.transform.scale(pygame.image.load('images\\main_gui\\bg.jpg').convert_alpha(), (screen.get_width(), screen.get_height()))
                bg_rect = bg_surf.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()


        screen.blit(bg_surf, bg_rect)
        play_button.draw(screen)
        exit_button.draw(screen)
        settings_button.draw(screen)


        pygame.display.flip()
        clock.tick(FPS)


def main_game_loop(screen):
    tiles.spawn_tiles()
    alive = True
    fc = 0
    direction_x = 1
    direction_y = 0
    ax = 0
    ay = 0
    input_num = 0
    apple_list = []
    movement = [(1, 0, 270)]
    angle = 270
    segments = [MySprite(snake_x, snake_y, cell_width, cell_height, snake_head_img, screen, angle), MySprite(snake_x - cell_width, snake_y, cell_width, cell_height, snake_body_img, screen, angle)]
    for segment in segments:
        segment.move(cell_width, 0, 0.1)

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
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        if movement[0][2] != 180 and movement[0][2] != 0:
                            direction_x = 0
                            direction_y = -1
                            angle = 0
                            input_num = 1
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if movement[0][2] != 180 and movement[0][2] != 0:
                            direction_x = 0
                            direction_y = 1
                            angle = 180
                            input_num = 1
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if movement[0][2] != 270 and movement[0][2] != 90:
                            direction_x = 1
                            direction_y = 0
                            angle = 270
                            input_num = 1
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if movement[0][2] != 270 and movement[0][2] != 90:
                            direction_x = -1
                            direction_y = 0
                            angle = 90
                            input_num = 1
                    

        
        
        if not fc%20:
            tiles.tile(segments[-2].get_x(), segments[-2].get_y())
            tiles.tile(segments[-1].get_x(), segments[-1].get_y())
            tiles.tile(segments[0].get_x(), segments[0].get_y())

            movement.insert(0, (direction_x, direction_y, angle))
            if len(movement) > len(segments):
                movement.pop()
            for i in range(len(segments)):
                if i == len(segments) -1:
                    segments[i].rotate(movement[i-1][2])
                else:
                    segments[i].rotate(movement[i][2])

                segments[i].move(cell_width*movement[i][0], cell_height*movement[i][1])
                for apple in apple_list:
                    if get_cell_x(segments[i].get_x()) == get_cell_x(apple.get_x()) and get_cell_y(segments[i].get_y()) == get_cell_y(apple.get_y()):
                        new = MySprite(segments[-1].get_x(), segments[-1].get_y(), cell_width, cell_height, snake_body_img, screen)
                        new.rotate(movement[-1][2])
                        segments.append(new)
                        apple_list.remove(apple)
                        segments[-2].set_frame(1)

            for i in range(len(movement)):
                if i != 0 and len(segments) > 2 and i != len(movement)-1:
                    if movement[i][2] != movement[i-1][2]:
                        if movement[i-1][2] - movement[i][2] == -90:
                            segments[i].set_frame(2) #left
                        elif movement[i][2] - movement[i-1][2] == -90:
                            segments[i].set_frame(3) #right

                        elif movement[i-1][2] - movement[i][2] == 270:
                            segments[i].set_frame(2) #left

                        elif movement[i][2] - movement[i-1][2] == 270:
                            segments[i].set_frame(3) #right

                            
                    else:
                        segments[i].set_frame(1)
                        


            for segment in segments:
                if segment != segments[0]:
                    if get_cell_x(segments[0].get_x()) == get_cell_x(segment.get_x()) and get_cell_y(segments[0].get_y()) == get_cell_y(segment.get_y()):
                        alive = False
                
            if segments[0].get_x() < cell_width/2 or segments[0].get_x() > screen.get_width() - cell_width/2 or segments[0].get_y() < cell_height/2 or segments[0].get_y() > screen.get_height() - cell_height/2:
                alive = False

        if len(segments) == cell_cx*cell_cy:
            print("you won")

        if len(apple_list) <= 0:
            ax, ay = spawn_apple()
            apple_list.append(MySprite(ax, ay, apple_surf.get_width(), apple_surf.get_height(), apple_images, screen))
            apple_list[-1].set_animation(0, 2, 1, True)

        
        for apple in apple_list:
            apple.draw()
        
        for seg in segments:
            seg.draw()


        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu(screen, bg_surf, bg_rect)
    #main_game_loop(screen)
    #spawn_tiles()

pygame.quit()