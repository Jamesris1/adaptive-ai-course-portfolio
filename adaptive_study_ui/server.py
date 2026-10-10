"""Local-only coursework server.

No package installation is needed. Run: python server.py [--port 8765]
"""
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class StudyHandler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, ".mjs": "text/javascript"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).resolve().parent), **kwargs)


def main():
    parser = argparse.ArgumentParser(description="Serve Adaptive Study Desk on this computer.")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    try:
        with ThreadingHTTPServer(("127.0.0.1", args.port), StudyHandler) as server:
            print(f"Open http://127.0.0.1:{args.port}/ in your browser. Press Ctrl+C to stop.", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as exc:
        parser.exit(1, f"Could not start the local server: {exc}\nTry another port with --port.\n")


if __name__ == "__main__":
    main()
