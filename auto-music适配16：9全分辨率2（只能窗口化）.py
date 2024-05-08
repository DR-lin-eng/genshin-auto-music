import threading
import time as t
import pyautogui as p
import keyboard
import pygetwindow as gw

# 基础分辨率和坐标
base_resolution = (1920, 1080)
base_coords = {
    'a': (424, 916),
    's': (638, 916),
    'd': (851, 916),
    'j': (1065, 916),
    'k': (1282, 916),
    'l': (1494, 916)
}

# 确保游戏窗口能被找到
try:
    win = gw.getWindowsWithTitle('原神')[0]  # 确保使用正确的窗口标题
    win.activate()
    win.moveTo(0, 0)
    win.resizeTo(base_resolution[0], base_resolution[1])
except IndexError:
    print("原神 window not found!")
    exit(1)

# 将坐标调整到窗口位置
left, top = win.topleft
scaled_coords = {k: (left + int(v[0]), top + int(v[1])) for k, v in base_coords.items()}
keys = list(scaled_coords.keys())
coords = list(scaled_coords.values())

# 控制变量
running = False

# 按键操作
def press_key(coord, key):
    print(f"Thread for key {key} started.")
    while running:
        if p.pixel(coord[0], coord[1])[2] < 220:
            p.keyDown(key)
            while running and p.pixel(coord[0], coord[1])[2] < 220:
                t.sleep(0.002)
            p.keyUp(key)
    print(f"Thread for key {key} stopped.")

# 监听停止和开始信号
def listen_for_stop():
    global running
    keyboard.wait('alt+v')
    running = False
    print("Stopping all threads...")

def listen_for_start():
    global running
    keyboard.wait('alt+x')
    running = True
    print("Starting all threads...")

# 创建并启动线程
def create_threads():
    threads = [threading.Thread(target=press_key, args=(coord, key)) for coord, key in zip(coords, keys)]
    for thread in threads:
        thread.start()
    return threads

# 主程序逻辑
if __name__ == "__main__":
    start_thread = threading.Thread(target=listen_for_start)
    stop_thread = threading.Thread(target=listen_for_stop)
    
    start_thread.start()
    stop_thread.start()

    start_thread.join()  # 等待开始信号

    if running:
        threads = create_threads()
        for thread in threads:
            thread.join()

    stop_thread.join()  # 等待停止信号