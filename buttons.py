import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text=None, color=(96, 196, 237)):
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.color = color
        self.high_light_color = (189, 189, 189)
        self.highlighted = False
        self.function = None
        self.params = None

    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        self.image.fill(self.high_light_color if self.highlighted else self.color)
        window.blit(self.image, self.pos)
        self.text_to_button(window, self.pos)

    def text_to_button(self, window, pos, color=BLACK):
        font = pygame.font.SysFont("arial", round(CELL_SIZE//2))
        render_font = font.render(self.text, False, color)
        font_width = render_font.get_width()
        font_height = render_font.get_height()
        x = pos[0] + 5
        y = pos[1] + 2
        window.blit(render_font, (x, y))


    def set_high_light_color(self, color):
        self.high_light_color = color

    def set_function(self, function):
        self.function = function

    def set_params(self, param):
        self.params = param
