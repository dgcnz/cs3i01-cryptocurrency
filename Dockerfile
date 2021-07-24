FROM python:3.9.6-alpine

WORKDIR /usr/src/app

# https://github.com/pyca/cryptography/blob/main/docs/installation.rst#alpine
RUN apk update && apk add \
    cargo \
    gcc \
    libc-dev \
    libffi-dev \
    make \
    musl-dev \
    openssl-dev \
    python3-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
