FROM python:3.9-alpine3.13

WORKDIR /server
COPY . /server

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3"]