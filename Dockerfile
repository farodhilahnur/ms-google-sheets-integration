FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get -y install cron vim

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "./app/_entrypoint.sh"]
