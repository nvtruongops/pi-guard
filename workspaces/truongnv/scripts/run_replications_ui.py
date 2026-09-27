"""
workspaces/truongnv/scripts/run_replications_ui.py

Launcher script for the Replications Model Explorer UI.
Usage:
    python workspaces/truongnv/scripts/run_replications_ui.py
    or:
    streamlit run workspaces/truongnv/src/dashboard/replications_explorer.py
"""

import os
import sys
import subprocess

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import threading
import time
import urllib.request

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DASHBOARD_PATH = os.path.join(WORKSPACE_ROOT, "src", "dashboard", "replications_explorer.py")
VENV_PYTHON = os.path.join(WORKSPACE_ROOT, ".venv", "Scripts", "python.exe")
VENV_STREAMLIT = os.path.join(WORKSPACE_ROOT, ".venv", "Scripts", "streamlit.exe")

def trigger_ram_preload(port=8501, delay=2.0):
    """
    Background worker that waits for the Streamlit server to start on the specified port,
    then automatically sends an HTTP request to trigger the model preloading into RAM
    before the user even opens the browser.
    """
    time.sleep(delay)
    target_url = f"http://localhost:{port}"
    print(f"\n[RAM PRELOAD] Đang kiểm tra cổng {port} để kích hoạt nạp mô hình vào RAM...")
    for attempt in range(15):
        try:
            req = urllib.request.Request(target_url, headers={"User-Agent": "PI-Guard-Preloader/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    print(f"[RAM PRELOAD] Cổng {port} đã mở! Tín hiệu kích hoạt nạp RAM thành công.")
                    print("[RAM PRELOAD] Toàn bộ 6 mô hình đang được nạp vào RAM máy chủ.\n")
                    return
        except Exception:
            time.sleep(1.0)
    print(f"[RAM PRELOAD] Không thể kết nối tới {target_url} sau 15 giây.")

def main():
    print("=" * 70)
    print("Khởi chạy PI-Guard Replications Model Explorer UI...")
    print(f"Target Dashboard: {DASHBOARD_PATH}")
    print("=" * 70)

    if not os.path.exists(DASHBOARD_PATH):
        print(f"[-] Error: Dashboard script not found at {DASHBOARD_PATH}")
        sys.exit(1)

    # Launch background RAM preloader worker
    preload_thread = threading.Thread(target=trigger_ram_preload, args=(8501, 2.0), daemon=True)
    preload_thread.start()

    cmd = [
        VENV_PYTHON, "-m", "streamlit", "run", DASHBOARD_PATH,
        "--server.port=8501",
        "--server.headless=true",
        "--server.fileWatcherType=none",
        "--theme.base=dark",
        "--theme.backgroundColor=#0b0f19",
        "--theme.secondaryBackgroundColor=#111827",
        "--theme.primaryColor=#3b82f6",
        "--theme.textColor=#f3f4f6"
    ]
    print(f"Executing: {' '.join(cmd)}\n")
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n[!] Dừng server UI.")

if __name__ == "__main__":
    main()
