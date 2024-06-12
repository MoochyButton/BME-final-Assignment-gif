import threading
import queue

import game_main
import scrollsOfDestiny


def game_loop(input_queue):
    game_main.main()

    # if there is anything in the queue from the other thread
    if not input_queue.empty():
        # set the appropriate keys to True
        # tells the game which keys are being pressed by the neural network
        key_map = input_queue.get()


def sensor_loop(output_queue):
    scrollsOfDestiny.main(output_queue)



def main():
    ...



if __name__ == "__main__":
    # create a data transmission line between two threads
    data_queue = queue.Queue()

    # create two threads to run recognition and game simultaneously
    # this is done so that the chord recognition can record for several
    # seconds without interrupting the game
    game_thread = threading.Thread(target=game_loop, args=(data_queue,))
    ai_thread   = threading.Thread(target=sensor_loop, args=(data_queue,))

    # start the two threads
    game_thread.start()
    ai_thread.start()

    # wait for both threads to stop before ending the program
    game_thread.join()
    ai_thread.join()