import pyglet
from typing import Tuple


class Heart:

    Vector2D = Tuple[int, int]

    def __init__(self, size, position: Vector2D = (0, 0)):
        self.position = position
        self.size = size
        self.sprite = pyglet.image.load_animation('heart.gif')
        self.sprite = pyglet.sprite.Sprite(self.sprite, self.position[0], self.position[1])
        self.sprite.scale = 0.01 * self.size

    def draw(self):
        self.sprite.draw()

    def update(self, position: Vector2D):
        self.position += position
        self.sprite.x += position[1]
        self.sprite.y += position[0]
