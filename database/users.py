from database.db_setup import SessionLocal,Users

class UsersService:

    @staticmethod
    def get_user(**kwargs):
        session = SessionLocal()
        try:
            user = session.query(Users).filter_by(**kwargs).first()
            return user if user else None
        except Exception as e:
            session.rollback()
            print(f"❌ Error in set_session: {e}")
        finally:
            session.close()

    @staticmethod
    def get_sub_users():
        session = SessionLocal()
        try:
            users = session.query(Users).filter_by(role='sub').all()
            return users
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_users: {e}")
        finally:
            session.close()

    @staticmethod
    def create_user(username, password, role="super"):
        session = SessionLocal()
        try:
            existing_user = session.query(Users).filter_by(username=username).first()
            if existing_user:
                session.close()
                return False
            if role not in ['super','sub']:
                role='sub'
            new_user = Users(username=username, password=password, role=role)
            session.add(new_user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"❌ Error in set_session: {e}")
        finally:
            session.close()