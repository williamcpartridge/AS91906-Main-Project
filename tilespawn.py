import pygame

class TileSpawn():
    def __init__(self, cell_count_x, cell_count_y, cell_width, cell_height, screen):
        if cell_count_x >= 0:
            self._cell_count_x = cell_count_x
        if cell_count_y >= 0:
            self._cell_count_y = cell_count_y

        if cell_width > 0:
            self._cell_width = cell_width
        if cell_height > 0:
            self._cell_height = cell_height

        if isinstance(screen, pygame.Surface):
            self._screen = screen

        self._tile_surf = pygame.Surface((cell_width, cell_width))
        self._LIGHT_GREEN = ((168, 230, 29))
        self._DARK_GREEN = ((127, 173, 22))


    def spawn_tiles(self, cell_cx, cell_cy):
        self._cell_count_x = cell_cx
        self._cell_count_y = cell_cy
        for x in range(self._cell_count_x):
            for y in range(self._cell_count_y):
                if y % 2 == 0:
                    if x % 2 == 0:
                        self._tile_surf.fill(self._LIGHT_GREEN)
                    else:
                        self._tile_surf.fill(self._DARK_GREEN)
                else:
                    if x % 2 == 0:
                        self._tile_surf.fill(self._DARK_GREEN)
                    else:
                        self._tile_surf.fill(self._LIGHT_GREEN)
                self._screen.blit(self._tile_surf, (x*self._cell_width, y*self._cell_height))

    def tile(self, x, y):
        x = int(x/self._cell_width)
        y = int(y/self._cell_height)

        if y % 2 == 0:
            if x % 2 == 0:
                self._tile_surf.fill(self._LIGHT_GREEN)
            else:
                self._tile_surf.fill(self._DARK_GREEN)
        else:
            if x % 2 == 0:
                self._tile_surf.fill(self._DARK_GREEN)
            else:
                self._tile_surf.fill(self._LIGHT_GREEN)
        self._screen.blit(self._tile_surf, (x*self._cell_width, y*self._cell_height))

if __name__ == "__main__":
    TEST_CX = 20
    TEST_CY = 14
    TEST_CW = 40
    TEST_CH = 40

    running = True

    screen = pygame.display.set_mode((TEST_CW*TEST_CX, TEST_CH*TEST_CY), pygame.RESIZABLE)

    tiles = TileSpawn(TEST_CX, TEST_CY, TEST_CW, TEST_CH, screen)
    tiles.spawn_tiles()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()



    pygame.quit()
    quit()
