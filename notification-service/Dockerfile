FROM python:3.10-alpine

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
ENV DB_STRING=${DB_STRING}

CMD exec python3 server.py