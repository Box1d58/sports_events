from fastapi import FastAPI
import uvicorn
from html.parser import HTMLParser

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
