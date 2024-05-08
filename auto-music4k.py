import threading
import time as t
import pyautogui as p
import keyboard

keys = ['a', 's', 'd', 'j', 'k', 'l']
coords = [(832, 1838), (1268, 1838), (1698, 1838), (2128, 1838), (2564, 1838), (3000, 1838)]
running = False

def press_key(coord, key):
    while running:
        if p.pixel(coord[0], coord[1])[2] < 220:
            p.keyDown(key)
            while running and p.pixel(coord[0], coord[1])[2] < 220:
                t.sleep(0.005)  # Minimize CPU usage, but effectively no "cooldown" between checks
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
