from copy import deepcopy
from typing import Tuple
import pyglet as pg
from pyglet import shapes
from heart import Heart
import pyglet
from pyglet.window import key
from typing import Any

class HUD:

    vector2D = Tuple[int, int]
    squareCoordinates = Tuple[int, int, int, int] # top left, top right, bottom left, bottom right

    def __init__(self, max_value: int = 5, position: vector2D = (200, 200)):
        self.position = position
        self.max_value = max_value
        self.hearts = []
        self.hearts = [Heart((x * 80, 0)) for x in range(max_value)]  # Initialize with max_value Heart objects

    def draw(self):
        for heart in self.hearts:
            heart.draw()


    def update(self, position: vector2D):
        """
        update the position by adding the supplied vector
        :param position:
        :return:
        """
        for heart in self.hearts:
            heart.update(position)
        return self.position

    def set_position(self, position: vector2D) -> vector2D:
        """
        set the position to the supplied vector
        :param position:
        :return:
        """

        self.position = position
        return self.position

    def update_value(self, damage: int = 10) -> int:
        """
        updates the hud based on whatever damage we take,
        or what stamina we're at
        """
        self.current_value -= damage
        return self.current_value

    def reset(self):
        self.current_value = deepcopy(self.max_value)

def main():
    window = pyglet.window.Window(500, 500)
    heart = HUD(2)

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


