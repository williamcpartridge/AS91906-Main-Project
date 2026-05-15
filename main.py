import os
import pygame
import random
from settings import Settings
from button import Button
from mysprite import MySprite
from imagelist import ImageList
from tilespawn import TileSpawn


class Snake():
    def __init__(self, segments, movement, cell_w, cell_h, dir_x, dir_y, angle, screen):
        self._segments = segments
        self._movement = movement
        self._cell_w = cell_w
        self._cell_h = cell_h
        self._screen = screen
        self._dir_x = dir_x
        self._dir_y = dir_y
        self._angle = angle
        self._add_segment = False

    def get_cell_x(self, x):
        return int(x/self._cell_w)

    def get_cell_y(self, y):
        return int(y/self._cell_h)
    
    def set_dir_x(self, dir_x):
        self._dir_x = dir_x
    
    def get_dir_x(self):
        return self._dir_x

    def set_dir_y(self, dir_y):
        self._dir_y = dir_y

    def get_dir_y(self):
        return self._dir_y

    def set_angle(self, angle):
        self._angle = angle

    def get_angle(self):
        return self._angle

    def set_movement(self, dir_x, dir_y, angle):
        self.set_dir_x(dir_x)
        self.set_dir_y(dir_y)
        self.set_angle(angle)

    def get_movement(self):
        return (self.get_dir_x(), self.get_dir_y(), self.get_angle())

    def step(self):
        self._movement.insert(0, self.get_movement())
        if len(self._movement) > len(self._segments):
            self._movement.pop()
        for i in range(len(self._segments)):
            if i == len(self._segments) -1:
                self._segments[i].rotate(self._movement[i-1][2])
            else:
                self._segments[i].rotate(self._movement[i][2])

            self._segments[i].move(self._cell_w*self._movement[i][0], self._cell_h*self._movement[i][1])

    def cell_collide(self, obj):
        if self.get_cell_x(self._segments[0].get_x()) == self.get_cell_x(obj.get_x()) and \
            self.get_cell_y(self._segments[0].get_y()) == self.get_cell_y(obj.get_y()):
            return True

    def new_seg(self):
        new = MySprite(self._segments[-1].get_x() - self._movement[-1][0]*self._cell_w, \
                       self._segments[-1].get_y() - self._movement[-1][1]*self._cell_h, \
                        cell_width, cell_height, snake_body_img, screen)
        new.rotate(self._movement[-1][2])
        new.set_frame(0)
        return new

    def append_seg(self, new):
        self._segments.append(new)
        

    def check_rotation(self):
        for i in range(len(self._movement)):
            if i != 0 and len(self._segments) > 2 and i != len(self._movement)-1:
                if self._movement[i][2] != self._movement[i-1][2]:
                    if self._movement[i-1][2] - self._movement[i][2] == -90:
                        self._segments[i].set_frame(2) #left
                    elif self._movement[i][2] - self._movement[i-1][2] == -90:
                        self._segments[i].set_frame(3) #right

                    elif self._movement[i-1][2] - self._movement[i][2] == 270:
                        self._segments[i].set_frame(2) #left

                    elif self._movement[i][2] - self._movement[i-1][2] == 270:
                        self._segments[i].set_frame(3) #right
                        
                else:
                    self._segments[i].set_frame(1)

    def death_check(self):
        for segment in self._segments:
            if segment != self._segments[0]:
                if self.cell_collide(segment):
                    return True
            
        if self._segments[0].get_x() < self._cell_w/2 or self._segments[0].get_x() > self._screen.get_width() - self._cell_w/2 or \
            self._segments[0].get_y() < self._cell_h/2 or self._segments[0].get_y() > self._screen.get_height() - self._cell_h/2:
            return True
        
    def start(self):
        for segment in self._segments:
            segment.move(cell_width, 0, 0.1)

    def draw(self):
        for seg in self._segments:
            seg.draw()

def spawn_apple():
    ax = (cell_width*random.randint(0, cell_cx - 1)) + apple_surf.get_width()/2
    ay = (cell_height*random.randint(0, cell_cy - 1)) + apple_surf.get_height()/2
    return (ax, ay)


def main_menu(screen, bg_surf, bg_rect, menu_screen_x, menu_screen_y):
    font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', int(menu_screen_x/12))
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        play_button = Button(3, 1, font, 'Play', screen)
        settings_button = Button(3, 2, font, 'Settings', screen)
        exit_button = Button(3, 3, font, 'Exit', screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.pressed(mouse_pos):
                    screen = pygame.display.set_mode((scr_x, scr_y), vsync=1)
                    main_game_loop(screen, menu_screen_x, menu_screen_y)
                if exit_button.pressed(mouse_pos):
                    print("bye bye")
                    pygame.quit()
                if settings_button.pressed(mouse_pos):
                    print("Settings")

                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()


        screen.blit(bg_surf, bg_rect)
        play_button.draw()
        exit_button.draw()
        settings_button.draw()


        pygame.display.flip()
        clock.tick(FPS)


def main_game_loop(screen, menu_screen_x, menu_screen_y):
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
    eaten = False
    segments = [MySprite(snake_x, snake_y, cell_width, cell_height, snake_head_img, screen, angle), \
                MySprite(snake_x - cell_width, snake_y, cell_width, cell_height, snake_body_img, screen, angle)]
    snake = Snake(segments, movement, cell_width, cell_height, direction_x, direction_y, angle, screen)

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
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        if movement[0][2] != 180 and movement[0][2] != 0:
                            snake.set_movement(0, -1, 0)
                            input_num = 1
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if movement[0][2] != 180 and movement[0][2] != 0:
                            snake.set_movement(0, 1, 180)
                            input_num = 1
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if movement[0][2] != 270 and movement[0][2] != 90:
                            snake.set_movement(1, 0, 270)
                            input_num = 1
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if movement[0][2] != 270 and movement[0][2] != 90:
                            snake.set_movement(-1, 0, 90)
                            input_num = 1
        
        if not fc%20:
            tiles.tile(segments[-2].get_x(), segments[-2].get_y())
            tiles.tile(segments[-1].get_x(), segments[-1].get_y())
            tiles.tile(segments[0].get_x(), segments[0].get_y())

            if eaten:
                snake.append_seg(new)
                eaten = False

            snake.step()

            for apple in apple_list:
                if snake.cell_collide(apple):
                    apple_list.remove(apple)
                    new = snake.new_seg()
                    eaten = True
            
            snake.check_rotation()       

            if snake.death_check():
                screen = pygame.display.set_mode((menu_screen_x, menu_screen_y))
                alive = False

        if len(segments) == cell_cx*cell_cy:
            print("you won")

        if len(apple_list) <= 0:
            ax, ay = spawn_apple()
            apple_list.append(MySprite(ax, ay, apple_surf.get_width(), apple_surf.get_height(), apple_images, screen))
            apple_list[-1].set_animation(0, 2, 1, True)

        for apple in apple_list:
            apple.draw()

        snake.draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    FPS = 60

    cell_width, cell_height = 40, 40
    cell_cx, cell_cy = 12, 9

    fullscreen = False

    if fullscreen:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        if cell_cx > cell_cy:
            cell_width = pygame.display.Info().current_h / cell_cy
            cell_height = pygame.display.Info().current_h / cell_cy
        else:
            cell_width = pygame.display.Info().current_w / cell_cx
            cell_height = pygame.display.Info().current_w / cell_cx

    snake_x, snake_y = cell_width+(cell_width/2), cell_height/2
    scr_x=cell_width*cell_cx ; scr_y=cell_width*cell_cy

    menu_screen_x, menu_screen_y = 1000, 700


    pygame.display.set_caption('Snake game')

    apple_surf = pygame.Surface((cell_width, cell_height))

    screen = pygame.display.set_mode((menu_screen_x, menu_screen_y), pygame.SCALED | pygame.RESIZABLE, vsync=1)
    enemy_images = ImageList("images\\enemy\\enemy", 100, 100)
    apple_images = ImageList("images\\apple\\apple", apple_surf.get_width(), apple_surf.get_height())
    snake_head_img = ImageList("images\\snake\\head\\snake_head", cell_width, cell_height)
    snake_body_img = ImageList("images\\snake\\body\\snake_body", cell_width, cell_height)

    tiles = TileSpawn(cell_cx, cell_cy, cell_width, cell_height, screen)

    bg_surf = pygame.transform.scale(pygame.image.load('images\\main_gui\\bg.jpg').convert_alpha(), (screen.get_width(), screen.get_height()))
    bg_rect = bg_surf.get_rect(center=(screen.get_width()/2, screen.get_height()/2))


    main_menu(screen, bg_surf, bg_rect, menu_screen_x, menu_screen_y)
    #main_game_loop(screen)
    #spawn_tiles()

pygame.quit()