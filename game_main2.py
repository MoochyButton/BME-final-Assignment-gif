import pyglet
from pyglet.window import key
from Monster import Monster
from HUD import HUD
from LostScreen import youlost


def main():
    # Initialize enter_pressed as a global variable
    global enter_pressed
    enter_pressed = False
    lost = False

    def centre_animation(animation):
        for frame in animation.frames:
            frame.image.anchor_x = frame.image.width // 2
            frame.image.anchor_y = frame.image.height // 2

    window = pyglet.window.Window(1000, 600)

    hud = HUD(position=(25, 500))

    # Load animations
    monster_sleep_gif = pyglet.image.load_animation('LadSleeping.gif')
    monster_anger_gif = pyglet.image.load_animation('AngyLad.gif')

    centre_animation(monster_sleep_gif)
    centre_animation(monster_anger_gif)

    top = pyglet.graphics.Batch()
    bot = pyglet.graphics.Batch()

    running_man = pyglet.image.load_animation('DudeRunning.gif')
    rotating_ball = pyglet.image.load_animation('rotating_ball.gif')

    centre_animation(running_man)
    centre_animation(rotating_ball)

    monster1 = Monster(window.get_size()[1], window.get_size()[0], monster_sleep_gif, monster_anger_gif)
    monster2 = Monster(window.get_size()[1], window.get_size()[0], monster_sleep_gif, monster_anger_gif)
    monster3 = Monster(window.get_size()[1], window.get_size()[0], monster_sleep_gif, monster_anger_gif)

    ball = pyglet.sprite.Sprite(rotating_ball, x=window.get_size()[0] / 2, y=0, batch=bot)
    ball.rotation = 90
    ball.scale = 1.7

    man = pyglet.sprite.Sprite(running_man, x=window.get_size()[0] / 2, y=window.get_size()[1] / 2, batch=top)
    man.scale = 1.7

    # Variable to track whether the Enter key is pressed
    enter_pressed = False

    @window.event
    def on_draw():
        window.clear()
        bot.draw()
        top.draw()
        monster1.draw()
        monster2.draw()
        monster3.draw()
        hud.draw()

    @window.event
    def on_key_press(symbol, modifiers):
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
            man.scale = 1.7  # Increase scale when Enter is pressed

    @window.event
    def on_key_release(symbol, modifiers):
        global enter_pressed
        if symbol == key.ENTER:
            enter_pressed = False
            hud.take_damage()
            man.scale = 1.7  # Decrease scale when Enter is released

    def update(dt):
        if len(hud.hearts) <= 0:
            lost = True
            youlost()
        else:
            global enter_pressed
            # impact_velocity = 6  # Example impact velocity, you can calculate based on your needs
            if not enter_pressed:
                impact_velocity = 4
            else:
                impact_velocity = 6

            monster1.display(threshold=5, impact_velocity=impact_velocity)
            monster1.update(dt)
            monster2.display(threshold=5, impact_velocity=impact_velocity)
            monster2.update(dt)
            monster3.display(threshold=5, impact_velocity=impact_velocity)
            monster3.update(dt)

    pyglet.clock.schedule_interval(update, 1 / 60.0)

    pyglet.app.run()


if __name__ == '__main__':
    main()
