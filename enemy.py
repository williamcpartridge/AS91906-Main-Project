import pygame
from imagelist import ImageList

class Enemy():
    def __init__(self, x, y, width, height, screen):
        self.rect = pygame.Rect(x, y, width, height)
        self.screen = screen

    def get_width(self):
        return self.width

    def get_hight(self):
        return self.height

    def collide(self, position, width, height):
        pass

    def move():
        pass

    def draw(sprite, position, width, height, screen):
        pass

    def get_images():
        pass