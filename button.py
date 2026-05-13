import pygame

class Button():
    def __init__(self, count, index, font, text_input, screen):
        self.x = screen.get_width()/2
        self.y = (2*index)*(screen.get_height()/(((count+1)*2)))
        self.screen = screen
        self.font = font
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        self.bg_surface = pygame.Surface((self.text_rect.width + 35, self.text_rect.height + 20), pygame.SRCALPHA)
        self.bg_rect = self.bg_surface.get_rect(center=(self.x, self.y))
        self.bg_surface.fill((200, 200, 200, 150))

    def draw(self):
        self.screen.blit(self.bg_surface, self.bg_rect)
        self.screen.blit(self.text, self.text_rect)

    def pressed(self, position):
        if position[0] in range(self.bg_rect.left, self.bg_rect.right) and position[1] in range(self.bg_rect.top, self.bg_rect.bottom):
            return True
        else:
            return False