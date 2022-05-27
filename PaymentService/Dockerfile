FROM python:3.10-alpine

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
ENV PORT=${PORT}
ENV DB_STRING=mongodb+srv://housingo:housingodb@cluster0.ea4of.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
ENV JWT_SECRET=housingosecret
ENV STRIPE_KEY_LIVE=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
ENV STRIPE_KEY_TEST=sk_test_51KRM7EDZMSJnOXe4N6AmuTC8h5EAbYgZyRrDluQ3FOSZlc23wrI0aJJhAkO2JikZul85LeOvpIg0RhFoAsrrwRGq008FEfmSka

CMD exec uvicorn server:app --port $PORT --host 0.0.0.0
EXPOSE $PORT