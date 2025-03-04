from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import select, update, ForeignKey
from app.database import Base, str_uniq, int_pk, created_at, updated_at
from datetime import date, datetime

from app.database import async_session_maker as Session
from app.models_pydantic import Match, Team, User


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

class UsersDB(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    nickname: Mapped[str]
    follow_team: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    created_at: Mapped[created_at]

