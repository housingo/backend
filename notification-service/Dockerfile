FROM python:3.10-alpine

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
ENV DB_STRING=${DB_STRING}

CMD ["python","server.py"]