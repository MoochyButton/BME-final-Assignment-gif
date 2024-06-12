import pyglet


class PygletTools:
    @staticmethod
    def shapes_to_sprite(batch, width, height):
        # Create an off-screen buffer to render the shapes
        buffer = pyglet.image.BufferImage(width, height)

        # Bind the buffer
        buffer.bind()

        # Draw the shapes to the buffer
        batch.draw()

        # Unbind the buffer
        buffer.unbind()

        # Create a texture from the buffer
        texture = buffer.get_texture()

        # Create a sprite from the texture
        sprite = pyglet.sprite.Sprite(texture)

        return sprite