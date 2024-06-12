import pyglet
from pyglet.window import key
from HUD import HUD
from typing import Any

def centre_animation(animation):
    for frame in animation.frames:
        frame.image.anchor_x = frame.image.width // 2
        frame.image.anchor_y = frame.image.height // 2

def create_window(input_queue: Any = None):
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
        # window.clear()
        bot.draw()
        top.draw()
        hud.draw()

    def update(dt):
        nonlocal enter_pressed
        hit = False
        if input_queue and not input_queue.empty():
            hit = input_queue.get()
        if hit:
            man.scale *= 1.01

    @window.event
    def on_key_press(symbol: Any, modifiers) -> None:
        nonlocal enter_pressed
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
        nonlocal enter_pressed
        if symbol == key.ENTER:
            enter_pressed = False
            man.scale /= 1.5  # Decrease scale when Enter is released

    # Schedule the update function
    pyglet.clock.schedule_interval(update, 1/60.0)  # Update at 60Hz

    pyglet.app.run()

if __name__ == '__main__':
    create_window()