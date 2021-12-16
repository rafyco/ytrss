FROM python:3.6-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install .

RUN adduser ytrss

USER ytrss

CMD ["python", "-m", "ytrss.daemon"]
