#! /bin/bash

export PROJECT_ID=housingo-350313
export REGION=europe-west4
export PORT=8000

gcloud builds submit \
    --tag gcr.io/$PROJECT_ID/housingo \
    --project $PROJECT_ID

gcloud run deploy housingo \
    --image gcr.io/$PROJECT_ID/housingo \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --project $PROJECT_ID \
    --port $PORT