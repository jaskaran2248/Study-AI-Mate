"""
StudyMate AI - Application Launcher & Port Manager
Automatically resolves port conflicts and binds to an available port.
"""
import os
import sys
import socket
import argparse
import uvicorn

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Checks whether a port is already occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True

def find_next_available_port(start_port: int = 8000, host: str = "127.0.0.1", max_tries: int = 50) -> int:
    """Finds the next free socket port starting from start_port."""
    for p in range(start_port, start_port + max_tries):
        if not is_port_in_use(p, host):
            return p
    return start_port

def main():
    parser = argparse.ArgumentParser(description="StudyMate AI Web Server")
    parser.add_argument("--port", type=int, default=None, help="Port to run server on (default: 8000 or next free)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    parser.add_argument("pos_port", nargs="?", type=int, default=None, help="Positional port argument")
    args = parser.parse_args()

    host = os.environ.get("HOST", args.host)
    requested_port = args.port or args.pos_port or int(os.environ.get("PORT", 8000))

    final_port = requested_port
    if is_port_in_use(requested_port, host):
        print("=" * 65)
        print(f"⚠️  Notice: Port {requested_port} is already in use by another process.")
        final_port = find_next_available_port(requested_port + 1, host)
        print(f"⚡ Automatically selected next free port: {final_port}")
        print("💡 Tip: To free port 8000 on Windows, run:")
        print("   Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force")
        print("=" * 65)

    print("=" * 65)
    print("  🎓 StudyMate AI – UN SDG 4 Quality Education")
    print(f"  👉 Server Running at: http://{host}:{final_port}")
    print("  Press Ctrl+C to stop the server.")
    print("=" * 65)

    try:
        uvicorn.run("app.main:app", host=host, port=final_port, reload=False)
    except OSError as e:
        if e.errno == 10048 or "10048" in str(e):
            print(f"\n❌ Port {final_port} was just occupied. Retrying with another port...")
            alt_port = find_next_available_port(final_port + 1, host)
            print(f"👉 Starting on alternate port: http://{host}:{alt_port}")
            uvicorn.run("app.main:app", host=host, port=alt_port, reload=False)
        else:
            raise

if __name__ == "__main__":
    main()
