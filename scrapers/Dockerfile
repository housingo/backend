FROM python:3.10-alpine

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pip3 install -r requirements.txt

RUN crontab crontab

CMD ["crond","-f"]