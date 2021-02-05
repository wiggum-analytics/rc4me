FROM python:3.8

WORKDIR /app/
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY setup.py tox.ini myproject.toml /app/
COPY rc4me /app/rc4me
RUN pip install -e /app/
WORKDIR /app/
