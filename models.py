from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    video_filename = Column(String)

class TestGroup(Base):
    __tablename__ = "test_groups"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    questions = relationship("TestQuestion", back_populates="group")

class TestQuestion(Base):
    __tablename__ = "test_questions"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("test_groups.id"))
    question = Column(Text)
    answer = Column(String)

    group = relationship("TestGroup", back_populates="questions")

class UserAnswer(Base):
    __tablename__ = "user_answers"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("test_questions.id"))
    user_answer = Column(String)
