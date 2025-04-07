from database.db_setup import SessionLocal,Tasks

class TasksService:

    @staticmethod
    def get_tasks(**kwargs):
        session = SessionLocal()
        try:
            tasks = session.query(Tasks).filter_by(**kwargs).all()
            return tasks
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_tasks: {e}")
        finally:
            session.close()

    @staticmethod
    def get_task(**kwargs):
        session = SessionLocal()
        try:
            tasks = session.query(Tasks).filter_by(**kwargs).first()
            return tasks
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_task: {e}")
        finally:
            session.close()

    @staticmethod
    def create_task(description,assigned_user_id,project_id):
        session = SessionLocal()
        try:
            new_task = Tasks(description=description, assigned_user_id=assigned_user_id,project_id=project_id)
            session.add(new_task)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"❌ Error in create_task: {e}")
        finally:
            session.close()

    @staticmethod
    def get_task(**kwargs):
        session = SessionLocal()
        try:
            task = session.query(Tasks).filter_by(**kwargs).first()
            return task if task else None
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_task: {e}")
        finally:
            session.close()