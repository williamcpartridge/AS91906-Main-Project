import pygame
import math

class Button():
    def __init__(self, font=None, text="", screen=None, state="link", options=None, index=0, count=None, pos_index=None, x=0, y=0):
        if count != None:
            self._x = screen.get_width()/2
            self._y = (2*pos_index)*(screen.get_height()/(((count+1)*2)))
        else:
            self._x = x
            self._y = y
        self._screen = screen
        self._font = font
        self._text_input = text
        self._in_hovered = False

        self._state = state
        self._index = index
        if options != None:
            self._options = options
        if self._state == "link":
            self.link()
        if self._state == "multi":
            self.multi()

        self._text_rect = self._text.get_rect(center=(self._x, self._y))
        self._bg_surface = pygame.Surface((self._text_rect.width + 35, self._text_rect.height + 20), pygame.SRCALPHA)
        self._bg_rect = self._bg_surface.get_rect(center=(self._x, self._y))
        self._draw_rect = self._bg_rect.copy()

        self._bob_intensity = 0.0
        self._transition_speed = 0.1
        self._bob_range = 5    
        self._bob_speed = 0.007     
        

    def update(self, mouse_pos):
        self._is_hovered = self._bg_rect.collidepoint(mouse_pos)

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
        self._text = self._font.render(self._text_input, True, (255, 255, 255))

    def multi(self):
        self._text = self._font.render(f"{self._text_input}: {self._options[self._index]}", True, (255, 255, 255))

    def draw(self):
        self.update(pygame.mouse.get_pos())
        self._bg_surface = pygame.Surface((self._draw_rect.width, self._draw_rect.height), pygame.SRCALPHA)

        self._bg_surface.fill((200, 200, 200, 150))
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
