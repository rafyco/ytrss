FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
WORKDIR /app

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-dev --no-install-project --extra optional
COPY . /app

RUN apt-get update; \
    apt-get install git wget -y; \
    wget -qO /usr/local/bin/deno.gz https://github.com/denoland/deno/releases/latest/download/deno-x86_64-unknown-linux-gnu.zip; \
    gunzip /usr/local/bin/deno.gz; \
    chmod a+x /usr/local/bin/deno;

RUN uv sync --frozen --no-dev --extra optional


FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app /app
COPY --from=builder /usr/local/bin/deno /usr/local/bin/deno

ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update; \
    apt-get install ffmpeg -y; \
    adduser -u 1000 --disabled-password --gecos "" ytrss

USER ytrss

RUN mkdir -p /home/ytrss/.config/ytrss/cache; \
    mkdir -p /home/ytrss/.config/ytrss/config; \
    mkdir -p /home/ytrss/.config/ytrss/database; \
    mkdir -p /home/ytrss/podcasts

ENTRYPOINT ["ytrss"]
CMD ["daemon"]
