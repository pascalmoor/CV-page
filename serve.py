"""Dev server: rebuild on file change, live-reload the browser."""

from pathlib import Path

from livereload import Server

from build import build

ROOT = Path(__file__).parent
DIST = ROOT / "dist"


def main() -> None:
    build()

    server = Server()
    server.watch(str(ROOT / "content"), build)
    server.watch(str(ROOT / "templates"), build)
    server.watch(str(ROOT / "static"), build)
    server.serve(root=str(DIST), port=8000, host="127.0.0.1", open_url_delay=1)


if __name__ == "__main__":
    main()
