import pyglet
from pyglet import shapes
from pyglet.window import key
from typing import Tuple, Any


class Heart:

    Vector2D = Tuple[int, int]

    def __init__(self, position: Vector2D = (0, 0)):
        self.position = position
        self.ear1 = shapes.Circle(self.position[0] + 52.8, self.position[1] + 17.6, 25, 10)
        self.ear2 = shapes.Circle(self.position[0] + 17.6, self.position[1] + 17.6, 25, 10)
        self.body = shapes.Rectangle(self.position[0], self.position[1], 50, 50)
        self.body.rotation = 45

    def draw(self):
        self.body.draw()
        self.ear1.draw()
        self.ear2.draw()

    def update(self, position: Vector2D):
        self.body.x += position[0]
        self.ear1.x += position[0]
        self.ear2.x += position[0]
        self.body.y += position[1]
        self.ear1.y += position[1]
        self.ear2.y += position[1]


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
