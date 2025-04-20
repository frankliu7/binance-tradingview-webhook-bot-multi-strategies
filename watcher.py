
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".env") or event.src_path.endswith("strategy_config.json"):
            print("[🔁] Config file changed, reloading dashboard...")
            os.system("pkill -f streamlit")
            time.sleep(1)
            os.system("bash start_dashboard.sh")

observer = Observer()
observer.schedule(ReloadHandler(), path='.', recursive=False)
observer.start()

print("🛡️ Watching for changes in .env or strategy_config.json ...")
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
