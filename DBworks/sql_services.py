

from sqlalchemy import Inspector, create_engine
from sqlalchemy.orm import Session

from DBworks.models import hability as Hability
from DBworks.models import user as User

engine_created = create_engine('sqlite:///teste.db', echo=True)
inspector = Inspector.from_engine(engine_created)

if not inspector.has_table('users'):
    User.__table__.create(engine_created)

if not inspector.has_table('habilities'):
    Hability.__table__.create(engine_created)


class SQLService:
    engine = engine_created

    @staticmethod
    def get_engine():
        return SQLService.engine

    @staticmethod
    def create_user(name: str, age: int, email: str):
        new_user = User(name=name, age=age, email=email)
        with Session(SQLService.get_engine()) as session:
            session.add(new_user)
            session.commit()


    @staticmethod
    def search_user_by_name(name: str):
        with Session(SQLService.get_engine()) as session:
            return session.query(User).filter_by(name=name).all()

    @staticmethod
    def search_user_by_email(email: str):
        with Session(SQLService.get_engine()) as session:
            return session.query(User).filter_by(email=email).first()

    @staticmethod
    def search_user_by_age(age: int):
        with Session(SQLService.get_engine()) as session:
            return session.query(User).filter_by(age=age).all()

    @staticmethod
    def delete_user(user_name: str = None, user_email: str = None):
        if user_name:
            user = SQLService.search_user_by_name(user_name)
            with Session(SQLService.get_engine()) as session:
                session.delete(user)
                session.commit()
                if user not in session:
                    return 0
                else:
                    return 1

        elif user_email:
            user = SQLService.search_user_by_email(user_email)
            with Session(SQLService.get_engine()) as session:
                session.delete(user)
                session.commit()
                if user not in session:
                    return 0
                else:
                    return 1

    @staticmethod
    def create_hability(user_name:str, hability_name: str, hability_level: int, hability_description: str = None):
        new_hability = Hability(name=hability_name.lower(), level=hability_level, description=hability_description)

        with Session(SQLService.get_engine()) as session:
            session_user = session.query(User).filter_by(name=user_name).first()
            session_user.habilities.append(new_hability)
            session.commit()
        return 0

    @staticmethod
    def search_hability_by_name(hability_name: str, user_id: int):
        with Session(SQLService.get_engine()) as session:
            hability = session.query(Hability).filter_by(name=hability_name.lower(), user_id=user_id).first()
            return hability

    @staticmethod
    def search_habilities_by_user(user_id: int):
        with Session(SQLService.get_engine()) as session:
            habilities = session.query(Hability).filter_by(user_id=user_id).all()
            return habilities

    @staticmethod
    def search_habilities_by_level(hability_level: str, user_id: int):
        with Session(SQLService.get_engine()) as session:
            habilities = session.query(Hability).filter_by(level=hability_level, user_id=user_id).all()
            return habilities

    @staticmethod
    def delete_hability(hability_name: str, user_id: int):
        hability = SQLService.search_hability_by_name(hability_name, user_id)
        if hability:
            with Session(SQLService.get_engine()) as session:
                session.delete(hability)
                session.commit()
                if hability not in session:
                    return 0
                else:
                    return 1


    @staticmethod
    def update_user(user_email: str, user_name: str, user_age: int):
        user = SQLService.search_user_by_email(user_email)
        if user:
            with Session(SQLService.get_engine()) as session:
                session.add(user)
                user.name = user_name
                user.age = user_age
                user.email = user_email
                session.commit()
                return 0
        else:
            return 1


    @staticmethod
    def update_user_email(user_email: str, new_email: str):
        user = SQLService.search_user_by_email(user_email)
        if user:
            with Session(SQLService.get_engine()) as session:
                session.add(user)
                user.email = new_email
                session.commit()
                return 0
        else:
            return 1

if __name__ == '__main__':
    pass
