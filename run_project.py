import subprocess
import webbrowser
import time
import os
import sys

# Paths
BACKEND_DIR = os.path.join(os.getcwd())
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend")

def run_backend():
    print("🚀 Starting Flask backend...")
    return subprocess.Popen([sys.executable, "app.py"], cwd=BACKEND_DIR)

def run_frontend():
    print("⚛️ Starting React frontend...")
    return subprocess.Popen(["npm", "run", "dev"], cwd=FRONTEND_DIR, shell=True)

if __name__ == "__main__":
    backend = run_backend()
    time.sleep(2)  # wait for Flask to start

    frontend = run_frontend()
    time.sleep(3)  # wait for Vite to start

    print("🌍 Opening app in browser...")
    webbrowser.open("http://localhost:5173")

    # Keep running until user stops
    backend.wait()
    frontend.wait()
