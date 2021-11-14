from sqlmodel import Session, SQLModel, create_engine

from .settings import settings
from .filesystem import working_directory
from .models import Test, DataStorage

with working_directory(settings.project_root):
    engine = create_engine(settings.database_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class SQLiteRepository:
    def __init__(self):
        self.engine = engine

    def reset(self):
        SQLModel.metadata.drop_all(self.engine)
        create_db_and_tables()

    # Test
    async def add_test(self, test: Test) -> Test:
        with Session(self.engine) as session:
            session.add(test)
            session.commit()
            session.refresh(test)
        return test
    
    async def get_tests(self, ) -> list[Test]:
        with Session(self.engine) as session:
            test_list = session.query(Test)
        return test_list

    async def add_data(self, data: DataStorage) -> DataStorage:
        with Session(self.engine) as session:
            session.add(data)
            session.commit()
            session.refresh(data)
        return data

    

repository = SQLiteRepository()