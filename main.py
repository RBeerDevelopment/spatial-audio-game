import math
import os

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

from pygame import mixer

gridSize = 20

mixer.init()
# use this if more than the default 8 channels (i.e. objects) are required
# mixer.set_num_channels()


_sound_library = {}


def play_sound(sound_name, volume):
    global _sound_library
    sound = _sound_library.get(sound_name)
    if sound is None:
        sound_path = get_sound_path(sound_name)
        sound = mixer.Sound(sound_path)
        _sound_library[sound_name] = sound

    sound.set_volume(volume)
    sound.play()


def get_sound_path(sound_name):
    dir_name = os.path.dirname(__file__)
    path = os.path.join(dir_name + f'/sounds/{sound_name}')
    return path


class Player:
    def __init__(self, x, y, side_length=gridSize):
        self.x = x
        self.y = y
        self.side_length = side_length

    def moved(self):
        print_position(self.x, self.y)
        for sound_name, sound in _sound_library.items():
            sound.stop()
        for o in objects:
            o.check_close(self.x, self.y)

    def set_x(self, new_x):
        if 0 < new_x < self.side_length:
            self.x = new_x
            self.moved()

    def set_y(self, new_y):
        if 0 < new_y < self.side_length:
            self.y = new_y
            self.moved()

    def move_left(self):
        print('mvl')
        self.set_x(self.x - 1)

    def move_right(self):
        print('mvr')
        self.set_x(self.x + 1)

    def move_up(self):
        print('mvu')
        self.set_y(self.y + 1)

    def move_down(self):
        print('mvd')
        self.set_y(self.y - 1)


class Object:
    def __init__(self, x, y, name, sound_name, radius=1):
        self.x = x
        self.y = y
        self.name = name
        self.sound_name = sound_name
        self.radius = radius

    def check_close(self, player_x, player_y):
        distance = calculate_distance(player_x, player_y, self.x, self.y)
        print(f'Distance to {self.name}: {math.floor(distance)}')
        if distance <= self.radius:
            volume = round(1 - distance / self.radius, 2)
            print(f'{self.name}: {volume * 100}% volume')
            play_sound(self.sound_name, volume)


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


player = Player(1, 1)

objects = [
    Object(2, 3, 'Facet', 'water.mp3', radius=3),
    Object(5, 5, 'Door', 'door.mp3', radius=2),
]


def print_position(x, y):
    print(f"x: {x}, y: {y}")


def arrow_key_pressed(event):
    key = event.keysym
    if key == 'Up':
        player.move_up()
    elif key == 'Down':
        player.move_down()
    elif key == 'Left':
        player.move_left()
    elif key == 'Right':
        player.move_right()
    elif key == 'Escape':
        root.destroy()
    else:
        print("Please press an arrow key to move or press ESC to exit game.")


root = tk.Tk()
print("Press arrow keys to move (Escape key to exit):")
root.bind_all('<Key>', func=arrow_key_pressed)

root.mainloop()
