from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.orm import relationship
import models

Base = declarative_base()
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserInformation(Base):
    __tablename__ = "user_information"
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String)
    user_agent = Column(String)
    os = Column(String)
    cores = Column(Integer)
    graphical_inf = Column(String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_user_inf(db: Session, ip: str, user: models.UserRegister):
    new_user_inf = UserInformation(ip_address=ip, user_agent=user.user_agent, os=user.os, cores=user.cores, graphical_inf=user.graphical_inf)
    db.add(new_user_inf)
    db.commit()
    db.refresh(new_user_inf)




