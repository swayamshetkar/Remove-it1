import threading
import time
import requests
import os

def start_keep_alive():
    """Background ping thread to keep Render backend awake."""
    render_url = os.getenv("RENDER_BACKEND_URL", "https://YOUR_RENDER_DOMAIN_HERE")

    # 🔹 Function to repeatedly ping the backend
    def keep_alive():
        while True:
            try:
                requests.get(f"{render_url}/", timeout=5)
                print("✅ Pinged backend successfully")
            except Exception as e:
                print(f"⚠️ Ping failed: {e}")
            time.sleep(30)  # every 30 seconds

    # 🔹 Immediate first ping at startup
    try:
        requests.get(f"{render_url}/", timeout=5)
        print("✅ Initial ping done")
    except Exception as e:
        print(f"⚠️ Initial ping failed: {e}")

    # 🔹 Start background ping thread
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
