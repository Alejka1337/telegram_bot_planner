from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from settings import DATABASE_TYPE, USERNAME, PASSWORD, PORT, DATABASE_NAME

engine = create_engine(f"{DATABASE_TYPE}://{USERNAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}", echo=True)
Base = declarative_base()


class Task(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True)
    task_name = Column(String(250), nullable=False)
    status = Column(Boolean, default=False)
    task_date = Column(Date)
    priority = Column(Integer, default=5)
    regular = Column(Boolean, default=False)
    username = Column(Integer, ForeignKey("Users.id"))
    User = relationship("User")

    def __repr__(self):
        return f"{self.id} | {self.task_name} | {self.status} | {self.task_date} | {self.priority} | {self.regular}"


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    city = Column(String(50))
    phone = Column(String(15))
    task = relationship("Task")

    def __repr__(self):
        return f"ID = {self.id} | Username = {self.username}, City = {self.city}, Phone = {self.phone}"


Base.metadata.create_all(engine)
