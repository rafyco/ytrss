FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip==21.3.1; \
    pip install --no-cache-dir .; \
    adduser ytrss

USER ytrss

CMD ["python", "-m", "ytrss"]
