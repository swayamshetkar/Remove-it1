import threading
import time
import requests
import os
import psutil

def start_keep_alive():
    """Background ping thread to keep Render backend awake and optionally restart container."""
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

    # 🔹 Optional: Memory watchdog to restart container if usage is high
    def memory_watchdog(threshold=80):  # % of RAM
        while True:
            mem = psutil.virtual_memory()
            if mem.percent > threshold:
                print(f"⚠️ Memory high ({mem.percent}%), restarting container...")
                os._exit(1)  # triggers Render auto-restart
            time.sleep(10)

    threading.Thread(target=memory_watchdog, daemon=True).start()

    # 🔹 Optional: Periodic restart (e.g., every 5 minutes)
    def periodic_restart(interval_minutes=5):
        while True:
            time.sleep(interval_minutes * 60)
            print("🔁 Periodic restart triggered")
            os._exit(1)  # triggers Render auto-restart

    threading.Thread(target=periodic_restart, daemon=True).start()

    # 🔹 Start background ping thread
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
