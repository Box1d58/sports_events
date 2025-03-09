from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, update, ForeignKey
from app.database import Base, int_pk, created_at, updated_at
from datetime import datetime

from app.database import async_session_maker as Session
from app.models_pydantic import Follow


current_date = datetime.now().strftime("%d.%m.%Y")

class FollowDB(Base):
    __tablename__ = 'follows'

    user_id: Mapped[int_pk]
    follow_team: Mapped[int] = mapped_column(ForeignKey('teams.id'), nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @classmethod
    async def create_follow(self, new_user_id, follow, session: Session):
        follow = {'user_id': new_user_id,
                   'follow_team': follow}
        query = select(FollowDB.user_id).where(FollowDB.user_id == follow['user_id'])
        result = await  session.execute(query)
        result = result.scalar()
        if result:
            pass
        else:
            follow_instance = FollowDB(**follow)
            session.add(follow_instance)
            await session.commit()
            await session.refresh(follow_instance)
            return follow_instance

    @classmethod
    async def update_follow(self, user_id, team_id, session: Session):
        stmt = update(FollowDB).where(FollowDB.user_id == user_id
                                      ).values(
            follow_team=team_id
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_follow(self, session: Session):
        query = select(FollowDB)
        result = await session.execute(query)
        return result.scalars().all()