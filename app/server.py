"""Serve the local simulated transfer quotation application."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os


APP_DIRECTORY = Path(__file__).resolve().parent


class AppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, directory=str(APP_DIRECTORY), **kwargs)


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    print(f"Serving simulated transfer app at http://{host}:{port}")
    ThreadingHTTPServer((host, port), AppHandler).serve_forever()
