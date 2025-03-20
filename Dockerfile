FROM --platform=linux/arm64 python:3.7-alpine

WORKDIR /python-docker

RUN pip install flask

CMD [ "python", "app.py" ]

COPY . .