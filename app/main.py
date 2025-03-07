import uvicorn

from fastapi import FastAPI

from app.routes.today_matches import router
from app.routes.get_today_matches import router_2
from app.routes.get_events_in_db import router_events
from app.routes.upgrade_events import router_upgrade
from app.routes.teams_add import router_team


app = FastAPI()
app.include_router(router)
app.include_router(router_2)
app.include_router(router_upgrade)
app.include_router(router_events)
app.include_router(router_team)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
