FROM python:3.12

RUN mkdir /app

WORKDIR /app/redist-insight-config

COPY requirements.txt .
COPY main.py .

RUN pip install -r ./requirements.txt

CMD [ "python", "./main.py"]
