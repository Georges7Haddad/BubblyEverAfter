FROM python:3.7.3-alpine3.10

WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

RUN apk add --virtual .build-deps postgresql-dev build-base
RUN apk add jpeg-dev zlib-dev

# Install requirements
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt


COPY . /app

EXPOSE 8000

CMD ["sh", "start.sh"]
