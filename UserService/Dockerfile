FROM python:3.10-alpine

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
ENV PORT=${PORT}
ENV DB_STRING=mongodb+srv://housingo:housingodb@cluster0.ea4of.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
ENV JWT_SECRET=housingosecret

CMD exec uvicorn server:app --port $PORT --host 0.0.0.0
EXPOSE $PORT