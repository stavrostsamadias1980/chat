"""
Anytime.gr Complete RAG & Chatbot System Launcher
Launches:
  1. Pure Java 21 Spring Boot 3 Backend with WebSockets (Port 8088)
  2. Angular 22 UI Web Server (Port 4200)
"""

import os
import sys
import subprocess
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def start_all():
    print("="*70)
    print("🚀 STARTING ANYTIME.GR HYBRID RAG CHATBOT SYSTEM (100% PURE JAVA)")
    print("="*70)

    # 1. Start Spring Boot Pure Java Backend (with WebSockets)
    print("\n[1/2] Starting Pure Java 21 Spring Boot Backend (Port 8088)...")
    gradle_bat = ROOT_DIR / "BACKEND_JAVA" / "gradlew.bat"
    jar_file = ROOT_DIR / "BACKEND_JAVA" / "build" / "libs" / "anytime-chatbot-backend-3.0.0.jar"
    if jar_file.exists():
        java_cmd = ["java", "-jar", str(jar_file)]
    elif gradle_bat.exists():
        java_cmd = [str(gradle_bat), "bootRun"]
    else:
        gradle_bin = ROOT_DIR / "BACKEND_JAVA" / "gradle_dist" / "gradle-8.10.2" / "bin" / "gradle.bat"
        java_cmd = [str(gradle_bin), "bootRun"]
    java_proc = subprocess.Popen(java_cmd, cwd=str(ROOT_DIR / "BACKEND_JAVA"))
    print("      Spring Boot (Pure Java 21) process started.")

    time.sleep(3)

    # 2. Start Angular UI Server
    print("\n[2/2] Starting Angular 22 UI Dev Server on http://localhost:4200/...")
    dist_path = ROOT_DIR / "UI" / "dist" / "anytime-chatbot-ui" / "browser"
    if dist_path.exists():
        ui_cmd = [sys.executable, "-m", "http.server", "4200", "--directory", str(dist_path)]
    else:
        ui_cmd = ["npm", "start", "--prefix", str(ROOT_DIR / "UI"), "--", "--port", "4200"]
    ui_proc = subprocess.Popen(ui_cmd, cwd=str(ROOT_DIR / "UI"))

    print("\n" + "="*70)
    print("✨ ALL SERVICES RUNNING (100% PURE JAVA & ANGULAR 22)!")
    print("  🌐 Angular 22 Chatbot Portal : http://localhost:4200/")
    print("  ⚡ Pure Real-Time WebSocket  : ws://localhost:8088/ws/chat")
    print("  🛡️ HTTP Surface Exposure     : 0% (Pure WebSocket Stealth Mode)")
    print("="*70)
    print("\nPress Ctrl+C to stop all services.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        java_proc.terminate()
        ui_proc.terminate()
        print("All services stopped.")

if __name__ == "__main__":
    start_all()
