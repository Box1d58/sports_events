from pydantic import BaseModel
from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date

class Match(Base):
    id: Mapped[int_pk]
    match_date: Mapped[str]
    owner: Mapped[str]
    guest: Mapped[str]

    def __str__(self):
        return f"{self.__class__.__name__}(id = {self.id}, owner = {self.owner}, guest = {self.guest})"

    def __repr__(self):
        return str(self)