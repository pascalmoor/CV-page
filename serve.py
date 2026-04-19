"""Dev server: rebuild on file change, live-reload the browser."""

import os
import socket
from pathlib import Path

from livereload import Server

from build import build

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
HOST = "127.0.0.1"
DEFAULT_PORT = int(os.environ.get("PORT", "8000"))


def find_free_port(host: str, start: int, attempts: int = 20) -> int:
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return port
            except OSError:
                continue
    raise RuntimeError(
        f"No free port in range {start}–{start + attempts - 1}. "
        f"Free one with e.g. `lsof -iTCP:{start} -sTCP:LISTEN` and kill the process, "
        f"or set PORT=<other>."
    )


def main() -> None:
    build()
    port = find_free_port(HOST, DEFAULT_PORT)
    if port != DEFAULT_PORT:
        print(f"  port {DEFAULT_PORT} is busy — using {port} instead")

    server = Server()
    server.watch(str(ROOT / "content"), build)
    server.watch(str(ROOT / "templates"), build)
    server.watch(str(ROOT / "static"), build)
    server.serve(root=str(DIST), port=port, host=HOST, open_url_delay=1)


if __name__ == "__main__":
    main()
