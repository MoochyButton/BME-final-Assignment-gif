import pyglet
from pyglet.window import key

# Window dimensions
window_width = 800
window_height = 600

# Create the main window
window = pyglet.window.Window(window_width, window_height, "Start Screen Example")

background_image = pyglet.image.load('Lost.jpg')  # Replace with your image file path
background_sprite = pyglet.sprite.Sprite(background_image)

# Create a label for the welcome message
welcome_label = pyglet.text.Label(
    'Well, you lost, quit your stomping',
    font_name='Arial',
    font_size=32,
    x=window_width // 2,
    y=window_height - 200,
    anchor_x='center',
    anchor_y='center',
    bold=True
)

subtitle = pyglet.text.Label(
    'Press Space to restart',
    font_name='Arial',
    font_size=16,
    x=window_width // 2,
    y=window_height - 300,
    anchor_x='center',
    anchor_y='center',
    bold=True
)

# Boolean to track if the start button was clicked
start_clicked = False


# Handle key press events
@window.event
def on_key_press(symbol, modifiers):
    global start_clicked
    if symbol == key.SPACE:
        start_clicked = True
        print("Spacebar pressed! Starting application...")
        # Close the window to simulate moving to the next screen
        window.close()


# Handle window draw events
@window.event
def on_draw():
    window.clear()
    background_sprite.draw()
    welcome_label.draw()
    subtitle.draw()


# Function to create the start screen
def create_start_screen():
    global start_clicked
    pyglet.app.run()
    return start_clicked


# Call this function to display the start screen
start_screen_result = create_start_screen()

# Print the result after the window is closed
print(f"Spacebar pressed: {start_screen_result}")

# If needed, use the boolean to perform further actions
if start_screen_result:
    print("Proceeding to the main application...")
    start = True
    # Add your main application code here
else:
    print("Spacebar was not pressed.")


def restarted():
    return start
