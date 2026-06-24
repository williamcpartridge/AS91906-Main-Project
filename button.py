import pygame
import math
from settings import Settings

class Button():
    DEFAULT_TEXT_COLOR = (255, 255, 255)
    DEFAULT_BG_COLOR = (200, 200, 200, 150)
    BORDER_WIDTH, BORDER_HEIGHT = 35, 20
    def __init__(self, font=None, text="", screen=None, state="link", func=None, options=None, index=0, count=None, pos_index=None, x=None, y=None, value=5):
        pygame.init()

        self._func = func
        self._screen = screen
        self._font = font
        self._text_input = text
        self._in_hovered = False
        self._text = self._font.render(self._text_input, True, Button.DEFAULT_TEXT_COLOR)

        # input state variables
        self._value = value
        self._input_active = False

        self._state = state
        self._index = index
        if options != None:
            self._options = options
        if self._state == "link":
            self.link()
        if self._state == "multi":
            self.multi()
        if self._state == "input":
            self.input()

        self._bg_width, self._bg_height = self._text.get_width() + Button.BORDER_WIDTH, self._text.get_height() + Button.BORDER_WIDTH

        if count != None and index != None: # this needs fixing checks for valid x and y
            if x != None:
                self._x = x
            else:
                self._x = self._screen.get_width()/2

            self._y = (2*pos_index)*(self._screen.get_height()/(((count+1)*2)))

        elif x != None and y != None:
            if x > self._screen.get_width() - self._bg_width/2:
                self._x = self._screen.get_width() - self._bg_width/2
            elif x < self._bg_width/2:
                self._x = self._bg_width/2
            else:
                self._x = x

            if y > self._screen.get_height() - self._bg_height/2:
                self._y = self._screen.get_height() - self._bg_height/2
            elif y < self._bg_height:
                self._y = self._bg_height/2
            else:
                self._y = y
        else:
            print("NO VALID POSITIONAL VARIABLES!")

        self._text_rect = self._text.get_rect(center=(self._x, self._y))
        self._bg_surface = pygame.Surface((self._bg_width, self._bg_height), pygame.SRCALPHA)
        self._bg_rect = self._bg_surface.get_rect(center=(self._x, self._y))
        self._draw_rect = self._bg_rect.copy()

        self._bob_intensity = 0.0
        self._transition_speed = 0.1
        self._bob_range = 5    
        self._bob_speed = 0.007     
        
    def get_func(self):
        return self._func

    def update(self, mouse_pos, num=None):
        self._is_hovered = self._bg_rect.collidepoint(mouse_pos)

        if self._state == "input":
            if num != None and self._input_active:
                if self._value != 0:
                    if num == -1 and len(str(self._value)) > 1:
                        self._value = str(self._value)
                        self._value = self._value[:-1]
                        self._value = int(self._value)
                    elif num == -1 and len(str(self._value)) == 1:
                        self._value = 0
                    elif num != -1:
                        self._value = int(f'{str(self._value)}{num}')
                elif num != -1:
                    self._value = num
            if self._value > Settings.MAX_ACCROSS and self._input_active == False:
                self._value = Settings.MAX_ACCROSS
            elif self._value < Settings.MIN_ACCROSS and self._input_active == False:
                self._value = Settings.MIN_ACCROSS
            self.input()

        target_intensity = 1.0 if self._is_hovered else 0.0
        self._bob_intensity += (target_intensity - self._bob_intensity) * self._transition_speed

        ticks = pygame.time.get_ticks()
        raw_bob = math.sin(ticks * self._bob_speed) * self._bob_range

        scale = 1 + (0.08 * self._bob_intensity)

        width = (self._text_rect.width + 35) * scale
        height = (self._text_rect.height + 20) * scale

        self._draw_rect = pygame.Rect(0, 0, width, height)
        self._draw_rect.center = (self._x, self._y + raw_bob * self._bob_intensity)

    def link(self):
        self._text = self._font.render(self._text_input, True, Button.DEFAULT_TEXT_COLOR)

    def multi(self):
        self._text = self._font.render(f"{self._text_input}: {self._options[self._index]}", True, Button.DEFAULT_TEXT_COLOR)

    def input(self):
        self._text = self._font.render(f"{self._text_input}{self._value}", True, Button.DEFAULT_TEXT_COLOR)

    def get_val(self):
        return self._value

    def draw(self):
        #self.update(pygame.mouse.get_pos())
        self._bg_surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height), pygame.SRCALPHA)

        self._bg_surface.fill(Button.DEFAULT_BG_COLOR)
        self._screen.blit(self._bg_surface, self._draw_rect)

        self._text_rect = self._text.get_rect(center=self._draw_rect.center)
        self._screen.blit(self._text, self._text_rect)

    def pressed(self, position):
        rect = self._draw_rect

        if self._state == "link":
            return rect.collidepoint(position)

        elif self._state == "multi":
            if rect.collidepoint(position):

                if self._index < len(self._options) - 1:
                    self._index += 1
                else:
                    self._index = 0

                self.multi()

            return self._index
        
        elif self._state == "input":
            if rect.collidepoint(position):
                if self._input_active:
                    self._input_active = False
                else:
                    self._input_active = True
            return rect.collidepoint(position)