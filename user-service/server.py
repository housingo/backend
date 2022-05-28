from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routes import router as api_router

app = FastAPI()
origins = ["http://localhost:3000", "localhost:3000", "https://housingo.nl"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def index():
    return "Hi!"


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True,
        log_level="info",
    )
