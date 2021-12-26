FROM python:3.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m pip install --upgrade pip

WORKDIR /nsfw_bot/

COPY requirements.txt /nsfw_bot/
RUN pip3 install -r requirements.txt

COPY . /nsfw_bot/

ENTRYPOINT [ "python3", "ml_bot.py" ]
