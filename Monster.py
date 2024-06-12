import pyglet
import random as rnd


class Monster:
    def __init__(self, height, width, sleep_image, anger_image):
        self.width = width
        self.height = height
        self.starting_x_speed = rnd.randrange(-3, 3, 2)
        self.starting_y_speed = rnd.randrange(-3, 3, 2)
        self.x_speed = self.starting_x_speed
        self.y_speed = self.starting_y_speed
        self.anger_duration = 180  # duration the monster remains angry in frames (120 frames = 2 seconds at 60fps)
        self.is_angry = False
        self.anger_time = 0
        self.fight = pyglet.image.load_animation('beating.gif')
        self.fight_sprite = pyglet.sprite.Sprite(self.fight, x=(self.width / 2) - 200, y=(self.height / 2) - 200)
        self.sprite = pyglet.sprite.Sprite(sleep_image, x=(self.width / 2), y=(self.height / 2))
        self.sleep_image = sleep_image
        self.anger_image = anger_image
        self.sprite.scale = 0.40
        self.fight_sprite.scale = 2

    def display(self, threshold, impact_velocity):
        if impact_velocity < threshold and self.anger_time <= 0:
            self.is_angry = False
            self.sprite.image = self.sleep_image
            self.x_speed = self.starting_x_speed
            self.y_speed = self.starting_y_speed
        if impact_velocity > threshold:
            self.is_angry = True
            print(self.anger_time)
            self.anger_time = self.anger_duration
            self.sprite.image = self.anger_image

    def update(self, dt):
        # Update position
        if not self.is_angry:
            self.sprite.x += self.x_speed
            self.sprite.y += self.y_speed

        # Bounce off the borders
        if self.sprite.x <= 0 or self.sprite.x >= self.width:
            self.x_speed *= -1  # Reverse direction on x-axis
            self.starting_x_speed *= -1
        if self.sprite.y <= 0 or self.sprite.y >= self.height:
            self.y_speed *= -1  # Reverse direction on y-axis
            self.starting_y_speed *= -1

        # Move towards the center if angry
        if self.is_angry and self.anger_time > 0:
            self.anger_time -= 1
            self.x_speed = 6
            self.y_speed = 6
            if self.sprite.x < self.width/2:
                self.sprite.x += self.x_speed
            elif self.sprite.x > self.width/2:
                self.sprite.x -= self.x_speed

            if self.sprite.y < self.height/2:
                self.sprite.y += self.y_speed
            elif self.sprite.y > self.height/2:
                self.sprite.y -= self.y_speed

        elif self.anger_time <= 0:
            self.is_angry = False
            self.sprite.image = self.sleep_image
            self.x_speed = self.starting_x_speed
            self.y_speed = self.starting_y_speed

    def draw(self):
        self.sprite.draw()
        if self.is_angry and self.anger_time > 0:
            self.fight_sprite.draw()
