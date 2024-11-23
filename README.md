# yt-dlp-batch-builder

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/atloo1/yt-dlp-batch-builder/ci.yaml)](https://github.com/atloo1/yt-dlp-batch-builder/actions/workflows/ci.yaml?query=branch%3Amain)
[![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fatloo1%2Fyt-dlp-batch-builder%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.dependencies.python&label=python)](https://github.com/atloo1/yt-dlp-batch-builder/blob/main/pyproject.toml)
[![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fatloo1%2Fyt-dlp-batch-builder%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.version&label=version)](https://github.com/atloo1/yt-dlp-batch-builder/blob/main/pyproject.toml)
[![GitHub License](https://img.shields.io/github/license/atloo1/yt-dlp-batch-builder)](https://github.com/atloo1/yt-dlp-batch-builder/blob/main/LICENSE)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/atloo1/yt-dlp-batch-builder)

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://renovatebot.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Download your YouTube "Watch later" playlist w/ only Docker as a prerequisite.

The `yt-dlp-batch-builder` container runs a Python parser of the HTML of your "Watch later" playlist. This is used over the API, which [requires authentication in a browser](https://developers.google.com/youtube/v3/quickstart/python), just creating an extra step. `yt_dlp_batch.txt` results, which is input for the `yt-dlp` container whose arguments are [documented here](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#usage-and-options). Here, 720p videos favoring open codecs & containers (AV1, VP9, Opus, WebM) truncated by [SponsorBlock](https://github.com/ajayyy/SponsorBlock?tab=readme-ov-file#sponsorblock) are downloaded. Intermediate files & containers are also cleaned up.

## prerequisites

```
git clone https://github.com/atloo1/yt-dlp-batch-builder.git
cd yt-dlp-batch-builder/
```

## run with Docker:

### prerequisites

- [docker](https://docs.docker.com/get-started/get-docker/)

```
docker build . -t yt_dlp_batch_builder
```

### part 1

Download [your YouTube "Watch later" playlist](https://www.youtube.com/playlist?list=WL). Defaults are assumed: `C:\Users\$env:USERNAME\Downloads\"Watch later - YouTube.htm"` for Windows & `~/Downloads/"Watch later - YouTube.html"` for Unix.

```
cd <this-repo-root>
docker build . -t yt-dlp-batch-builder
```

### part 2: Windows (PowerShell)

#### programmatic

```
Rename-Item -Path C:\Users\$env:USERNAME\Downloads\"Watch later - YouTube.htm" -NewName watch_later.html
docker run `
    -v C:\Users\$env:USERNAME\Downloads\watch_later.html:/app/watch_later.html `
    --name yt-dlp-batch-builder `
    yt-dlp-batch-builder `
    --input-filepath watch_later.html `
    --output-filepath yt_dlp_batch.txt
docker cp yt-dlp-batch-builder:/app/yt_dlp_batch.txt C:\Users\$env:USERNAME\Downloads
# optionally edit yt_dlp_batch.txt
docker run `
    -v C:\Users\$env:USERNAME\Downloads\yt_dlp_batch.txt:/downloads/yt_dlp_batch.txt `
    --name yt-dlp `
    jauderho/yt-dlp:latest `
    -a yt_dlp_batch.txt `
    -f "bv[height=720]+ba[acodec=opus][ext=webm]" `
    -o "%(title)s_%(channel)s.%(ext)s" `
    --embed-chapters `
    --embed-subs `
    --exec 'mv {} $(echo {} | tr "[:upper:]" "[:lower:]")' `
    --restrict-filenames `
    --sponsorblock-remove all
docker cp yt-dlp:/downloads/. C:\Users\$env:USERNAME\Videos\youtube
rm C:\Users\$env:USERNAME\Downloads\"Watch later - YouTube_files\" -Recurse
rm C:\Users\$env:USERNAME\Downloads\watch_later.html
rm C:\Users\$env:USERNAME\Downloads\yt_dlp_batch.txt
rm C:\Users\$env:USERNAME\Videos\youtube\yt_dlp_batch.txt
```

#### interactive

```
docker run `
    --name yt-dlp `
    --entrypoint /bin/sh `
    jauderho/yt-dlp:latest `
    -c "sleep infinity"
docker exec -it yt-dlp /bin/sh
```

### part 2: Unix (Bash)

#### programmatic

```
mv ~/Downloads/"Watch later - YouTube.html" ~/Downloads/watch_later.html
docker run \
    -v ~/Downloads/watch_later.html:/app/watch_later.html \
    --name yt-dlp-batch-builder \
    yt-dlp-batch-builder \
    --input-filepath watch_later.html \
    --output-filepath yt_dlp_batch.txt
docker cp yt-dlp-batch-builder:/app/yt_dlp_batch.txt ~/Downloads/
# optionally edit yt_dlp_batch.txt
docker run \
    -v ~/Downloads/yt_dlp_batch.txt:/downloads/yt_dlp_batch.txt \
    --name yt-dlp \
    jauderho/yt-dlp:latest \
    -a yt_dlp_batch.txt \
    -f "bv[height=720]+ba[acodec=opus][ext=webm]" \
    -o "%(title)s_%(channel)s.%(ext)s" \
    --embed-chapters \
    --embed-subs \
    --exec 'mv {} $(echo {} | tr "[:upper:]" "[:lower:]")' \
    --restrict-filenames \
    --sponsorblock-remove all
docker cp yt-dlp:/downloads/. ~/Videos/youtube
rm ~/Downloads/watch_later.html
rm ~/Downloads/yt_dlp_batch.txt
rm ~/Videos/youtube/yt_dlp_batch.txt
```

#### interactive

```
docker run \
    --name yt-dlp \
    --entrypoint /bin/sh \
    jauderho/yt-dlp:latest \
    -c "sleep infinity"
docker exec -it yt-dlp /bin/sh
```

### part 3

```
docker rm yt-dlp-batch-builder yt-dlp
```

## use with Python interpreter:

### prerequisites

- [poetry](https://python-poetry.org/docs/#installing-with-pipx)

### run

```
poetry run python -m yt_dlp_batch_builder.main
```

### develop

#### prerequisites

- [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

#### 1st time setup

```
pyenv install 3.9 --skip-existing   # or your choice
pyenv local 3.9   # or your choice
poetry install
poetry run pre-commit install
```
