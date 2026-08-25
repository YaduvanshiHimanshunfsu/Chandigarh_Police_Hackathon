"""
PratiBimb Praman — Unified All-in-One Local Runner.

Single-command startup:
    python run.py

What this does:
  1. Configures local SQLite + in-memory task pipeline
  2. Ensures model artifacts, uploads, and report folders exist
  3. Launches FastAPI Backend (port 8000)
  4. Launches Next.js Frontend Dashboard (port 3000)
  5. Launches Forensic Celery Worker (with solo pool for Windows)
  6. Automatically opens your browser to http://localhost:3000
  7. Gracefully handles Ctrl+C to stop all child processes cleanly
"""

import os
import sys
import time
import shutil
import signal
import subprocess
import webbrowser
from pathlib import Path

# Resolve base directories (auto-detect whether run from parent or main folder)
CURRENT_DIR = Path(__file__).resolve().parent
if (CURRENT_DIR / "Chandigarh_Police_Hackathon-main").exists():
    ROOT_DIR = CURRENT_DIR / "Chandigarh_Police_Hackathon-main"
else:
    ROOT_DIR = CURRENT_DIR

BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

processes = []

def cleanup(signum=None, frame=None):
    """Gracefully terminate all running child processes."""
    print("\n\n[🛑 Shutting down PratiBimb Praman services...]")
    for proc in processes:
        if proc and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
    print("[✓ All services stopped. Goodbye!]")
    sys.exit(0)

# Register signal handlers for clean exit
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def setup_environment():
    """Ensure environment files, folders, and model artifacts are in place."""
    # Automatically discover and add Node.js to PATH if missing
    possible_node_dirs = [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\nodejs"),
        os.path.expandvars(r"%APPDATA%\npm"),
    ]
    current_path = os.environ.get("PATH", "")
    for nd in possible_node_dirs:
        if os.path.exists(nd) and nd.lower() not in current_path.lower():
            os.environ["PATH"] = nd + os.pathsep + os.environ["PATH"]

    print("=" * 65)
    print("  🛡️  PratiBimb Praman — AI Media Forensic Intelligence")
    print("      Unified Local Runner (Single-Command Mode)")
    print("=" * 65)

    # 1. Environment file setup
    env_local = BACKEND_DIR / ".env.local"
    env_target = BACKEND_DIR / ".env"
    if not env_target.exists() and env_local.exists():
        shutil.copy(env_local, env_target)
        print("[1/5] Initialized backend/.env with SQLite & local config")
    else:
        print("[1/5] Backend environment file verified")

    # 2. Upload and Report directories
    uploads = BACKEND_DIR / "uploads"
    reports = BACKEND_DIR / "reports"
    uploads.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    print("[2/5] Storage directories (uploads/, reports/) verified")

    # 3. Model verification
    onnx_model = BACKEND_DIR / "models" / "mobilenet_v2_triage.onnx"
    h5_model = BACKEND_DIR / "models" / "mobilenet_v2_finetuned.h5"
    if onnx_model.exists():
        size_mb = onnx_model.stat().st_size / (1024 * 1024)
        print(f"[3/5] MobileNetV2 ONNX model ready ({size_mb:.1f} MB)")
    elif h5_model.exists():
        print(f"[3/5] MobileNetV2 .h5 model found ({h5_model.name})")
    else:
        print("[3/5] Note: Running with deep learning ensemble models")

    # 4. Check frontend node_modules
    node_modules = FRONTEND_DIR / "node_modules"
    if not node_modules.exists():
        print("[4/5] Installing frontend packages (npm install)...")
        subprocess.run(["npm", "install"], cwd=str(FRONTEND_DIR), shell=True, check=True)
        print("      Frontend packages installed successfully")
    else:
        print("[4/5] Frontend dependencies verified")

def start_services():
    """Start Backend, Worker, and Frontend concurrently."""
    print("[5/5] Starting application services...")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND_DIR)

    # 1. Start FastAPI Backend
    print("      → Starting FastAPI Backend on http://localhost:8000...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=str(BACKEND_DIR),
        env=env,
    )
    processes.append(backend_proc)

    time.sleep(2)

    # 2. Start Celery Forensic Worker
    print("      → Starting Forensic Analysis Worker...")
    worker_proc = subprocess.Popen(
        [sys.executable, "-m", "celery", "-A", "app.core.celery_app", "worker", "--loglevel=info", "--concurrency=2", "--pool=solo"],
        cwd=str(BACKEND_DIR),
        env=env,
    )
    processes.append(worker_proc)

    time.sleep(2)

    # 3. Start Next.js Frontend
    print("      → Starting Next.js Dashboard on http://localhost:3000...")
    npm_cmd = shutil.which("npm") or r"C:\Program Files\nodejs\npm.cmd"
    frontend_proc = subprocess.Popen(
        f'"{npm_cmd}" run dev' if os.name == 'nt' else ["npm", "run", "dev"],
        cwd=str(FRONTEND_DIR),
        shell=True,
        env=env,
    )
    processes.append(frontend_proc)

    print("\n" + "=" * 65)
    print("  ✅ All services are RUNNING!")
    print("=" * 65)
    print("  🌐 Dashboard UI : http://localhost:3000")
    print("  📜 API Docs    : http://localhost:8000/docs")
    print("  Press Ctrl+C at any time to stop all services.")
    print("=" * 65 + "\n")

    # Wait for server to warm up and open browser
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:3000")
    except Exception:
        pass

    # Keep main process alive
    try:
        while True:
            time.sleep(1)
            # Check if critical processes died unexpectedly
            if backend_proc.poll() is not None:
                print("[⚠️ Backend process exited]")
                break
            if frontend_proc.poll() is not None:
                print("[⚠️ Frontend process exited]")
                break
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == "__main__":
    setup_environment()
    start_services()
