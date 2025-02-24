from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import Base, str_uniq, int_pk, created_at, updated_at
from datetime import date, datetime
from typing import Optional

from app.database import async_session_maker as Session
from app.models_pydantic import Match


current_date = datetime.now().strftime("%d.%m.%Y")

class MatchDB(Base):
    __tablename__ = "matches"

    id: Mapped[int_pk]
    match_date: Mapped[str]
    time: Mapped[str]
    owner: Mapped[str]
    guest: Mapped[str]
    created_at: Mapped[created_at]

    def __str__(self):
        return f"{self.__class__.__name__}(id = {self.id}, owner = {self.owner}, guest = {self.guest})"

    def __repr__(self):
        return str(self)

    async def create_match(self, match: Match, session: Session) -> Match:
        session.add(match)
        await session.commit()
        await session.refresh(match)
        return match

    @classmethod
    async def get_today_events(self, session: Session)-> list[Match]:
        query = select(MatchDB).where(MatchDB.match_date == current_date)
        result = await session.execute(query)
        return result.scalars().all()