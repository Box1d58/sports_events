from sqlalchemy.orm import Mapped
from sqlalchemy import select
from app.database import Base, int_pk
from datetime import datetime

from app.database import async_session_maker as Session
from app.models_pydantic import Team


current_date = datetime.now().strftime("%d.%m.%Y")

class TeamsDB(Base):
    __tablename__ = 'teams'

    id: Mapped[int_pk]
    title: Mapped[str]

    async def create_team(self, team: Team, session: Session) -> Team:
        session.add(team)
        await session.commit()
        await session.refresh(team)
        return team

    @classmethod
    async def get_team_id(self, session: Session, current_team: str):
        query = select(TeamsDB.id).where(TeamsDB.title == current_team)
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def get_team_title(self, session: Session, current_id: int):
        query = select(TeamsDB.title).where(TeamsDB.id == current_id)
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def get_teams(self, session: Session):
        query = select(TeamsDB)
        result = await session.execute(query)
        return result.scalars().all()