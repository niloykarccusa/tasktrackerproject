from database.db_setup import SessionLocal,TimeLogs,refresh_object

class TimeLogsService:

    @staticmethod
    def get_time_logs(**kwargs):
        session = SessionLocal()
        try:
            time_logs = session.query(TimeLogs).filter_by(**kwargs).all()
            return time_logs
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_time_logs: {e}")
        finally:
            session.close()

    @staticmethod
    def get_distinct_tasks(**kwargs):
        session = SessionLocal()
        try:
            tasks = session.query(TimeLogs.task_id).distinct().all()
            return [task_id[0] for task_id in tasks]
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_distinct_tasks: {e}")
        finally:
            session.close()

    @staticmethod
    def get_ordered_time_logs(**kwargs):
        session = SessionLocal()
        try:
            time_logs = session.query(TimeLogs).filter_by(**kwargs).order_by(TimeLogs.task_id,TimeLogs.start_time.desc()).all()
            return time_logs
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_ordered_time_logs: {e}")
        finally:
            session.close()

    @staticmethod
    def create_time_logs(user_id,task_id,start_time):
        session = SessionLocal()
        try:
            new_time_logs = TimeLogs(user_id=user_id, task_id=task_id,start_time=start_time)
            session.add(new_time_logs)
            session.commit()
            # refresh_object(new_time_logs)
            return True
        except Exception as e:
            session.rollback()
            print(f"❌ Error in create_time_logs: {e}")
        finally:
            session.close()

    @staticmethod
    def update_time_logs(user_id,task_id,end_time):
        session = SessionLocal()
        try:
            log=session.query(TimeLogs).filter_by(user_id=user_id, task_id=task_id,end_time=None).first()
            if log:
                log.end_time=end_time
                session.commit()
                # refresh_object(log)
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"❌ Error in update_time_logs: {e}")
        finally:
            session.close()

    @staticmethod
    def get_time_log(**kwargs):
        session = SessionLocal()
        try:
            time_log = session.query(TimeLogs).filter_by(**kwargs).first()
            return time_log if time_log else None
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_time_logs: {e}")
        finally:
            session.close()

    @staticmethod
    def is_timer_active(user_id,task_id):
        session = SessionLocal()
        try:
            log = session.query(TimeLogs).filter_by(user_id=user_id, task_id=task_id,end_time=None).first()
            return bool(log)
        except Exception as e:
            session.rollback()
            print(f"❌ Error in is_timer_active: {e}")
        finally:
            session.close()

    @staticmethod
    def is_any_timer_active(user_id):
        session = SessionLocal()
        try:
            logs = session.query(TimeLogs).filter_by(user_id=user_id,end_time=None).all()
            for log in logs:
                session.refresh(log)
            return bool(logs)
        except Exception as e:
            session.rollback()
            print(f"❌ Error in is_any_timer_active: {e}")
        finally:
            session.close()