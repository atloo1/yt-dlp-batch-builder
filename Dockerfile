# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

# Python quirks:
# [1] don't write pyc files
# [2] don't buffer stdout & stderr; keeps post crash logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# [1] create a less privileged user for running the app
# [2] give this user write permissions in WORKDIR
# https://docs.docker.com/go/dockerfile-user-best-practices/
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --no-create-home \
    --shell "/sbin/nologin" \
    --uid "10001" \
    appuser \
    && \
    chown appuser -R /app/

# download & install dependencies separately to leverage caching
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

# copy source code into WORKDIR, ignoring .dockerignore
COPY . .

# switch to less privileged user
USER appuser

# run application
ENTRYPOINT ["python", "-m", "yt_dlp_batch_builder.main"]
