import tkinter as tk
import threading
import time
import pyperclip
import pyttsx3
import keyboard
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import sys

# 初始化语音引擎
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# 剪贴板朗读逻辑
def read_clipboard():
    text = pyperclip.paste()
    if text.strip():
        engine.say(text)
        engine.runAndWait()

# 持续监听 Ctrl+Alt+R 并朗读
def listen_clipboard():
    while True:
        keyboard.wait('ctrl+alt+r')
        read_clipboard()
        time.sleep(0.1)

# 托盘关闭程序
def on_quit(icon, item):
    icon.stop()
    root.destroy()
    sys.exit()

# 托盘恢复窗口
def on_show(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

# 创建托盘图标
def create_image():
    image = Image.new('RGB', (64, 64), "white")
    dc = ImageDraw.Draw(image)
    dc.ellipse((16, 16, 48, 48), fill="black")
    return image

# 最小化到托盘
def minimize_to_tray():
    root.withdraw()
    tray_icon = pystray.Icon("clipboard_speaker")
    tray_icon.icon = create_image()
    tray_icon.menu = pystray.Menu(
        item('打开', on_show),
        item('退出', on_quit)
    )
    threading.Thread(target=tray_icon.run, daemon=True).start()

# GUI 主程序
root = tk.Tk()
root.title("剪贴板英文朗读器")
root.geometry("300x120")

tk.Label(root, text="程序已启动，需要首先Ctrl + C 来复制你所要朗读的英文之后，按 Ctrl + Alt + R 朗读剪贴板内容").pack(pady=15)
tk.Button(root, text="📥 最小化到托盘", command=minimize_to_tray).pack(pady=10)

# 启动监听线程
threading.Thread(target=listen_clipboard, daemon=True).start()

# 拦截关闭窗口行为（最小化）
root.protocol("WM_DELETE_WINDOW", minimize_to_tray)
root.mainloop()
