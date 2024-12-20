from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    todos = relationship('ToDo', back_populates='user')
    # Method to check password
    def check_password(self, password):
        return check_password_hash(self.password, password)
# ToDo model
class ToDo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='todos')
    date = Column(String, nullable=False)
    category = Column(String, nullable=False)

# Database setup
engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)
print("Database and tables created successfully.")
# update the app.py addtodo route to include the date field