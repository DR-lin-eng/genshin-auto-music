import threading
import time as t
import pyautogui as p
import keyboard


base_resolution = (1920, 1080)
base_coords = {
    'a': (417, 916),
    's': (632, 916),
    'd': (846, 916),
    'j': (1065, 916),
    'k': (1282, 916),
    'l': (1497, 916)
}


screen_width, screen_height = p.size()


scale_x = screen_width / base_resolution[0]
scale_y = screen_height / base_resolution[1]


scaled_coords = {k: (int(v[0] * scale_x), int(v[1] * scale_y)) for k, v in base_coords.items()}
keys = list(scaled_coords.keys())
coords = list(scaled_coords.values())

running = False

def press_key(coord, key):
    while running:
        if p.pixel(coord[0], coord[1])[2] < 240:
            p.keyDown(key)
            while running and p.pixel(coord[0], coord[1])[2] < 240:
                t.sleep(0.005)
            p.keyUp(key)

def listen_for_stop():
    global running
    keyboard.wait('alt+v')
    running = False

def listen_for_start():
    global running
    keyboard.wait('alt+x')
    running = True

start_thread = threading.Thread(target=listen_for_start)
start_thread.start()

stop_thread = threading.Thread(target=listen_for_stop)
stop_thread.start()

threads = []
for coord, key in zip(coords, keys):
    thread = threading.Thread(target=press_key, args=(coord, key))
    threads.append(thread)

start_thread.join()

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

stop_thread.join()
