# Main import section
import os      # I used the OS module to set an environment variable to hide a pygame licensing banner.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # pygame - the reason we're here
import time    # I use this to get clock ticks for dealing with and calculating the framerate
from slider import Slider
from button import Button

# a simple debug print function borrowed from my debug library
def dprint(level,*arg):
	if level<=DEBUG:
		if level>0:
			print("  " * level, *arg)
		else:
			print( *arg )

def display_mouse_coords(surface, coords):
	mousefont = pygame.font.Font( MAIN_FONT, 10 )
	mousetext = mousefont.render( '('+str(coords[0])+','+str(coords[1])+')', True, WHITE, BLACK )
	mousetextRect = mousetext.get_rect()
	mousetextRect.center = coords
	surface.blit(mousetext, mousetextRect)

def my_button_function():
	print("I'm doing something because a button was clicked.")

# program settings and constants
DEBUG=1
# the logical screen size
LOGICAL_X = 800
LOGICAL_Y = 600

# font constants
MAIN_FONT = 'freesansbold.ttf'  # one of the free built in fonts with pygame

# color constants
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
LIGHTBLUE = (  0, 128, 255)
ORANGE    = (255, 100,   0)
BROWN     = ( 98,  52,  18)
PURPLE    = (104,  71, 141)
YELLOW    = (255, 233,   0)
PINK      = (255,   0, 128)

# PROGRAM INITIALIZATION
framecounter=0
# the actual window size
scr_x=800
scr_y=600
showfps=False
sound_on = True      # is sound on?
music_on = False      # is music on?
music_playing = False # is music currently playing?
music_volume = 1 # a float between 0 and 1
fullscreen=False
quitting = False
mouse_down = False
square_x = 50
square_y = 150
is_blue = True
image_x=150
image_y=150


pygame.init()       # Init the pygame library
pygame.mixer.init() # initialise sound mixer
clock = pygame.time.Clock() # init pygame clock

#Fullscreen
if fullscreen: 
	screen = pygame.display.set_mode((scr_x, scr_y), pygame.FULLSCREEN)
else: 
	screen = pygame.display.set_mode((scr_x, scr_y), pygame.RESIZABLE)
pygame.display.set_caption('My Window Caption')

# create separate canvas for scaling
canvas = pygame.Surface((LOGICAL_X, LOGICAL_Y))

# set up the text rectangle
font = pygame.font.Font( MAIN_FONT, 32)
text = font.render('Some Example Text', True, GREEN, BLUE)
textRect = text.get_rect()
textRect.center = (scr_x // 2, scr_y // 2)

# load images
image1 = pygame.image.load('redcloud.png')

# load sounds
sound_click = pygame.mixer.Sound('sounds\\click.wav')
sound_typing = pygame.mixer.Sound('sounds\\typing.wav')
sound_whoosh = pygame.mixer.Sound('sounds\\whoosh.wav')
music_loop = pygame.mixer.Sound('sounds\\music loop1.wav')


music_slider = Slider(10,10, 600, 100, "Music Volume", font, font_color = BLACK, bg_color = WHITE, fg_color = BLUE)
music_slider.value = 100

ok_button = Button(10,400, 100,50, "ok", font, bg_color = WHITE, font_color = BLUE, border_color = BLUE)
ok_button.set_action(my_button_function)

#move mouse to centre
pygame.mouse.set_pos(scr_x // 2, scr_y // 2)

# THE MAIN LOOP
while not quitting:
	# get the mouse current position
	coords=pygame.mouse.get_pos()
	# scale the mouse coordinates
	scaled_coords = ( coords[0] * LOGICAL_X //scr_x , coords[1] * LOGICAL_Y //scr_y )
	# Process the event queue
	for event in pygame.event.get():
		dprint(2, event )

		# processing operating system events
		if event.type == pygame.QUIT:  # have we pressed quit
			dprint(1, "Quit was clicked")
			quitting = True
		if event.type == pygame.VIDEORESIZE: # have we resized the window
			scr_x, scr_y = event.dict['size']
			print(event.dict['size'])
			screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
			dprint(1, "Window was resized to",scr_x, scr_y)

		# processing mouse events
		if event.type == pygame.MOUSEBUTTONDOWN:
			if sound_on: sound_click.play()
			mouse_down = True
			# tell the control about the click
			ok_button.mouse_click(event)
			dprint(1, "BUTTON",pygame.mouse.get_pressed(),"PRESSED AT", scaled_coords)
		if event.type == pygame.MOUSEBUTTONUP:
			dprint(1, "BUTTON",pygame.mouse.get_pressed(),"RELEASED AT", scaled_coords)
			mouse_down = False
			# tell the control about the click
			ok_button.mouse_click(event)
		if event.type == pygame.MOUSEMOTION:
			ok_button.mouse_move(scaled_coords[0], scaled_coords[1])

		# process key events
		if event.type == pygame.KEYDOWN: # this is the moment a key gets pressed.
			if sound_on: sound_typing.play()
			dprint(1, pygame.key.name(event.key), "was pressed")
			if event.key == pygame.K_ESCAPE:
				quitting = True
			if event.key == pygame.K_SPACE:
				is_blue = not is_blue
				dprint(0, "Changing colour to", "Blue" if is_blue else "Purple")
			if event.key == pygame.K_f:
				showfps = not showfps
				dprint(0, "Turning FPS", "On" if showfps else "Off")
			if event.key == pygame.K_s:
				sound_on = not sound_on
				dprint(0, "Turning sound", "On" if sound_on else "Off")
			if event.key == pygame.K_m:
				music_on = not music_on
				dprint(0, "Turning music", "On" if music_on else "Off")
		if event.type == pygame.KEYUP: # this is the moment a key gets let go.
			dprint(1, pygame.key.name(event.key), "was let go")

	# process keys currently being held.
	pressed = pygame.key.get_pressed()

	if pressed[pygame.K_UP]: 
		square_y -= 3
	if pressed[pygame.K_DOWN]: 
		square_y += 3
	if pressed[pygame.K_LEFT]: 
		square_x -= 3
	if pressed[pygame.K_RIGHT]: 
		square_x += 3
	
	if mouse_down:
		if music_slider.contains(scaled_coords[0], scaled_coords[1]):
			music_slider.click(scaled_coords[0],scaled_coords[1])
		elif ok_button.contains(scaled_coords[0], scaled_coords[1]):
			pass # this is processed on release, but we don't want other things to happen
		else:
			pressed_buttons = pygame.mouse.get_pressed() # this is a list of True/False
			if pressed_buttons[0] == True: # left button
				# set the location of the square
				square_x = scaled_coords[0]
				square_y = scaled_coords[1]
			if pressed_buttons[1] == True: # middle button
				# set the location of the text rectangle
				textRect.center = (scaled_coords[0], scaled_coords[1])
			if pressed_buttons[2] == True: # right button
				# set the location of the image
				image_x=scaled_coords[0]
				image_y=scaled_coords[1]

	# starting/stopping music
	if music_on and sound_on:
		if not music_playing: # only start the music if it's not already playing
			music_channel = music_loop.play(loops=-1)
			music_playing = True
	else:
		if music_playing:     # only stop the music if it's playing
			music_loop.stop()
			music_playing = False

	# only set the music volume if the slider has changed
	if music_playing and music_slider.dirty:
		music_volume = music_slider.value / 100
		music_channel.set_volume( music_volume)
		dprint(0, f"Music volume set to {music_volume}.")

	#Clear The Screen
	canvas.fill(BLACK)
	# Blit the text image
	canvas.blit(text, textRect)
	# Blit the image we loaded earlier
	canvas.blit(image1,(image_x,image_y))

	# draw the slider
	music_slider.draw(canvas)
	# draw the button
	ok_button.draw(canvas)
	
	# Draw the coloured square
	if is_blue: 
		color = LIGHTBLUE
	else: 
		color = PURPLE
	pygame.draw.rect(canvas, color, pygame.Rect(square_x, square_y, 60, 60))
	pygame.draw.line(canvas, WHITE, (square_x,square_y), (square_x+59,square_y+59), 1)
	pygame.draw.line(canvas, WHITE, (square_x+59,square_y), (square_x,square_y+59), 1)

	# show the mouse coordinates if we're not currently clicking.
	if not mouse_down: 
		display_mouse_coords(canvas, scaled_coords)

	# scale the canvas and blit
	scale_x = scr_x / LOGICAL_X
	scale_y = scr_y / LOGICAL_Y

	# 2. Choose the smaller scale factor to ensure the canvas fits entirely inside the window
	scale = min(scale_x, scale_y)

	# 3. Calculate the new width and height using the same scale factor
	new_w = int(LOGICAL_X * scale)
	new_h = int(LOGICAL_Y * scale)

	# 4. Scale the canvas and center it on the screen (adds letterboxing/pillarboxing)
	scaled_canvas = pygame.transform.scale(canvas, (new_w, new_h))

	# Center the image by calculating the offset (black bar) padding
	offset_x = (scr_x - new_w) // 2
	offset_y = (scr_y - new_h) // 2

	screen.blit(scaled_canvas, (offset_x, offset_y))

	# Show the display buffer
	pygame.display.flip()
	# limit the frame rate to 60fps
	clock.tick(60)

	if showfps:
		framecounter+=1
		if framecounter==30: 
			print("FPS:", clock.get_fps())
			framecounter=0

# get ready to quit - stop music and play final sound
dprint(0, "Stopping sounds and quitting Program.")
if sound_on:
	if music_playing:
		music_loop.stop()
	sound_channel = sound_whoosh.play()
	# actually wait for all sounds to finish
	while sound_channel.get_busy():
			clock.tick(60)

# unload the pygame stuff and quit
pygame.mixer.quit()
pygame.quit()
exit()