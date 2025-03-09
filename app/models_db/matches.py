from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, update, ForeignKey
from app.database import Base, int_pk, created_at, updated_at
from datetime import datetime

from app.database import async_session_maker as Session
from app.models_pydantic import Match


current_date = datetime.now().strftime("%d.%m.%Y")

class MatchDB(Base):
    __tablename__ = "matches"

    id: Mapped[int_pk]
    match_date: Mapped[str]
    time: Mapped[str]
    scores: Mapped[str]
    owner: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    guest: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    status: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    async def create_match(self, match: Match, session: Session) -> Match:
        session.add(match)
        await session.commit()
        await session.refresh(match)
        return match

    @classmethod
    async def upgrade_match(self, session: Session, new_matches):
        for new_match in new_matches:
            query = select(MatchDB).where(
                MatchDB.match_date == new_match['match_date'],
                MatchDB.owner == new_match['owner']
            )
            result = await session.execute(query)
            match = result.scalar()

            stmt = update(MatchDB).where(
                MatchDB.id == match.id
            ).values(
                scores=new_match["scores"],
                status=new_match["status"]
            )
            await session.execute(stmt)
            await session.commit()


    @classmethod
    async def get_today_events(self, session: Session)-> list[Match]:
        query = select(MatchDB).where(MatchDB.match_date == current_date)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def check_follow(self, session: Session) -> list[Match]:
        query = select(MatchDB.time, MatchDB.owner, MatchDB.guest).where(MatchDB.match_date == current_date)
        result = await session.execute(query)
        return result.all()