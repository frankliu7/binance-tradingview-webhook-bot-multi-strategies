import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import dotenv_values

class EnvFileChangeHandler(FileSystemEventHandler):
    def __init__(self, env_path=".env"):
        self.env_path = env_path

    def on_modified(self, event):
        if event.src_path.endswith(self.env_path):
            print(f"[monitor] Detected .env change, reloading environment...")
            new_env = dotenv_values(self.env_path)
            for k, v in new_env.items():
                os.environ[k] = v
            print(f"[monitor] .env reloaded.")

def start_env_monitor(env_path=".env"):
    event_handler = EnvFileChangeHandler(env_path=env_path)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print("[monitor] .env monitoring started.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_env_monitor()
