import pyglet
from pyglet import shapes
from pyglet.window import key
from typing import Tuple, Any
import math

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


def main():
    window = pyglet.window.Window(500, 500)
    heart = Heart((200, 200))

    @window.event
    def on_draw():
        window.clear()
        heart.draw()

    @window.event
    def on_key_press(symbol: Any, modifiers: Any) -> None:
        global enter_pressed
        if symbol == key.LEFT:
            heart.update((-10, 0))
        if symbol == key.RIGHT:
            heart.update((10, 0))
        if symbol == key.UP:
            heart.update((0, 10))
        if symbol == key.DOWN:
            heart.update((0, -10))

    pyglet.app.run()

if __name__ == "__main__":
    main()
