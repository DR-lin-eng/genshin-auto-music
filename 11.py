import threading
import time
import pyautogui as p
import keyboard
from typing import Dict, Tuple
from datetime import datetime
from colorama import init, Fore, Back, Style

# 初始化colorama
init(autoreset=True)

# 基础分辨率和坐标配置
base_resolution = (1920, 1080)
base_coords = {
    'a': (417, 916),
    's': (632, 916),
    'd': (846, 916),
    'j': (1065, 916),
    'k': (1282, 916),
    'l': (1497, 916)
}

def print_banner():
    banner = f"""
{Fore.CYAN}╭──────────────────────────────────────────╮
│     {Fore.YELLOW}Genshin Impact Auto Music Player{Fore.CYAN}      │
│        {Fore.GREEN}Created by Your Name 2024{Fore.CYAN}        │
╰──────────────────────────────────────────╯{Style.RESET_ALL}
"""
    print(banner)

def print_status(message: str, status_type: str = "info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status_type == "info":
        print(f"{Fore.BLUE}[{timestamp}] ℹ {Fore.WHITE}{message}")
    elif status_type == "success":
        print(f"{Fore.GREEN}[{timestamp}] ✓ {Fore.WHITE}{message}")
    elif status_type == "warning":
        print(f"{Fore.YELLOW}[{timestamp}] ⚠ {Fore.WHITE}{message}")
    elif status_type == "error":
        print(f"{Fore.RED}[{timestamp}] ✗ {Fore.WHITE}{message}")

# 获取屏幕分辨率并计算缩放
screen_width, screen_height = p.size()
scale_x = screen_width / base_resolution[0]
scale_y = screen_height / base_resolution[1]

# 计算缩放后的坐标
scaled_coords = {k: (int(v[0] * scale_x), int(v[1] * scale_y)) 
                for k, v in base_coords.items()}

keys = list(scaled_coords.keys())
coords = list(scaled_coords.values())
running = False
key_press_counts = {key: 0 for key in keys}  # 添加按键计数器

def print_key_stats():
    while running:
        time.sleep(1)  # 每秒更新一次统计信息
        print("\033[2J\033[H")  # 清屏并移动光标到开始位置
        print_banner()
        print(f"{Fore.CYAN}按键统计信息：{Style.RESET_ALL}")
        for key, count in key_press_counts.items():
            print(f"{Fore.YELLOW}{key.upper()}{Style.RESET_ALL}: {Fore.GREEN}{count}{Style.RESET_ALL} 次")
        print("\n" + "=" * 50 + "\n")

def press_key(coord: Tuple[int, int], key: str):
    """优化的按键处理函数"""
    p.PAUSE = 0  # 禁用pyautogui的默认延迟
    while running:
        try:
            pixel = p.pixel(coord[0], coord[1])
            if pixel[2] < 220:  # 检查蓝色通道
                p.keyDown(key)
                key_press_counts[key] += 1  # 增加按键计数
                while running and p.pixel(coord[0], coord[1])[2] < 220:
                    time.sleep(0.001)  # 减少延迟到1ms
                p.keyUp(key)
        except:
            continue
        time.sleep(0.001)

def listen_for_stop():
    global running
    keyboard.wait('alt+v')
    running = False
    print_status("程序正在停止...", "warning")

def listen_for_start():
    global running
    keyboard.wait('alt+x')
    running = True
    print_status("程序已启动！", "success")

def main():
    global running
    print_banner()
    print_status("初始化成功！", "info")
    print_status(f"检测到屏幕分辨率: {screen_width}x{screen_height}", "info")
    print_status("按 Alt+X 开始运行，Alt+V 停止运行", "info")
    
    # 创建控制线程
    start_thread = threading.Thread(target=listen_for_start)
    stop_thread = threading.Thread(target=listen_for_stop)
    start_thread.daemon = True
    stop_thread.daemon = True
    
    # 启动控制线程
    start_thread.start()
    stop_thread.start()

    # 准备按键处理线程
    threads = []
    for coord, key in zip(coords, keys):
        thread = threading.Thread(target=press_key, args=(coord, key))
        thread.daemon = True
        threads.append(thread)

    # 创建统计信息显示线程
    stats_thread = threading.Thread(target=print_key_stats)
    stats_thread.daemon = True

    # 等待开始信号
    start_thread.join()
    
    # 启动所有线程
    stats_thread.start()
    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print_status("程序已停止运行", "info")
    print(f"\n{Fore.CYAN}最终统计信息：{Style.RESET_ALL}")
    for key, count in key_press_counts.items():
        print(f"{Fore.YELLOW}{key.upper()}{Style.RESET_ALL}: {Fore.GREEN}{count}{Style.RESET_ALL} 次")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_status("程序被用户中断", "error")
    except Exception as e:
        print_status(f"发生错误: {str(e)}", "error")
    finally:
        running = False

