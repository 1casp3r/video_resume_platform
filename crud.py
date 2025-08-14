from sqlalchemy.orm import Session
from models import Resume, TestGroup, TestQuestion, UserAnswer

def create_resume(db: Session, text, video_filename):
    resume = Resume(text=text, video_filename=video_filename)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume

# === Тесты ===
def get_all_test_groups(db: Session):
    return db.query(TestGroup).all()

def get_test_group(db: Session, group_id: int):
    return db.query(TestGroup).filter(TestGroup.id == group_id).first()

def add_test_group(db: Session, title: str):
    test_group = TestGroup(title=title)
    db.add(test_group)
    db.commit()
    return test_group

def add_question_to_group(db: Session, group_id: int, question: str, answer: str):
    test_question = TestQuestion(group_id=group_id, question=question, answer=answer)
    db.add(test_question)
    db.commit()

def get_questions_by_group(db: Session, group_id: int):
    return db.query(TestQuestion).filter(TestQuestion.group_id == group_id).all()

def save_user_answer(db: Session, question_id: int, answer: str):
    user_answer = UserAnswer(question_id=question_id, user_answer=answer)
    db.add(user_answer)
    db.commit()

def get_question_answer(db: Session, question_id: int):
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if question:
        return question.answer
    return None

