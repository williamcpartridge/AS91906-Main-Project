import pygame

class Button():
    def __init__(self, x=None, y=None, count=None, pos_index=None, font=None, text=None, screen=None, state="link", options=None, index=0):
        if count != None:
            self._x = screen.get_width()/2
            self._y = (2*pos_index)*(screen.get_height()/(((count+1)*2)))
        elif x != None and y != None:
            self._x = x
            self._y = y
        else:
            print("NO POSITION SET!\n   DEFULT SET: (0, 0)")
            self._x = 0
            self._y = 0
        self._screen = screen
        self._font = font
        self._text_input = text

        self._state = state
        self._index = index
        if options != None:
            self._options = options
        if self._state == "link":
            self.link()
        if self._state == "multi":
            self.multi()

    def link(self):
        self._text = self._font.render(self._text_input, True, (255, 255, 255))
        self._text_rect = self._text.get_rect(center=(self._x, self._y))
        self._bg_surface = pygame.Surface((self._text_rect.width + 35, self._text_rect.height + 20), pygame.SRCALPHA)
        self._bg_rect = self._bg_surface.get_rect(center=(self._x, self._y))
        self._bg_surface.fill((200, 200, 200, 150))

    def multi(self):
        self._text = self._font.render(f"{self._text_input}: {self._options[self._index]}", True, (255, 255, 255))
        self._text_rect = self._text.get_rect(center=(self._x, self._y))
        self._bg_surface = pygame.Surface((self._text_rect.width + 35, self._text_rect.height + 20), pygame.SRCALPHA)
        self._bg_rect = self._bg_surface.get_rect(center=(self._x, self._y))
        self._bg_surface.fill((200, 200, 200, 150))

    def draw(self):
        self._screen.blit(self._bg_surface, self._bg_rect)
        self._screen.blit(self._text, self._text_rect)

    def pressed(self, position):
        if self._state == "link":
            if position[0] in range(self._bg_rect.left, self._bg_rect.right) and position[1] in range(self._bg_rect.top, self._bg_rect.bottom):
                return True
            else:
                return False
        elif self._state == "multi":
            if position[0] in range(self._bg_rect.left, self._bg_rect.right) and position[1] in range(self._bg_rect.top, self._bg_rect.bottom):
                if self._index < len(self._options) - 1:
                    self._index += 1
                else:
                    self._index = 0
                self.multi()
            return self._index
