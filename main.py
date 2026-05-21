import os
import pygame
import random
from settings import Settings
from button import Button
from mysprite import MySprite
from imagelist import ImageList
from tilespawn import TileSpawn
import debug
debug.DEBUG_LEVEL = 1

class Snake():
    def __init__(self, movement, cell_w, cell_h, cell_cx, cell_cy, dir_x, dir_y, angle, screen):
        self._movement = movement
        self._cell_w = cell_w
        self._cell_h = cell_h
        self._cell_cx = cell_cx
        self._cell_cy = cell_cy
        self._screen = screen
        self._dir_x = dir_x
        self._dir_y = dir_y
        self._angle = angle
        self._add_segment = False

        self._snake_head_img = ImageList("images\\snake\\head\\snake_head", cell_width, cell_height)
        self._snake_body_img = ImageList("images\\snake\\body\\snake_body", cell_width, cell_height)

        snake_x = self._cell_w+(self._cell_w/2)
        snake_y = self._cell_h/2
        self._segments = [MySprite(snake_x, snake_y, self._cell_w, self._cell_h, self._snake_head_img, self._screen, self._angle), \
                MySprite(snake_x - self._cell_w, snake_y, self._cell_w, self._cell_h, self._snake_body_img, self._screen, self._angle)]

    def get_head_pos(self):
        return (self._segments[0].get_x(), self._segments[0].get_y())
    
    def get_cell_poss(self):
        temp = []
        for seg in self._segments:
            temp.append((self.get_cell_x(seg.get_x()), self.get_cell_y(seg.get_y())))
        #debug.dprint(2, temp)
        return temp

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
        tiles.tile(self._segments[-2].get_x(), self._segments[-2].get_y())
        tiles.tile(self._segments[-1].get_x(), self._segments[-1].get_y())
        tiles.tile(self._segments[0].get_x(), self._segments[0].get_y())

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
                        self._cell_w, self._cell_h, self._snake_body_img, self._screen)
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

    def win_check(self):
        if len(self._segments) == self._cell_cx*self._cell_cy:
            return True
        else:
            return False

    def draw(self):
        for seg in self._segments:
            seg.draw()

class Apple():
    def __init__(self, cell_w, cell_h, cell_cx, cell_cy, apple_count, screen):
        self._cell_w = cell_w
        self._cell_h = cell_h
        self._cell_cx = cell_cx
        self._cell_cy = cell_cy
        self._apple_list = []
        self._apple_count = apple_count
        self._screen = screen
        self._apple_images = ImageList("images\\apple\\apple", cell_width, cell_height)


    def spawn_apple(self, snake_cells):
        if len(self._apple_list) < self._apple_count and ((self._cell_cx*self._cell_cy) - len(snake_cells)) > self._apple_count:
            done = False
            while not done:
                cell_x = random.randint(0, self._cell_cx - 1) 
                cell_y = random.randint(0, self._cell_cy - 1)
                done = True
            
                print((cell_x, cell_y), snake_cells)
                if (cell_x, cell_y) in snake_cells:
                    done = False

                for a in self._apple_list:
                    ax = int(a.get_x() / self._cell_w)
                    ay = int(a.get_y() / self._cell_h)

                    if (cell_x, cell_y) == (ax, ay):
                        done = False

            debug.dprint(2, (cell_x, cell_y))
            ax = cell_x * self._cell_w + self._cell_w / 2
            ay = cell_y * self._cell_h + self._cell_h / 2
            self._apple_list.append(MySprite(ax, ay, self._cell_w, self._cell_h, self._apple_images, self._screen))
            self._apple_list[-1].set_animation(0, 2, 1, True)
    
    
    def draw(self):
        for apple in self._apple_list:
            apple.draw()

    def get_apples(self):
        return self._apple_list
    
    def rm(self, apple):
        self._apple_list.remove(self._apple_list[apple])

def main_menu(screen, bg_surf, bg_rect, menu_screen_x, menu_screen_y, cell_cx, cell_cy, settings): 
    main = True
    while main:
        mouse_pos = pygame.mouse.get_pos()
        play_button = Button(count=3, pos_index=1, font=font, text='Play', screen=screen, state="link")
        settings_button = Button(3, 2, font, 'Settings', screen)
        exit_button = Button(3, 3, font, 'Exit', screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.pressed(mouse_pos):
                    (cell_cx, cell_cy) = settings.get_size()

                    screen = pygame.display.set_mode((cell_cx*cell_width, cell_cy*cell_height))
                    screen.fill((0, 0, 0))
                    main_game_loop(screen, menu_screen_x, menu_screen_y, cell_cx, cell_cy)
                if exit_button.pressed(mouse_pos):
                    main = False
                    print("bye bye")
                    pygame.quit()
                if settings_button.pressed(mouse_pos):
                    settings_menu(settings)

                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()


        screen.blit(bg_surf, bg_rect)
        play_button.draw()
        exit_button.draw()
        settings_button.draw()


        pygame.display.flip()
        clock.tick(FPS)

def main_game_loop(screen, menu_screen_x, menu_screen_y, cell_cx, cell_cy):
    tiles.spawn_tiles(cell_cx, cell_cy)
    alive = True
    fc = 0
    apple_count = settings.get_apple_count()
    input_num = 0
    movement = [(1, 0, 270)]
    eaten = False
    (cell_cx, cell_cy) = settings.get_size()
    speed = settings.get_speed()
    snake = Snake(movement, cell_width, cell_height, cell_cx, cell_cy, dir_x=1, dir_y=0, angle=270, screen=screen)
    apple = Apple(cell_width, cell_height, cell_cx, cell_cy, apple_count, screen)
    font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 14)
    score = 0
    score_text = font.render(str(score), True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(screen.get_width()/2, 20))

    while alive:
        apple.spawn_apple(snake.get_cell_poss())
        input_num = 0
        fc += 1

        for event in pygame.event.get(): # movement inputs
            if event.type == pygame.QUIT:
                alive = False
                pygame.quit()
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
        
        if not fc%speed:
            if eaten:
                snake.append_seg(new)
                eaten = False


            snake.step()

            for apple_sprite in apple.get_apples():
                if snake.cell_collide(apple_sprite):
                    apple.rm(apple.get_apples().index(apple_sprite))
                    new = snake.new_seg()
                    score += 1
                    eaten = True
            
            snake.check_rotation()       

            if snake.death_check():
                print("pjfjfjf")
                screen = pygame.display.set_mode((menu_screen_x, menu_screen_y))
                alive = False

        if snake.win_check():
            print("you won")


        tiles.tile(screen.get_width()/2, 0)
        tiles.tile((screen.get_width()/2)-1, 0)
        snake.draw()
        apple.draw()
        screen.blit(font.render(str(score), True, (0, 0, 0)), score_rect)

        pygame.display.flip()
        clock.tick(FPS)

def settings_menu(settings):
    settings.read_settings()
    font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', int(menu_screen_x/20))
    sizes_button = ["6x5", "10x7", "16x10"]
    sizes_game = [(6, 5), (10, 7), (16, 10)]
    speed_button = ["slow", "medium", "fast"]
    speed_game = [30, 20, 10]
    apples_button = ["1", "3", "5", "10"]
    apples_game = [1, 3, 5, 10]

    size_index = sizes_game.index(settings.get_size())
    speed_index = speed_game.index(settings.get_speed())
    apple_index = apples_game.index(settings.get_apple_count())
    size = Button(count=4, pos_index=1, font=font, text='size', screen=screen, state="multi", options=sizes_button, index=size_index)
    speed = Button(count=4, pos_index=2, font=font, text="Speed", screen=screen, state="multi", options=speed_button, index=speed_index)
    apples = Button(count=4, pos_index=3, font=font, text="Apple count", screen=screen, state="multi", options=apples_button, index=apple_index)
    back = Button(count=4, pos_index=4, font=font, text="back", screen=screen, state="link")
    settings_open = True

    while settings_open:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                size_index = size.pressed(mouse_pos)
                speed_index = speed.pressed(mouse_pos)
                apples_index = apples.pressed(mouse_pos)
                if back.pressed(mouse_pos):
                    settings.size = sizes_game[size_index]
                    settings.speed = speed_game[speed_index]
                    settings.apples = apples_game[apples_index]
                    settings.write_setting()
                    settings_open = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                
        screen.blit(bg_surf, bg_rect)

        size.draw()
        speed.draw()
        apples.draw()
        back.draw()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    settings = Settings(filename="settings.json")
    cell_cx, cell_cy = settings.get_size()

    clock = pygame.time.Clock()
    FPS = 60

    cell_width, cell_height = 40, 40



    fullscreen = False

    if fullscreen:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        if cell_cx > cell_cy:
            cell_width = pygame.display.Info().current_h / cell_cy
            cell_height = pygame.display.Info().current_h / cell_cy
        else:
            cell_width = pygame.display.Info().current_w / cell_cx
            cell_height = pygame.display.Info().current_w / cell_cx

    scr_x=cell_width*cell_cx ; scr_y=cell_width*cell_cy

    menu_screen_x, menu_screen_y = 1000, 700

    font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', int(menu_screen_x/12))


    pygame.display.set_caption('Snake game')

    screen = pygame.display.set_mode((menu_screen_x, menu_screen_y), pygame.SCALED | pygame.RESIZABLE, vsync=1)

    tiles = TileSpawn(cell_cx, cell_cy, cell_width, cell_height, screen)

    bg_surf = pygame.transform.scale(pygame.image.load('images\\main_gui\\bg.jpg').convert_alpha(), (screen.get_width(), screen.get_height()))
    bg_rect = bg_surf.get_rect(center=(screen.get_width()/2, screen.get_height()/2))


    main_menu(screen, bg_surf, bg_rect, menu_screen_x, menu_screen_y, cell_cx, cell_cy, settings)
    #main_game_loop(screen)
    #spawn_tiles()
    debug.dprint(1, "game quitting")

pygame.quit()