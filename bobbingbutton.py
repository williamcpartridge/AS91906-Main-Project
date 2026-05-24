import pygame
import math

class BobbingButton:
    def __init__(self, x, y, width, height, text="", base_color=(0, 150, 255), hover_color=(0, 255, 0)):
        # 1. Geometry and State
        self.base_rect = pygame.Rect(x, y, width, height)
        self.draw_rect = self.base_rect.copy()
        self.is_hovered = False
        
        # 2. Colors and Text
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.text = text
        self.font = pygame.font.SysFont(None, 24)

        # 3. Animation Variables
        self.bob_intensity = 0.0
        self.transition_speed = 0.1  # Higher = snaps faster, Lower = smoother
        self.bob_range = 3          # Max pixels it moves up/down
        self.bob_speed = 0.007        # Speed of the sine wave oscillation

    def update(self, mouse_pos):
        """Handles hover detection and smooth animation math."""
        # Check hover state against the stationary base position
        self.is_hovered = self.base_rect.collidepoint(mouse_pos)

        # Linear Interpolation (Lerp) for smooth dampening
        target_intensity = 1.0 if self.is_hovered else 0.0
        self.bob_intensity += (target_intensity - self.bob_intensity) * self.transition_speed

        # Reset draw rect to base, then apply the dampened sine wave offset
        self.draw_rect = self.base_rect.copy()
        ticks = pygame.time.get_ticks()
        
        raw_bob = math.sin(ticks * self.bob_speed) * self.bob_range
        self.draw_rect.y += raw_bob * self.bob_intensity

        # Smoothly blend the color based on animation intensity
        self.current_color = (
            int(self.base_color[0] + (self.hover_color[0] - self.base_color[0]) * self.bob_intensity),
            int(self.base_color[1] + (self.hover_color[1] - self.base_color[1]) * self.bob_intensity),
            int(self.base_color[2] + (self.hover_color[2] - self.base_color[2]) * self.bob_intensity)
        )

    def draw(self, surface):
        """Renders the button and its centered text onto the screen."""
        # Draw button body
        pygame.draw.rect(surface, self.current_color, self.draw_rect)
        
        # Draw centered text (it will move smoothly with the button)
        if self.text:
            text_surf = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.draw_rect.center)
            surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        """Returns True if the button is successfully clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False


# ==========================================
# EXAMPLE USAGE IN A PYGAME LOOP
# ==========================================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 400))
    clock = pygame.time.Clock()

    # Instantiate multiple buttons easily
    btn_start = BobbingButton(75, 175, 140, 50, "Start Game")
    btn_quit = BobbingButton(285, 175, 140, 50, "Quit", base_color=(200, 50, 50), hover_color=(255, 100, 100))

    buttons = [btn_start, btn_quit]

    running = True
    while running:
        mouse_position = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle clicks
            if btn_start.handle_event(event):
                print("Start Game Triggered!")
            if btn_quit.handle_event(event):
                print("Quit Triggered!")
                running = False

        # Update all buttons
        for btn in buttons:
            btn.update(mouse_position)

        # Draw everything
        screen.fill((30, 30, 30))
        for btn in buttons:
            btn.draw(screen)
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
