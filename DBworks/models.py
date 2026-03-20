from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class user(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()
    email: Mapped[str] = mapped_column()
    super_user: Mapped[bool] = mapped_column(default=False)

    habilities: Mapped[list['hability']] = relationship(back_populates='user')


class hability(Base):
    __tablename__ = 'habilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    level: Mapped[int] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(default='No description provided.')
    user_id = mapped_column(ForeignKey('users.id'))

    user: Mapped['user'] = relationship(back_populates='habilities')
