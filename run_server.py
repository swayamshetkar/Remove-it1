import threading
import time
import requests
import os

def start_keep_alive():
    """Background ping thread to keep Render backend awake."""
    render_url = os.getenv("RENDER_BACKEND_URL", "https://YOUR_RENDER_DOMAIN_HERE")

    def keep_alive():
        while True:
            try:
                requests.get(f"{render_url}/", timeout=5)
                print("✅ Pinged backend successfully")
            except Exception as e:
                print(f"⚠️ Ping failed: {e}")
            time.sleep(30)

    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
