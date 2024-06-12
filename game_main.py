import pyglet
from pyglet.window import key
from typing import Any
from HUD import HUD

def main():
    def centre_animation(animation):
        for frame in animation.frames:
            frame.image.anchor_x = frame.image.width // 2
            frame.image.anchor_y = frame.image.height // 2

    window = pyglet.window.Window(500, 500)

    # make the hud
    hud = HUD(position=(25, 450))

    top = pyglet.graphics.Batch()
    bot = pyglet.graphics.Batch()

    running_man = pyglet.image.load_animation('running_man.gif')
    rotating_ball = pyglet.image.load_animation('rotating_ball.gif')

    centre_animation(running_man)
    centre_animation(rotating_ball)

    ball = pyglet.sprite.Sprite(rotating_ball, x=250, y=-320, batch=bot)
    ball.rotation = 90
    ball.scale = 2

    man = pyglet.sprite.Sprite(running_man, x=250, y=250, batch=top)

    # Variable to track whether the Enter key is pressed
    enter_pressed = False


    @window.event
    def on_draw():
        window.clear()
        bot.draw()
        top.draw()
        hud.draw()


    @window.event
    def on_key_press(symbol: Any, modifiers) -> None:
        global enter_pressed
        if symbol == key.LEFT:
            man.x -= 10
        elif symbol == key.RIGHT:
            man.x += 10
        elif symbol == key.UP:
            man.y += 10
        elif symbol == key.DOWN:
            man.y -= 10
        elif symbol == key.ENTER:
            enter_pressed = True
            man.scale *= 1.5  # Increase scale when Enter is pressed
        elif symbol == key.SPACE:
            hud.take_damage()
        elif symbol == key.BACKSPACE:
            hud.reset()

    @window.event
    def on_key_release(symbol: Any, modifiers) -> None:
        global enter_pressed
        if symbol == key.ENTER:
            enter_pressed = False
            man.scale /= 1.5  # Decrease scale when Enter is released

    pyglet.app.run()
