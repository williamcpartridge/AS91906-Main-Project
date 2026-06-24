# pylint: disable=no-member
# pylint: disable=invalid-name
import os # used for positioning the window at startup and faster file paths
import json
import random # for random apple positions and apple types
import pygame # module that the game runs on
from settings import Settings # settings class save/write
from button import Button # button class handle button drawing and presses
from mysprite import MySprite # sprite class handles drawing sprites and movement of entities
from imagelist import ImageList # gets images of an object eg. snake
from tilespawn import TileSpawn # draws the game board and updates cells that are altered
import debug
debug.DEBUG_LEVEL = 0

FPS = 60 # runs game at 60 fps

EXC = [ # excluded items for input boxes
    pygame.K_ESCAPE,
    pygame.K_LSHIFT,
    pygame.K_RSHIFT,
    pygame.K_LCTRL,
    pygame.K_RCTRL,
    pygame.K_BACKSPACE,
    pygame.K_LALT,
    pygame.K_RALT,
    pygame.K_TAB,
    pygame.K_F1,
    pygame.K_F2,
    pygame.K_F3,
    pygame.K_F4,
    pygame.K_F5,
    pygame.K_F6,
    pygame.K_F7,
    pygame.K_F8,
    pygame.K_F9,
    pygame.K_F10,
    pygame.K_F11,
    pygame.K_F12,
    pygame.K_RETURN,
    pygame.K_UP,
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_DOWN,
    pygame.K_CAPSLOCK,
    pygame.K_LMETA,
    pygame.K_SPACE,
    pygame.K_NUMLOCK,
    pygame.K_NUMLOCKCLEAR,
    pygame.K_DELETE,
]

INC = [
    pygame.K_0,
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9,
    pygame.K_q,
    pygame.K_w,
    pygame.K_r,
    pygame.K_e,
    pygame.K_t,
    pygame.K_y,
    pygame.K_u,
    pygame.K_i,
    pygame.K_o,
    pygame.K_p,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_f,
    pygame.K_g,
    pygame.K_h,
    pygame.K_j,
    pygame.K_k,
    pygame.K_l,
    pygame.K_z,
    pygame.K_x,
    pygame.K_c,
    pygame.K_v,
    pygame.K_b,
    pygame.K_n,
    pygame.K_m,
    pygame.KSCAN_APOSTROPHE,
    pygame.K_EXCLAIM,
    pygame.K_AT,
    pygame.K_HASH,
    pygame.K_DOLLAR,
    pygame.K_PERCENT,
    pygame.K_POWER,
    pygame.K_ASTERISK,
    pygame.K_RIGHTBRACKET,
    pygame.K_LEFTBRACKET,
    pygame.K_MINUS,
    pygame.K_PLUS,
    pygame.K_EQUALS,
    pygame.K_UNDERSCORE,
    pygame.K_GREATER,
    pygame.K_LESS,
    pygame.K_COMMA,
    pygame.K_PERIOD,
]

class Snake():
    """Snake class handles snake movement and segment management"""
    def __init__(self, movement, cell_w, cell_h, cell_cx, cell_cy, dir_x, dir_y, angle, canvas):
        """initiating variables for the snake class"""
        self._movement = movement
        self._cell_w = cell_w
        self._cell_h = cell_h
        self._cell_cx = cell_cx
        self._cell_cy = cell_cy
        self._canvas = canvas
        self._dir_x = dir_x
        self._dir_y = dir_y
        self._angle = angle
        self._add_segment = False

        self._snake_head_img = ImageList("images\\snake\\head\\snake_head", cell_width, cell_height) # gets list of images for snake head
        self._snake_body_img = ImageList("images\\snake\\body\\snake_body", cell_width, cell_height) # gets list of images for snake body

        snake_x = self._cell_w+(self._cell_w/2)
        snake_y = self._cell_h/2
        self._segments = [MySprite(snake_x, snake_y, self._cell_w, self._cell_h, self._snake_head_img, self._canvas, self._angle), \
                MySprite(snake_x - self._cell_w, snake_y, self._cell_w, self._cell_h, self._snake_body_img, self._canvas, self._angle)] # creates starting list of snake segments with mysprite objects

    def get_head_pos(self): 
        """returns the (x, y) position of the snakes head"""
        return (self._segments[0].get_x(), self._segments[0].get_y())
    
    def get_cell_poss(self): 
        """get the cell that each snake segment is in"""
        temp = []
        for seg in self._segments:
            temp.append((self.get_cell_x(seg.get_x()), self.get_cell_y(seg.get_y())))
        #debug.dprint(2, temp)
        return temp

    def get_cell_x(self, x):
        """get the x position of a snake seg"""
        return int(x/self._cell_w)

    def get_cell_y(self, y):
        """get the y position of a snake seg"""
        return int(y/self._cell_h)
    
    def set_dir_x(self, dir_x): 
        """set the x part of the direction vector for the snake"""
        self._dir_x = dir_x
    
    def get_dir_x(self):
        """get the x part of the direction vector of the snake"""
        return self._dir_x

    def set_dir_y(self, dir_y):
        """set the y part of the direction vector for the snake"""
        self._dir_y = dir_y

    def get_dir_y(self):
        """get the y part of the direction vector of the snake"""
        return self._dir_y

    def set_angle(self, angle):
        """sets the direction the snake sprites are pointing"""
        self._angle = angle

    def get_angle(self):
        """gets the direction the snake sprites are pointing"""
        return self._angle

    def set_movement(self, dir_x, dir_y, angle):
        """sets the direction vector and angle of the snake"""
        self.set_dir_x(dir_x)
        self.set_dir_y(dir_y)
        self.set_angle(angle)

    def get_movement(self): # gets the direction vector and angle of the snake
        return (self.get_dir_x(), self.get_dir_y(), self.get_angle())

    def step(self): # handles what happens when the snake steps forward
        tiles.tile(self._segments[-2].get_x(), self._segments[-2].get_y()) # replaces the tiles that have been affected
        tiles.tile(self._segments[-1].get_x(), self._segments[-1].get_y())
        tiles.tile(self._segments[0].get_x(), self._segments[0].get_y())

        self._movement.insert(0, self.get_movement())
        if len(self._movement) > len(self._segments): # removes last segment
            self._movement.pop()
        for i in range(len(self._segments)): # sets the rotation of the snake segments
            if i == len(self._segments) -1:
                self._segments[i].rotate(self._movement[i-1][2])
            else:
                self._segments[i].rotate(self._movement[i][2])

            self._segments[i].move(self._cell_w*self._movement[i][0], self._cell_h*self._movement[i][1])

    def cell_collide(self, obj): # checks for collision with another object
        if self.get_cell_x(self._segments[0].get_x()) == self.get_cell_x(obj.get_x()) and \
            self.get_cell_y(self._segments[0].get_y()) == self.get_cell_y(obj.get_y()):
            return True

    def new_seg(self): # creates and new snake segment to be added to the list
        new = MySprite(self._segments[-1].get_x() - self._movement[-1][0]*self._cell_w, \
                       self._segments[-1].get_y() - self._movement[-1][1]*self._cell_h, \
                        self._cell_w, self._cell_h, self._snake_body_img, self._canvas)
        new.rotate(self._movement[-1][2])
        new.set_frame(0)
        return new

    def append_seg(self, new): # adds the new segment to the snake list
        self._segments.append(new)
        

    def check_rotation(self): # handles the rotation of every snake segment
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

    def death_check(self): # handles all death cases. collision with self, collision with wall
        for segment in self._segments:
            if segment != self._segments[0]:
                if self.cell_collide(segment):
                    return True
            
        if self._segments[0].get_x() < self._cell_w/2 or self._segments[0].get_x() > self._canvas.get_width() - self._cell_w/2 or \
            self._segments[0].get_y() < self._cell_h/2 or self._segments[0].get_y() > self._canvas.get_height() - self._cell_h/2:
            return True
        
    def start(self): # starts the movement of the first snake segments
        for segment in self._segments:
            segment.move(cell_width, 0, 0.1)

    def win_check(self): # checks if the player has filled the game board
        if len(self._segments) == self._cell_cx*self._cell_cy:
            return True
        else:
            return False

    def draw(self): # draws each snake segment to the screen
        for seg in self._segments:
            seg.draw()

class Apple(): 
    """Handles spwing apples and buffs for apple types"""
    def __init__(self, cell_w, cell_h, cell_cx, cell_cy, apple_count, canvas):  # initiating variables for the apple class
        self._cell_w = cell_w
        self._cell_h = cell_h
        self._cell_cx = cell_cx
        self._cell_cy = cell_cy
        self._apple_list = []
        self._apple_count = apple_count
        self._canvas = canvas
        self._apple_images = ImageList("images\\apple\\apple", cell_width, cell_height)
        self._upgrades = {"Golden": (True, 1), "Boost": (True, 2)}
        self._type_list = []


    def spawn_apple(self, snake_cells): # handles the spawning of the apples
        if len(self._apple_list) < self._apple_count and ((self._cell_cx*self._cell_cy) - len(snake_cells)) > self._apple_count: # checks of an apples is needed
            done = False
            type = self.apple_type() # gets the type of apple (normal, golden, boost)
            while not done: # choses random position for the apple
                cell_x = random.randint(0, self._cell_cx - 1) 
                cell_y = random.randint(0, self._cell_cy - 1)
                done = True
            
                if (cell_x, cell_y) in snake_cells: # checks if cell is occupied by snake
                    done = False

                for a in self._apple_list: # chekc if cell is occupied by apple
                    ax = int(a.get_x() / self._cell_w)
                    ay = int(a.get_y() / self._cell_h)

                    if (cell_x, cell_y) == (ax, ay):
                        done = False

            debug.dprint(2, (cell_x, cell_y))
            # adds the apple to the list
            ax = cell_x * self._cell_w + self._cell_w / 2
            ay = cell_y * self._cell_h + self._cell_h / 2
            self._apple_list.append(MySprite(ax, ay, self._cell_w, self._cell_h, self._apple_images, self._canvas))
            self._type_list.append(type)

            #self._apple_list[-1].set_animation(0, 1, 1, False)

    def apple_type(self): # choses random apple type
        for upgrade in self._upgrades.keys():
            if self._upgrades[upgrade][0]:
                if random.randint(1, 5) == 5:
                    return upgrade
        return "Normal"
    
    def draw(self): # draws all apples to the screen
        for i in range(len(self._apple_list)):
            if self._type_list[i] == "Normal":
                self._apple_list[i].set_frame(0)
            else:
                self._apple_list[i].set_frame(self._upgrades[self._type_list[i]][1])

            self._apple_list[i].draw()
            

    def get_apples(self): # returns the list of apples on screen
        return self._apple_list
    
    def get_type(self): # returns every type in apple list
        return self._type_list
    
    def rm(self, apple): # removes an apple from the apple sprites list and type list
        self._apple_list.pop(apple)
        self._type_list.pop(apple)

class LeaderBoard(): 
    """handles the reading and writing to the leaderboard files"""
    def __init__(self, filename, canvas):  # initiating variables for the leaderboard class
        self._filename = filename
        self._leaderboard = {}
        self.read_leaderboard()
        self._canvas = canvas

    def write_leaderboard(self, score, size, username): # handles writing scores to the leaderboard
        # checks for size/catagory
        if size == (6, 5):
            size = "small"
        elif size == (10, 7):
            size = "medium"
        elif size == (16, 11):
            size = "large"
        else:
            size = "custom"
        
        # checks if score is valid
        if username != None and username != "":
            if username in self._leaderboard[size]:     
                if score > self._leaderboard[size][username]:
                    self._leaderboard[size][username] = score
                    self.write_json(self._filename, self._leaderboard)
            else:
                self._leaderboard[size][username] = score
                self.write_json(self._filename, self._leaderboard)

    def write_json(self, filename, obj): # writes and sorts the scores to leaderboard file
        sorted_obj = {}

        for size, board in obj.items():
            sorted_obj[size] = dict(sorted(board.items(), key=lambda item: item[1], reverse=True))

        with open(filename, 'w') as f:
            json.dump(sorted_obj, f, indent=4)

        debug.dprint(1, "Data written successfully")
        debug.dprint(1, sorted_obj)

    def read_leaderboard(self): # gets the scores for the leaderboard
        self._leaderboard = self.json_read(self._filename)

    def json_read(self, filename): # reads the scores from the leaderboard file
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                debug.dprint(1, "Data read successfully:")
                debug.dprint(1, data)
                return data
        except FileNotFoundError: # ensures the game doesnt crash if the file does not exist
            print("No leaderboard file found, creating new one.")
            return {}
        
    def change_user(self, size, user, prev_user):

        if size == (6, 5):
            size = "small"
        elif size == (10, 7):
            size = "medium"
        elif size == (16, 11):
            size = "large"
        else:
            size = "custom"
        
        # checks if score is valid
        if prev_user in self._leaderboard[size]:     
            self._leaderboard[size][user] = self._leaderboard[size][prev_user]
            del self._leaderboard[size][prev_user]
            self.write_json(self._filename, self._leaderboard)

def get_scaled_mouse_pos(screen_x, screen_y): 
    """Scales mouse position"""
    scale = min(screen_x / LOGICAL_X, screen_y / LOGICAL_Y)

    offset_x = (screen_x - LOGICAL_X * scale) // 2
    offset_y = (screen_y - LOGICAL_Y * scale) // 2

    mx, my = pygame.mouse.get_pos()

    return (
        (mx - offset_x) / scale,
        (my - offset_y) / scale
    )

def main_menu(canvas, screen, bg_surf, bg_rect, cell_cx, cell_cy, settings, username, screen_x, screen_y, score): 
    """menu loop containing options to play edit settings or qiot the game"""
    global main_running # this is global to use as a cascading exit
    global username_set
    global change
    global name
    change = True
    fc = 0

    menu_channel.unpause()

    def play():
        (cx, cy) = settings.get_size()
        screen.fill((0, 0, 0))
        game_canvas = pygame.Surface((cx * cell_width, cy * cell_height))
        start.play()
        menu_channel.pause()
        game_channel.play(game_music, loops=-1)
        game_channel.unpause()
        main_game_loop(game_canvas, screen, cx, cy, username, score, screen_x, screen_y)

    def open_settings():
        click.play()
        settings_menu(canvas, screen, screen_x, screen_y)

    def open_leaderboard():
        menu_channel.pause()
        leaderboard_channel.unpause()
        leaderboard.read_leaderboard()
        click.play()
        leaderboard_menu(canvas, screen, leaderboard, screen_x, screen_y, score)

    def quit_game():
        global main_running
        main_running = False
        exit.play()
        print("bye bye")

    def change_username():
        global username_set
        global change
        click.play()
        username_set = True
        change = False

    def change_user():
        global username_set
        global change
        global name
        click.play()
        username_set = True
        change = True
        name = ""

    button_list = [
        Button(count=3, pos_index=1, font=font, text='Play', screen=canvas, state="link", func=play),
        Button(count=3, pos_index=2, font=font, text='Settings', screen=canvas, state="link", func=open_settings),
        Button(count=3, pos_index=3, font=font, text='Exit', screen=canvas, state="link", func=quit_game),
        Button(x=170, y=40, font=pygame.font.Font('fonts/PressStart2P-Regular.ttf', 20),
               text="Leader Board", screen=canvas, state="link", func=open_leaderboard),
        Button(x=canvas.get_width() + 170, y=40, font=pygame.font.Font('fonts/PressStart2P-Regular.ttf', 20),
               text="change username", screen=canvas, state="link", func=change_username),
        Button(x=canvas.get_width() - 170, y=100, font=pygame.font.Font('fonts/PressStart2P-Regular.ttf', 20),
               text="change user", screen=canvas, state="link", func=change_user),
    ]

    name = ""
    user_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 14)
    dis_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 40)
    dis_text = dis_font.render('USERNAME:', True, (255, 255, 255))
    text_rect = pygame.Rect((canvas.get_width()/2 - dis_text.get_width()/2), (canvas.get_height()/4 - dis_text.get_height()/2), 200, 50)
    # the box for the username enter box
    user_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
    user_surf.fill((255, 255, 255, 180))
    user_rect = user_surf.get_rect(center=(canvas.get_width()/2, canvas.get_height()/2))
    # text for user name enter box
    user_text = user_font.render(name, True, (0, 0, 0))
    user_text_rect = user_text.get_rect(center=user_rect.center)

    username_text = user_font.render(username, True, (0, 0, 0))
    info_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 11)
    info_text = info_font.render('Enter you prefered display name or press enter to runn as guest.\n\n        (Warning guest mode with not save highscore!)', True, (255, 255, 255))
    info_rect = info_text.get_rect(center=(canvas.get_width()/2, canvas.get_height()/2 - info_text.get_height()*2))
    
    while main_running:
        fc += 1
        mouse_pos = get_scaled_mouse_pos(screen_x, screen_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_running = False
                pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                (screen_x, screen_y) = event.size 
                if fullscreen:
                    screen = pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not username_set:
                    for button in button_list:
                        if button.pressed(mouse_pos):
                            func = button.get_func()
                            if func:
                                func()
            if event.type == pygame.KEYDOWN:
                key.play()
                if event.key == pygame.K_ESCAPE:
                    main_running = False
                if username_set:
                    info_text = info_font.render('Enter you prefered display name or press enter to runn as guest.\n\n        (Warning guest mode with not save highscore!)', True, (255, 255, 255))
                    if event.key in INC:
                        if len(name) <= 19:
                            name = f"{name}{pygame.key.name(event.key)}"
                        else:
                            info_text = info_font.render('Warning: username is too long! maximum lenth is 20 characters', True, (255, 255, 255))
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        username_set = False
                        prev_user = username
                        username = name
                        user_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 40)
                        username_text = user_font.render(username, True, (255, 255, 255))
                        if prev_user != None and not change:
                            leaderboard.change_user(settings.get_size(), username, prev_user)
                    elif event.key == pygame.K_ESCAPE:
                        username_set = False
                        username = None

        canvas.blit(bg_surf, bg_rect)

        if username_set:

            user_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 14)
            if (fc // 20) % 2 == 0:
                user_text = user_font.render(f'{name}|', True, (0, 0, 0))
            else:
                user_text = user_font.render(f'{name} ', True, (0, 0, 0))
            user_text_rect = user_text.get_rect(center=user_rect.center)
            if user_text_rect.w > user_surf.get_width():
                user_surf = pygame.Surface((user_text_rect.w, 50), pygame.SRCALPHA)

            canvas.blit(user_surf, user_rect)
            canvas.blit(user_text, user_text_rect)
            canvas.blit(dis_text, text_rect)
            canvas.blit(info_text, info_rect)
        else:
            canvas.blit(username_text, (canvas.get_width()/2 - (username_text.get_width()/2), 40))
            for button in button_list:
                button.update(mouse_pos)
                button.draw()

        scale = min(screen_x / LOGICAL_X, screen_y / LOGICAL_Y)

        scaled_canvas = pygame.transform.scale(canvas, (LOGICAL_X * scale, LOGICAL_Y * scale))

        offset_x = (screen_x - LOGICAL_X * scale) // 2
        offset_y = (screen_y - LOGICAL_Y * scale) // 2

        screen.blit(scaled_canvas, (offset_x, offset_y))

        pygame.display.flip()
        clock.tick(FPS)

def main_game_loop(canvas, screen, cell_cx, cell_cy, username, score, screen_x, screen_y): # game loop handles inputs and talks to snake and apple clases to run the game
    global main_running
    time = 0
    tiles.spawn_tiles(cell_cx, cell_cy, canvas)
    alive = True
    fc = 0
    apple_count = settings.get_apple_count()
    input_num = 0
    movement = [(1, 0, 270)]
    eaten = False
    (cell_cx, cell_cy) = settings.get_size()
    speed = settings.get_speed()
    snake = Snake(movement, cell_width, cell_height, cell_cx, cell_cy, dir_x=1, dir_y=0, angle=270, canvas=canvas)
    apple = Apple(cell_width, cell_height, cell_cx, cell_cy, apple_count, canvas)
    font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 14)
    score_text = font.render(str(score), True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(canvas.get_width()/2, 20))

    while alive:
        apple.spawn_apple(snake.get_cell_poss())
        input_num = 0
        fc += 1

        for event in pygame.event.get(): # movement inputs
            if event.type == pygame.QUIT:
                alive = False
                main_running = False
            if event.type == pygame.VIDEORESIZE:
                (screen_x, screen_y) = event.size 
                if fullscreen:
                    screen = pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit.play()
                    alive = False
                    canvas = pygame.display.set_mode((LOGICAL_X, LOGICAL_Y))
                if input_num == 0:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        if movement[0][2] != 180 and movement[0][2] != 0:
                            turn.play()
                            snake.set_movement(0, -1, 0)
                            input_num = 1
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if movement[0][2] != 180 and movement[0][2] != 0:
                            turn.play()
                            snake.set_movement(0, 1, 180)
                            input_num = 1
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if movement[0][2] != 270 and movement[0][2] != 90:
                            turn.play()
                            snake.set_movement(1, 0, 270)
                            input_num = 1
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if movement[0][2] != 270 and movement[0][2] != 90:
                            turn.play()
                            snake.set_movement(-1, 0, 90)
                            input_num = 1
        
        if not fc%speed:
            if eaten:
                snake.append_seg(new)
                eaten = False
        
            if time > 0 :
                time -= 1
            elif time == 0:
                speed = settings.get_speed()

            snake.step()

            for apple_sprite in apple.get_apples():
                if snake.cell_collide(apple_sprite):
                    i = apple.get_apples().index(apple_sprite)

                    upgrade = apple.get_type()[i]

                    apple.rm(i)

                    new = snake.new_seg()
                    eaten = True

                    if upgrade != "Normal":
                        if upgrade == "Golden":
                            golden.play()
                            score += 5

                        elif upgrade == "Boost":
                            boost.play()
                            speed = 10
                            time = 30

                    else:
                        normal.play()
                        score += 1
            
            snake.check_rotation()       

            if snake.death_check():
                leaderboard.write_leaderboard(score, settings.get_size(), username)
                die.play()
                game_channel.pause()
                menu_channel.unpause()
                alive = False

        if snake.win_check():
            alive = False
            main_game_loop(canvas, screen, cell_cx, cell_cy, username, score, screen_x, screen_y)


        tiles.tile(canvas.get_width()/2, 0)
        tiles.tile((canvas.get_width()/2)-1, 0)
        snake.draw()
        apple.draw()
        canvas.blit(font.render(str(score), True, (0, 0, 0)), score_rect)

        scale = min(screen_x / canvas.get_width(), screen_y / canvas.get_height())

        scaled_w = int(canvas.get_width() * scale)
        scaled_h = int(canvas.get_height() * scale)

        scaled_canvas = pygame.transform.scale(canvas, (scaled_w, scaled_h))

        offset_x = (screen_x - scaled_w) // 2
        offset_y = (screen_y - scaled_h) // 2

        screen.blit(scaled_canvas, (offset_x, offset_y))

        pygame.display.flip()
        clock.tick(FPS)

def settings_menu(canvas, screen, screen_x, screen_y): # displays settings that you can edit
    global main_running
    settings.read_settings()
    font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', int(LOGICAL_X/20))
    sizes_button = ["Small", "Medium", "Large", "Custom"]
    sizes_game = [(6, 5), (10, 7), (16, 11)]
    speed_button = ["slow", "medium", "fast"]
    speed_game = [30, 20, 10]
    apples_button = ["1", "3", "5", "10"]
    apples_game = [1, 3, 5, 10]

    key = None
    width_val, height_val = settings.get_size()

    if settings.get_size() in sizes_game:
        size_index = sizes_game.index(settings.get_size())
    else:
        size_index = 3
    speed_index = speed_game.index(settings.get_speed())
    apple_index = apples_game.index(settings.get_apple_count())
    size = Button(count=5, pos_index=1, font=font, text='size', screen=canvas, state="multi", options=sizes_button, index=size_index)
    speed = Button(count=5, pos_index=3, font=font, text="Speed", screen=canvas, state="multi", options=speed_button, index=speed_index)
    apples = Button(count=5, pos_index=4, font=font, text="Apple count", screen=canvas, state="multi", options=apples_button, index=apple_index)
    back = Button(count=5, pos_index=5, font=font, text="back", screen=canvas, state="link")
    width = Button(x=(canvas.get_width()/2)-100, count=5, pos_index=2, font=pygame.font.Font('fonts/PressStart2P-Regular.ttf', 14), text="Width: ", screen=canvas, state="input", value=width_val)
    height = Button(x=(canvas.get_width()/2)+100, count=5, pos_index=2, font=pygame.font.Font('fonts/PressStart2P-Regular.ttf', 14), text="Height: ", screen=canvas, state="input", value=height_val)
    settings_open = True

    while settings_open:
        mouse_pos = get_scaled_mouse_pos(screen_x, screen_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_open = False
                main_running = False
            if event.type == pygame.VIDEORESIZE:
                (screen_x, screen_y) = event.size 
                if fullscreen:
                    screen = pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click.play()
                size_index = size.pressed(mouse_pos)
                speed_index = speed.pressed(mouse_pos)
                apples_index = apples.pressed(mouse_pos)
                if not width.pressed(mouse_pos):
                    width._input_active = False
                if not height.pressed(mouse_pos):
                    height._input_active = False
                if back.pressed(mouse_pos):
                    exit.play()
                    if size_index != 3:
                        settings.size = sizes_game[size_index]
                    else:
                        if width._value > Settings.MAX_ACCROSS:
                            width._value = Settings.MAX_ACCROSS
                        elif width._value < Settings.MIN_ACCROSS:
                            width._value = Settings.MIN_ACCROSS
                        if height._value > Settings.MAX_ACCROSS:
                            height._value = Settings.MAX_ACCROSS
                        elif height._value < Settings.MIN_ACCROSS:
                            height._value = Settings.MIN_ACCROSS
                        settings.size = (width.get_val(), height.get_val())
                    settings.speed = speed_game[speed_index]
                    settings.apples = apples_game[apples_index]
                    settings.write_setting()
                    settings_open = False
            if size_index == 3:
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit():
                        key = int(event.unicode)
                    elif event.key == pygame.K_BACKSPACE:
                        key = -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_open = False
                
        canvas.blit(bg_surf, bg_rect)

        size.update(mouse_pos)  
        size.draw()
        speed.update(mouse_pos)
        speed.draw()
        apples.update(mouse_pos)
        apples.draw()
        back.update(mouse_pos)
        back.draw()

        if size_index == 3:
            width.update(mouse_pos, num=key)
            width.draw()
            height.update(mouse_pos, num=key)
            height.draw()
            key = None

        scale = min(screen_x / LOGICAL_X, screen_y / LOGICAL_Y)

        scaled_canvas = pygame.transform.scale(canvas, (LOGICAL_X * scale, LOGICAL_Y * scale))

        offset_x = (screen_x - LOGICAL_X * scale) / 2
        offset_y = (screen_y - LOGICAL_Y * scale) / 2

        screen.blit(scaled_canvas, (offset_x, offset_y))

        pygame.display.flip()
        clock.tick(FPS)

def leaderboard_menu(canvas, screen, leaderboard_obj, screen_x, screen_y, score): # displays the leaderboard
    font_title = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 40)
    font_text = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 25)
    font_text_small = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 18)
    font_back = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 30)

    back_button = Button(y=canvas.get_height()-70, x=canvas.get_width()/2, pos_index=1, font=font_back, text="Back", screen=canvas, state="link")

    running = True
    while running:
        mouse_pos = get_scaled_mouse_pos(screen_x, screen_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                (screen_x, screen_y) = event.size 
                if fullscreen:
                    screen = pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.pressed(mouse_pos):
                    exit.play()
                    leaderboard_channel.pause()
                    menu_channel.unpause()
                    running = False

        canvas.fill((20, 20, 20))

        title = font_title.render("LEADERBOARD", True, (255, 255, 255))
        canvas.blit(title, (canvas.get_width()//2 - title.get_width()//2, 20))

        y_offset = 120
        x_offset = 0

        data = leaderboard_obj._leaderboard

        if not data:
            empty = font_text.render("No scores yet", True, (200, 200, 200))
            canvas.blit(empty, (canvas.get_width()//2 - empty.get_width()//2, y_offset))

        else:
            for size in ["small", "medium", "large", "custom"]:
                if size in data:
                    header = font_text.render(size.upper(), True, (255, 200, 100))
                    canvas.blit(header, (60+x_offset, y_offset))
                    y_offset += 40

                    for i, (player, score) in enumerate(data[size].items()):
                        text = font_text_small.render(f"{i+1}. {player} - {score}", True, (255, 255, 255))
                        canvas.blit(text, (80+x_offset, y_offset))
                        y_offset += 30

                    y_offset = 120
                    x_offset += 320

        back_button.update(mouse_pos)
        back_button.draw()

        scale = min(screen_x / LOGICAL_X, screen_y / LOGICAL_Y)

        scaled_canvas = pygame.transform.scale(canvas, (LOGICAL_X * scale, LOGICAL_Y * scale))

        offset_x = (screen_x - LOGICAL_X * scale) // 2
        offset_y = (screen_y - LOGICAL_Y * scale) // 2

        screen.blit(scaled_canvas, (offset_x, offset_y))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__": # game initialisation
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30" # window positioning at (x=0, y=30)

    pygame.init()
    pygame.mixer.init()

    # These constants are initialized here because they depend on pygame being initialized first
    LOGICAL_X, LOGICAL_Y = pygame.display.Info().current_w/1.5, (pygame.display.Info().current_h-30)/1.5 # logical screen size this is what the game sees

    settings = Settings(filename="settings.json") # initiates settings class
    cell_cx, cell_cy = settings.get_size() # number of cells 

    clock = pygame.time.Clock()

    username = None
    username_set = True

    score = 0
    
    cell_width, cell_height = 40, 40 # width and height of an idividual cell

    screen_x, screen_y = pygame.display.Info().current_w, pygame.display.Info().current_h - 30 # real screen size this is what is displayed

    font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 75)

    #sound init
    click = pygame.mixer.Sound('sounds/click.mp3')
    die = pygame.mixer.Sound('sounds/die.mp3')
    eat = pygame.mixer.Sound('sounds/eat.mp3')
    golden = pygame.mixer.Sound('sounds/golden.mp3')
    key = pygame.mixer.Sound('sounds/key.mp3')
    start = pygame.mixer.Sound('sounds/start.mp3')
    boost = pygame.mixer.Sound('sounds/boost.mp3')
    exit = pygame.mixer.Sound('sounds/exit.mp3')
    normal = pygame.mixer.Sound('sounds/normal.mp3')
    level_up = pygame.mixer.Sound('sounds/level up.mp3')
    turn = pygame.mixer.Sound('sounds/turn.mp3')

    menu_music = pygame.mixer.Sound('music/menu_music.mp3')
    game_music = pygame.mixer.Sound('music/game_music.mp3')
    leaderboard_music = pygame.mixer.Sound('music/and now Im going to try to sing opera and Im going to do the best as I can.mp3')

    menu_channel = pygame.mixer.Channel(0)
    game_channel = pygame.mixer.Channel(1)
    leaderboard_channel = pygame.mixer.Channel(2)

    menu_channel.play(menu_music, loops=-1)
    menu_channel.pause()
    game_channel.play(game_music, loops=-1)
    game_channel.set_volume(0.5)
    game_channel.pause()
    leaderboard_channel.play(leaderboard_music, loops=-1)
    leaderboard_channel.pause()

    pygame.display.set_caption('Snake game')

    canvas = pygame.Surface((LOGICAL_X, LOGICAL_Y)) # serface the game sees

    fullscreen = False

    if fullscreen: # handles fullscreen or resizeable
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        screen = pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)

    leaderboard = LeaderBoard("leaderboard.json", canvas) # initiates the leaderboard class
    tiles = TileSpawn(cell_cx, cell_cy, cell_width, cell_height, canvas) # initiates the TileSpawn class 

    bg_surf = pygame.transform.scale(pygame.image.load('images\\main_gui\\bg.jpg').convert_alpha(), (canvas.get_width(), canvas.get_height())) # creates and sizes the background image for main menu and settings
    bg_rect = bg_surf.get_rect(center=(canvas.get_width()/2, canvas.get_height()/2))

    main_running = True # making this global to enable cascading exit
    main_menu(canvas, screen, bg_surf, bg_rect, cell_cx, cell_cy, settings, username, screen_x, screen_y, score) # start the program
    debug.dprint(1, "game quitting")

pygame.quit()