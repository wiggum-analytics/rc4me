FROM python:3.8

WORKDIR /app/
COPY rc4me /app/rc4me
COPY setup.py tox.ini myproject.toml /app/
RUN pip install -e /app/
COPY requirements.txt /app
RUN pip install -r requirements.txt
WORKDIR /app/
