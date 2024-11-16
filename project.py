import time
import sys
import os
import subprocess

def open_readme():
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.txt")
    if os.path.exists(readme_path):
        try:
            if sys.platform == "win32":
                os.startfile(readme_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", readme_path])
            else:
                subprocess.run(["xdg-open", readme_path])
        except Exception as e:
            print(f"Error opening README.txt: {e}")
    else:
        print("README.txt not found.")

def simulate_loading(label, duration=5):
    total_ticks = 50  # Total number of ticks in the loading bar
    interval = duration / total_ticks  # Time per tick

    print(f"Initializing {label} Black Out Challenge...")

    for i in range(total_ticks + 1):
        time.sleep(interval)  # Simulate time delay
        percent_complete = (i / total_ticks) * 100
        bar = '#' * i + '-' * (total_ticks - i)
        sys.stdout.write(f"\r{label} Loading... [{bar}] {percent_complete:.2f}%")
        sys.stdout.flush()
    
    print(f"\n{label} Loading complete!")

def launch_python_file(file_path):
    if os.path.exists(file_path):
        print(f"Launching {file_path}...")
        try:
            subprocess.run(["python", file_path], check=True)  # This assumes 'python' is in your PATH
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running the script: {e}")
        except FileNotFoundError as e:
            print(f"Python executable not found: {e}")
    else:
        print(f"File not found at {file_path}")

if __name__ == "__main__":
    open_readme()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "Project Files", "boc.py")
    
    tasks = ["Mouse passthrough", "Screen overlay", "Pause", "Play", "Stop", "Sizes", "Colors", "Speeds"]  # Add more labels for loading bars if needed

    for task in tasks:
        simulate_loading(task, duration=1)  # Duration can be adjusted if needed
    
    launch_python_file(file_path)
