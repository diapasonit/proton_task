from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=create_engine('sqlite:///sqlite.txt'))


class DBAdapter:

    @contextmanager
    def get_session(self):
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()
