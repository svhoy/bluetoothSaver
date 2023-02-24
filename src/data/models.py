from typing import Optional
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.sql.schema import Column
from sqlmodel import Field, SQLModel

class Test(SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class DataStorage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    test_id: int = Field(foreign_key="test.id")
    distance: float 
