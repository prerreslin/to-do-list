from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase,mapped_column,Mapped

engine = create_engine("sqlite:///tasks.db",echo=True)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)

class Tasks(Base):
    __tablename__ = "tasks"
    task: Mapped[str]

Base.metadata.create_all(bind=engine)