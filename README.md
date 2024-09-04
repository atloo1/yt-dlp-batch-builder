# yt-dlp-batch-builder

Download your YouTube "Watch later" playlist w/ only [Docker](https://www.docker.com/products/docker-desktop/) as a prerequisite.

The `yt-dlp-batch-builder` container runs a Python parser of the HTML of your "Watch later" playlist. This is used over the API, which [requires authentication in a browser](https://developers.google.com/youtube/v3/quickstart/python), just creating an extra step. `yt_dlp_batch.txt` results, which is input for the `yt-dlp` container whose arguments are [documented here](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#usage-and-options). In summary, 720p VP9 + 128 kbps AAC videos truncated by [SponsorBlock](https://github.com/ajayyy/SponsorBlock?tab=readme-ov-file#sponsorblock) are downloaded. Intermediate files & containers are also cleaned up.

## Usage instructions:

### Part 1
Download [your YouTube "Watch later" playlist](https://www.youtube.com/playlist?list=WL). Defaults are assumed: `C:\Users\$env:USERNAME\Downloads\"Watch later - YouTube.htm"` for Windows & `~/Downloads/"Watch later - YouTube.html"` for Unix.
```
cd <this-repo-root>
docker build . -t yt-dlp-batch-builder
```

### Part 2: Windows (PowerShell)

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
    -f 609+140 `
    -o "%(title)s_%(channel)s.%(ext)s" `
    --embed-chapters `
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

### Part 2: Unix (Bash)

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
    -f 609+140 \
    -o "%(title)s_%(channel)s.%(ext)s" \
    --embed-chapters \
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


### Part 3
```
docker rm yt-dlp-batch-builder yt-dlp
```

## For developers:

### Prerequisites
[poetry](https://github.com/python-poetry/install.python-poetry.org?tab=readme-ov-file#python-poetry-installer)

### Instructions:
```
cd <this-repo-root>
poetry install
poetry run pre-commit install
```
