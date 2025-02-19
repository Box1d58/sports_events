import uvicorn


from fastapi import FastAPI
from app.routes.today_matches import router
from app.routes.get_events import router_1

app = FastAPI()
app.include_router(router)
app.include_router(router_1)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
