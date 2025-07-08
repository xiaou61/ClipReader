import tkinter as tk
import threading
import pyperclip
import pyttsx3
import keyboard
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import sys

# 线程相关变量
read_thread = None
engine = None  # 当前语音引擎实例
engine_lock = threading.Lock()

def read_text(text):
    global engine
    # 每次新建engine
    local_engine = pyttsx3.init()
    local_engine.setProperty('rate', 150)
    local_engine.setProperty('volume', 1)

    with engine_lock:
        engine = local_engine  # 记录当前引擎，方便停止

    local_engine.say(text)
    local_engine.runAndWait()

    with engine_lock:
        engine = None  # 朗读完成，清空engine引用

def start_reading():
    global read_thread
    if read_thread and read_thread.is_alive():
        return
    text = pyperclip.paste()
    if text.strip():
        read_thread = threading.Thread(target=read_text, args=(text,), daemon=True)
        read_thread.start()

def stop_reading():
    with engine_lock:
        if engine is not None:
            engine.stop()

keyboard.add_hotkey('ctrl+alt+r', start_reading)
keyboard.add_hotkey('ctrl+alt+e', stop_reading)

def on_quit(icon, item):
    icon.stop()
    root.destroy()
    sys.exit()

def on_show(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

def create_image():
    image = Image.new('RGB', (64, 64), "white")
    dc = ImageDraw.Draw(image)
    dc.ellipse((16, 16, 48, 48), fill="black")
    return image

def minimize_to_tray():
    root.withdraw()
    tray_icon = pystray.Icon("clipboard_speaker")
    tray_icon.icon = create_image()
    tray_icon.menu = pystray.Menu(
        item('打开', on_show),
        item('退出', on_quit)
    )
    threading.Thread(target=tray_icon.run, daemon=True).start()

root = tk.Tk()
root.title("剪贴板英文朗读器")
root.geometry("320x130")

tk.Label(root, text="1.Ctrl + C 复制文本\n2.Ctrl + Alt + R 开始朗读\n3.Ctrl + Alt + E 停止朗读").pack(pady=15)
tk.Button(root, text="📥 最小化到托盘", command=minimize_to_tray).pack(pady=10)

root.protocol("WM_DELETE_WINDOW", minimize_to_tray)
root.mainloop()
