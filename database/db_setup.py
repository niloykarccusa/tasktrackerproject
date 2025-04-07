from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from utils.utils import get_db_path


DATABASE_URL = f"sqlite:///{get_db_path()}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)


class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)

    client = relationship("Users")


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    description = Column(String, nullable=False)

    project = relationship("Projects")
    assigned_user = relationship("Users")


class TimeLogs(Base):
    __tablename__ = "time_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=True)

    task = relationship("Tasks")
    user = relationship("Users")

class Sessions(Base):
    __tablename__ = "sessions"

    user_id = Column(Integer, ForeignKey("users.id"),primary_key=True)
    encrypted_data = Column(String, nullable=False)

    user = relationship("Users")

def refresh_object(obj):
    print("Heredb")
    with Session(engine) as session:
        session.refresh(obj)

try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Error creating database tables: {e}")

