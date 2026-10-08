"""Start/status/stop the local background server without keeping a terminal open."""
import argparse
import os
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "server/.runtime"
PIDFILE = RUNTIME / "server.pid"


def running():
    if not PIDFILE.exists():
        return None
    pid = int(PIDFILE.read_text().strip())
    try:
        command = subprocess.check_output(["ps", "-p", str(pid), "-o", "args="], text=True).strip()
        if "uvicorn server.app:app" in command and "--port 5000" in command:
            return pid
    except subprocess.CalledProcessError:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "stop", "status"])
    action = parser.parse_args().action
    pid = running()
    if action == "status":
        print(f"Running (PID {pid}) on http://127.0.0.1:5000" if pid else "Not running under this manager.")
    elif action == "stop":
        if pid:
            os.kill(pid, signal.SIGTERM)
            PIDFILE.unlink(missing_ok=True)
            print("Stopped portfolio server.")
        else:
            print("No managed portfolio server is running.")
    elif pid:
        print(f"Already running (PID {pid}).")
    else:
        RUNTIME.mkdir(exist_ok=True, mode=0o700)
        with (RUNTIME / "server.log").open("a") as log:
            process = subprocess.Popen([sys.executable, "-m", "uvicorn", "server.app:app",
                "--host", "127.0.0.1", "--port", "5000", "--no-proxy-headers", "--no-access-log"],
                cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
        PIDFILE.write_text(str(process.pid))
        for _ in range(30):
            if process.poll() is not None:
                PIDFILE.unlink(missing_ok=True)
                raise SystemExit(f"Server failed to start. See {RUNTIME / 'server.log'}")
            try:
                with urllib.request.urlopen("http://127.0.0.1:5000/api/config", timeout=1):
                    print(f"Started portfolio server (PID {process.pid}) on port 5000.")
                    return
            except OSError:
                time.sleep(0.2)
        raise SystemExit("Startup is taking longer than expected; check server/.runtime/server.log.")


if __name__ == "__main__":
    main()
