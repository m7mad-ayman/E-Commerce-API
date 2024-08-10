FROM python:3.12-rc-alpine


ENV PYTHONUNBUFFERED=1

WORKDIR /app/

COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

COPY . /app/