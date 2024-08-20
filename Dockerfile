FROM python:3.12-alpine

RUN mkdir /app

WORKDIR /app/redist-insight-config

COPY requirements.txt .
COPY main.py .

RUN pip install -r ./requirements.txt

CMD [ "python", "./main.py"]
