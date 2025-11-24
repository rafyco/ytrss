FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update; \
    apt-get install git ffmpeg -y; \
    adduser ytrss;

RUN pip install --no-cache-dir .

USER ytrss

RUN mkdir -p /home/ytrss/.config/ytrss/cache; \
    mkdir -p /home/ytrss/.config/ytrss/config; \
    mkdir -p /home/ytrss/podcasts

CMD ["ytrss", "run"]
