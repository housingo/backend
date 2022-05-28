FROM python:3.10-alpine

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
ENV PORT=${PORT}
ENV DB_STRING={DB_STRING}
ENV JWT_SECRET={JWT_SECRET}

CMD exec uvicorn server:app --port $PORT --host 0.0.0.0
EXPOSE $PORT