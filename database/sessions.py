from database.db_setup import SessionLocal, Sessions
from utils.encryption import encrypt_data, decrypt_data
import json

class SessionsService:
    @staticmethod
    def set_session(user_id, session_data):
        session = SessionLocal()
        try:
            encrypted_session = encrypt_data(json.dumps(session_data))
            existing_session = session.query(Sessions).filter_by(user_id=user_id).first()

            if existing_session:
                existing_session.encrypted_data = encrypted_session
            else:
                new_session = Sessions(user_id=user_id, encrypted_data=encrypted_session)
                session.add(new_session)

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"❌ Error in set_session: {e}")
        finally:
            session.close()

    @staticmethod
    def check_session(user_id=None):
        session = SessionLocal()
        try:
            query = session.query(Sessions)
            if user_id:
                query = query.filter_by(user_id=user_id)
            user_session = query.first()
            return bool(user_session)
        except Exception as e:
            print(f"❌ Error in check_session: {e}")
            return False
        finally:
            session.close()

    @staticmethod
    def clear_session(user_id):
        session = SessionLocal()
        try:
            session.query(Sessions).filter_by(user_id=user_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"❌ Error in clear_session: {e}")
        finally:
            session.close()

    @staticmethod
    def get_logged_in_user():
        session = SessionLocal()
        try:
            user_session = session.query(Sessions).filter_by().first()
            return user_session
        except Exception as e:
            print(f"❌ Error in check_session: {e}")
            return False
        finally:
            session.close()