# CV landing page — Pascal Moor

A single-page Python-generated static site for a med-tech / IVD CV landing page.
Content lives in YAML, templates in Jinja2, output is plain HTML/CSS/JS.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python build.py                    # one-shot build → dist/
python serve.py                    # dev server with live-reload at http://127.0.0.1:8000
```

## Editing the page

Everything you'd normally change lives in `content/`:

| File | What it controls |
| --- | --- |
| `profile.yml` | name, title, tagline, CTAs, contact links, open-to status, hero photo, intro video |
| `skills.yml` | radar chart axes (6–8 items, values 0–100) |
| `timeline.yml` | career milestones, most recent first |
| `certifications.yml` | regulatory credentials (ISO 13485, IVDR, FDA 510(k), ...) |
| `metrics.yml` | headline numbers shown below the hero |
| `testimonials.yml` | 2–3 quotes pulled from LinkedIn / colleagues |

After editing, either:

- run `python build.py` to regenerate `dist/`, or
- keep `python serve.py` running — the browser refreshes on save.

## Swapping placeholder assets

- **Professional photo** — drop the file into `static/img/` and point `profile.photo.src` at it (e.g. `/img/pascal.jpg`).
- **CV PDF** — drop at `static/cv.pdf` (the filename the `Download CV` button expects).
- **Intro video** — drop at `static/video/intro.mp4` and set `profile.video.src: /video/intro.mp4`.
- **Open-to status** — change `profile.open_to` to `actively_looking`, `open`, or `not_looking`.

The build warns in stderr if expected assets are missing.

## Deployment (GitHub Pages)

1. Push this repo to GitHub.
2. Repo → **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Push to `main` → `.github/workflows/deploy.yml` builds and publishes automatically.

For a custom domain, add a `static/CNAME` file with your domain and configure DNS per GitHub's docs.

## Project layout

```
.
├── build.py              # YAML + templates → dist/
├── serve.py              # dev server with live-reload
├── requirements.txt
├── content/              # everything you edit (YAML)
├── templates/            # Jinja2 templates + partials
├── static/               # CSS, JS, images, video, cv.pdf
├── dist/                 # generated (git-ignored)
└── .github/workflows/    # GitHub Pages deploy
```

## Dependencies

- [Jinja2](https://jinja.palletsprojects.com/) — templating
- [PyYAML](https://pyyaml.org/) — content parsing
- [livereload](https://livereload.readthedocs.io/) — dev-server browser refresh
- [Chart.js](https://www.chartjs.org/) — radar chart (loaded from CDN, no build step)
# CV-page
