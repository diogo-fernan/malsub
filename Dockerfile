FROM python:3.8

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python3", "malsub.py" ]
