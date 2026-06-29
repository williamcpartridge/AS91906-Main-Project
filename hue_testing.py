import pygame
import sys

# Initialize Pygame
pygame.init()

# Setup display window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame HSLA Testing")
clock = pygame.time.Clock()

def create_test_surface():
    """Generates a sample surface with a gradient for testing."""
    surf = pygame.Surface((200, 200), pygame.SRCALPHA)
    # Draw a multi-coloured gradient rectangle
    for i in range(200):
        for j in range(200):
            # Creates a red-to-green gradient with a solid blue component
            surf.set_at((i, j), (i, j, 150, 255))
    return surf

def adjust_hue_and_brightness(surface, hue_shift=0, brightness_shift=0):
    """Modifies the hue and brightness using PixelArray."""
    modified_surface = surface.copy()
    
    with pygame.PixelArray(modified_surface) as pixels:
        for x in range(modified_surface.get_width()):
            for y in range(modified_surface.get_height()):
                # FIX: Unmap the raw pixel integer into a valid Pygame Color object
                raw_pixel = pixels[x, y]
                color = pygame.Color(surface.unmap_rgb(raw_pixel))
                
                # Unpack current HSLA values
                h, s, l, a = color.hsla
                
                # Apply shifts and clamp values within legal boundaries
                new_h = (h + hue_shift) % 360
                new_l = max(0.0, min(100.0, l + brightness_shift))
                
                # Assign back safely
                color.hsla = (new_h, s, new_l, a)
                pixels[x, y] = color
                
    return modified_surface

# Create our base asset
base_image = pygame.image.load('images\snake\head\snake_head0.png')

# Initial modifier states
hue = 0
brightness = 0

# Main Game Loop
running = True
while running:
    screen.fill((40, 40, 40)) # Dark background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Capture keyboard inputs to adjust variables dynamically
    keys = pygame.key.get_pressed()
    
    # Left/Right changes Hue
    if keys[pygame.K_LEFT]:  hue = (hue - 2) % 360
    if keys[pygame.K_RIGHT]: hue = (hue + 2) % 360
    
    # Up/Down changes Brightness (Lightness)
    if keys[pygame.K_UP]:    brightness = min(50, brightness + 1)
    if keys[pygame.K_DOWN]:  brightness = max(-50, brightness - 1)

    # Process the surface modifier
    altered_image = adjust_hue_and_brightness(base_image, hue_shift=hue, brightness_shift=brightness)

    # Render visuals to the screen
    screen.blit(base_image, (150, 200))     # Left side: Original reference
    screen.blit(altered_image, (450, 200))  # Right side: Modified output

    # Simple HUD overlay instructions
    font = pygame.font.SysFont(None, 24)
    txt_hue = font.render(f"Hue Shift (Left/Right Arrows): {hue}°", True, (255, 255, 255))
    txt_bright = font.render(f"Brightness Shift (Up/Down Arrows): {brightness}%", True, (255, 255, 255))
    txt_orig = font.render("Original", True, (255, 255, 255))
    txt_mod = font.render("Modified", True, (255, 255, 255))
    
    screen.blit(txt_hue, (20, 20))
    screen.blit(txt_bright, (20, 50))
    screen.blit(txt_orig, (220, 170))
    screen.blit(txt_mod, (520, 170))

    pygame.display.flip()
    clock.tick(60) # Limit performance frame rate to 60 FPS

pygame.quit()
sys.exit()
