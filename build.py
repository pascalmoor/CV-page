"""Render content/*.yml through templates/ into dist/."""

from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"

EXPECTED_ASSETS = [
    STATIC_DIR / "cv.pdf",
]


def load_content() -> dict:
    context: dict = {}
    for yml in sorted(CONTENT_DIR.glob("*.yml")):
        with yml.open("r", encoding="utf-8") as f:
            context[yml.stem] = yaml.safe_load(f) or {}
    return context


def render_site(context: dict) -> None:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "html.j2"]),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("index.html.j2")
    html = template.render(**context)
    (DIST_DIR / "index.html").write_text(html, encoding="utf-8")


def copy_static() -> None:
    if not STATIC_DIR.exists():
        return
    shutil.copytree(STATIC_DIR, DIST_DIR, dirs_exist_ok=True)


def warn_missing_assets() -> list[str]:
    missing = [str(p.relative_to(ROOT)) for p in EXPECTED_ASSETS if not p.exists()]
    for m in missing:
        print(f"  warning: expected asset missing — {m}", file=sys.stderr)
    return missing


def summary() -> None:
    files = list(DIST_DIR.rglob("*"))
    total_bytes = sum(p.stat().st_size for p in files if p.is_file())
    file_count = sum(1 for p in files if p.is_file())
    print(f"  {file_count} files, {total_bytes / 1024:.1f} KB written to {DIST_DIR.relative_to(ROOT)}/")


def build() -> None:
    print("Building site…")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    context = load_content()
    context["build_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    render_site(context)
    copy_static()
    warn_missing_assets()
    summary()
    print("Done.")


if __name__ == "__main__":
    build()
