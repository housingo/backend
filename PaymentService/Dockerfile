FROM python:3.10-alpine

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
ENV PORT=${PORT}
ENV DB_STRING=${DB_STRING}
ENV JWT_SECRET={JWT_SECRET}
ENV STRIPE_KEY_LIVE=${STRIPE_KEY_TEST}
ENV STRIPE_KEY_TEST=${STRIPE_KEY_LIVE}

CMD exec uvicorn server:app --port $PORT --host 0.0.0.0
EXPOSE $PORT