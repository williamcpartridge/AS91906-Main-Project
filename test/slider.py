# Slider v0.1
# A quick and dirty slider control for pygame
# Intended as a short demonstration of building a simple control.
# Devlin Sakey 2026
import pygame

class Slider():
	MIN_SLIDER_W = 200
	MIN_SLIDER_H = 100

	def __init__(self, x, y, w, h, text, font, font_color, bg_color, fg_color):
		if w < Slider.MIN_SLIDER_W:
			w = Slider.MIN_SLIDER_W
		if h < Slider.MIN_SLIDER_H:
			h = Slider.MIN_SLIDER_H
		self._x = x
		self._y = y
		self._w = w
		self._h = h
		self._text = text
		self._font = font
		self._font_color = font_color
		self._bg_color = bg_color
		self._fg_color = fg_color
		self.set_value(0)
		self._dirty = True # has the value been read since it last changed

	def set_value(self, value):
		if value < 0:
			self._value = 0
		elif value > 100:
			self._value = 100
		else:
			self._value = value
		self._dirty = True
	
	def get_value(self):
		self_dirty = False
		return self._value
	
	value = property(get_value, set_value)

	def get_dirty(self):
		return self._dirty
	dirty = property(get_dirty)

	def get_rect(self):
		return pygame.Rect(self._x, self._y, self._w, self._h)

	def contains(self, x, y):
		return self.get_rect().collidepoint(x, y)
	
	def click(self, x, y):
		relative_x = x - self._x - self._w / 10
		bar_width = self._w * 0.8
		self.set_value(relative_x / bar_width * 100)

	def draw(self, screen):
		# draw the rectangle and border
		pygame.draw.rect(screen, self._fg_color, self.get_rect())
		pygame.draw.rect(screen, self._bg_color, pygame.Rect(self._x+2, self._y + 2, self._w - 4, self._h - 4))

		# draw the text
		rendered_text = self._font.render(self._text, True, self._font_color, self._bg_color)
		rendered_text_rect = rendered_text.get_rect()
		rendered_text_rect.center = (self._x + self._w / 2, self._y + self._h / 4)
		screen.blit(rendered_text, rendered_text_rect)

		# draw the slider bar
		bar_width = self._w * 0.8
		bar_height = self._h / 8
		bar_x = self._x + self._w / 10
		pygame.draw.rect(screen, self._fg_color, pygame.Rect(self._x + self._w / 10, self._y + self._h * 0.6, bar_width, bar_height))
		pygame.draw.rect(screen, self._bg_color, pygame.Rect(self._x + self._w / 10 + 2, self._y + self._h * 0.6 + 2, bar_width - 4, bar_height - 4))

		# draw the slider
		slider_width = bar_height * 2
		slider_height = bar_height * 3
		slider_x_pos = bar_x + self._value / 100 * (bar_width - slider_width)
		pygame.draw.rect(screen, self._fg_color, pygame.Rect(slider_x_pos, self._y + self._h * 0.6 - bar_height, slider_width, slider_height))
		pygame.draw.rect(screen, self._bg_color, pygame.Rect(slider_x_pos + 2, self._y + self._h * 0.6 - bar_height + 2, slider_width - 4, slider_height - 4))