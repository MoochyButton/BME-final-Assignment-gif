from typing import Tuple
from heart import Heart
import pyglet as pg
from pyglet.window import key
from typing import Any


class HUD:

    vector2D = Tuple[int, int]
    squareCoordinates = Tuple[int, int, int, int] # top left, top right, bottom left, bottom right

    def __init__(self, size: int = 5, max_value: int = 5, position: vector2D = (200, 200)):
        self.position = position
        self.max_value = max_value
        self.size = size
        self.hearts = []
        self.hearts = [Heart(self.size, ((x * 6 * self.size) + self.position[0], self.position[1])) for x in range(max_value)]  # Initialize with max_value Heart objects

    def draw(self):
        for heart in self.hearts:
            heart.draw()

    def update(self, position: vector2D):
        """
        update the position by adding the supplied vector
        :param position:
        :return:
        """
        self.position += position
        for heart in self.hearts:
            heart.update(position)
        return self.position

    def set_position(self, position: vector2D) -> vector2D:
        """
        set the position to the supplied vector
        :param position:
        :return:
        """

        self.position += position
        return self.position

    def take_damage(self) -> int:
        """
        updates the hud based on whatever damage we take,
        or what stamina we're at
        """
        self.hearts.pop()
        return len(self.hearts)

    def reset(self):
        """
        resets the heart counter to max_hearts
        :return:
        """

        for _ in self.hearts:
            self.hearts.pop()
        self.hearts = [Heart(self.size, ((x * 6 * self.size) + self.position[0], self.position[1])) for x in range(self.max_value)]  # Initialize with max_value Heart objects


def main():
    window = pg.window.Window(500, 500)
    heart = HUD(10, 5, (50, 400))

    @window.event
    def on_draw():
        window.clear()
        heart.draw()

    @window.event
    def on_key_press(symbol: Any, modifiers: Any) -> None:
        global enter_pressed
        if symbol == key.LEFT:
            heart.take_damage()
        if symbol == key.RIGHT:
            heart.reset()
        if symbol == key.UP:
            heart.update((10, 0))
        if symbol == key.DOWN:
            heart.update((-10, 0))

    pg.app.run()


if __name__ == "__main__":
    main()


