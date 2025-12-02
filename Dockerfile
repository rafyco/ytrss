FROM python:3.12-slim AS builder

WORKDIR /app

COPY . /app

RUN apt-get update; \
    apt-get install git -y;

RUN pip install --no-cache-dir .

FROM python:3.12-slim

COPY --from=builder /usr/local/lib /usr/local/lib
COPY --from=builder /usr/local/bin /usr/local/bin

RUN apt-get update; \
    apt-get install ffmpeg -y; \
    adduser -u 1000 ytrss;

USER ytrss

RUN mkdir -p /home/ytrss/.config/ytrss/cache; \
    mkdir -p /home/ytrss/.config/ytrss/config; \
    mkdir -p /home/ytrss/.config/ytrss/database; \
    mkdir -p /home/ytrss/podcasts

CMD ["ytrss", "daemon"]
