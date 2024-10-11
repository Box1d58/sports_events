from fastapi import FastAPI
import uvicorn
from routes import today_matches


app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
