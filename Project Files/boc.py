import tkinter as tk
import time
import random
import ctypes
import os
import threading
import sys

# Constants for window styles
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

# Ensure the window handles high-DPI settings correctly
ctypes.windll.shcore.SetProcessDpiAwareness(1)

def hide_from_taskbar(window_id):
    hwnd = window_id
    ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ex_style |= WS_EX_TOOLWINDOW
    ex_style &= ~WS_EX_APPWINDOW
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)
    ctypes.windll.user32.ShowWindow(hwnd, 5)

def make_click_through(window_id):
    hwnd = window_id
    ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ex_style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)

def overlay_pixel_by_pixel(color, pixel_size, speed, pause_event):
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    rainbow_mode = color.lower() == "rainbow"

    while True:
        pause_event.wait()  # Wait here if paused
        x = random.randint(0, width - pixel_size)
        y = random.randint(0, height - pixel_size)

        if rainbow_mode:
            color = random_color()

        canvas.create_rectangle(x, y, x + pixel_size, y + pixel_size, fill=color, outline=color)
        root.update()
        time.sleep(speed)

def random_color():
    return f'#{random.randint(0, 0xFFFFFF):06x}'

def get_user_input():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the Blackout Challenge")
    print("Epilepsy Warning")
    print("The Challenge is to play a game with this running until you can't see")
    print("See how far you can get")
    print()
    print("Created by: AKD_08")
    print()
    print("After the program has started in the cmd window you can type Pause and Play to pause and unpause the program")
    print()
    print("to RESTART close and open the program. You can close the program by typing STOP or hitting the X")
    print()
    color = input("What color do you want (type 'rainbow' for random colors)(default black): ")
    pixel_size = int(input("What pixel size do you want (default 1): "))
    speed = float(input("How fast do you want it to be (in seconds)(default 0.01): "))
    return color, pixel_size, speed

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)

def show_tip():
    tips = ["Move fast", "Don't waste pixels", "Hurry up", "You're losing time", "You can do it", "Hurry or you can't see", "Time is ticking!", "Quick, before it's too late!", "Every second counts!", "Keep going, you're almost there!", "Speed is key!", "Don't slow down now!", "Stay focused!", "Make every move count!", "Stay sharp!", "No time to lose!", "Keep the pace!", "Stay on target!", "Quick,quick, quick!", "Keep your eyes on the prize!", "Stay in the zone!", "You're doing great, don't stop!", "Go, go, go!", "Stay ahead of the game!"]
    tip_label.config(text=random.choice(tips))
    tip_label.place(x=10, y=10)
    root.after(10000, lambda: tip_label.place_forget())  # Hide tip after 10 seconds
    root.after(600000, show_tip)  # Schedule the next tip after 10 minutes

def monitor_console(pause_event):
    while True:
        command = input().strip().lower()
        if command == "pause":
            pause_event.clear()  # Pause the pixel overlay
        elif command == "play":
            pause_event.set()  # Resume the pixel overlay
        elif command == "stop":
            print("Stopping the program...")
            os._exit(0)  # Terminate the program

if __name__ == "__main__":
    color, pixel_size, speed = get_user_input()
    countdown(3)

    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")  # Fullscreen window
    root.attributes('-topmost', True)  # Keep the window on top
    root.attributes('-transparentcolor', 'white')  # Set the transparent color

    # Hide the window from the taskbar
    root.update_idletasks()
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    if hwnd == 0:
        hwnd = root.winfo_id()
    hide_from_taskbar(hwnd)
    make_click_through(hwnd)

    canvas = tk.Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    tip_label = tk.Label(root, text="", font=("Arial", 12), bg='yellow', fg='black')
    
    root.after(600000, show_tip)  # Show the first tip after 10 minutes

    pause_event = threading.Event()
    pause_event.set()  # Initially not paused

    # Start the overlay_pixel_by_pixel function in a separate thread
    overlay_thread = threading.Thread(target=overlay_pixel_by_pixel, args=(color, pixel_size, speed, pause_event))
    overlay_thread.daemon = True
    overlay_thread.start()

    # Start the monitor_console function in a separate thread
    console_thread = threading.Thread(target=monitor_console, args=(pause_event,))
    console_thread.daemon = True
    console_thread.start()

    root.mainloop()
