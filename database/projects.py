from database.db_setup import SessionLocal,Projects

class ProjectsService:

    @staticmethod
    def get_projects(**kwargs):
        session = SessionLocal()
        try:
            projects = session.query(Projects).filter_by(**kwargs).all()
            return projects
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_projects: {e}")
        finally:
            session.close()

    @staticmethod
    def create_project(name,client_id):
        session = SessionLocal()
        try:
            new_project = Projects(name=name, client_id=client_id)
            session.add(new_project)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"❌ Error in create_project: {e}")
        finally:
            session.close()

    @staticmethod
    def get_project(**kwargs):
        session = SessionLocal()
        try:
            project = session.query(Projects).filter_by(**kwargs).first()
            return project if project else None
        except Exception as e:
            session.rollback()
            print(f"❌ Error in get_project: {e}")
        finally:
            session.close()