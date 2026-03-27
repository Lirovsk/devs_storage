from typing import Optional
import uuid

from sqlalchemy import ForeignKey, Integer, Column, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_security import UserMixin, RoleMixin 
from flask_security.models import sqla as sqla

class Base(DeclarativeBase):
    pass


sqla.FsModels.set_db_info(db_adapter='sqlalchemy', db=Base)


role_user = Table(
    'role_user',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class user(Base, UserMixin):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    fs_uniquifier: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(default=True)
    roles: Mapped[list['role']] = relationship('role', secondary=role_user, back_populates='users')



    def __str__(self):
        return f"User(name={self.name}, age={self.age}, email={self.email})"
    
class role(Base, RoleMixin):
    __tablename__ = 'roles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    users: Mapped[list['user']] = relationship('user', secondary=role_user, back_populates='roles')

    def __str__(self):
        return f"Role(name={self.name}, description={self.description})"
