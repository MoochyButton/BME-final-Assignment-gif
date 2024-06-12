import threading
import queue
from game_main import create_window
from scrollsOfDestiny import main

if __name__ == '__main__':
    # create a data transmission line between two threads
    data_queue = queue.Queue()

    # create the input thread
    thread = threading.Thread(target=main, args=(data_queue,))
    thread.start()

    # create and run the pyglet window on the main thread
    create_window(data_queue)
