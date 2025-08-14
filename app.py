from fastapi import FastAPI, Request, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from crud import *
import shutil
from ai_resume import analyze_text_resume, analyze_video_resume

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/resume", response_class=HTMLResponse)
def resume_form(request: Request):
    return templates.TemplateResponse("resume_form.html", {"request": request})

# @app.post("/resume", response_class=HTMLResponse)
# async def submit_resume(request: Request, text_resume: str = Form(...), video: UploadFile = File(...), db: Session = Depends(get_db)):
#     video_path = f"static/{video.filename}"
#     with open(video_path, "wb") as f:
#         shutil.copyfileobj(video.file, f)

#     create_resume(db, text_resume, video.filename)
#     ai_result = analyze_text_resume(text_resume)

#     return templates.TemplateResponse("resume_form.html", {"request": request, "message": "Резюме успешно отправлено!", "ai_result": ai_result})

# Обработка текстового резюме (только текст)
@app.post("/resume/text", response_class=HTMLResponse)
async def submit_text_resume(request: Request, text_resume: str = Form(...)):
    # Анализ текста резюме
    ai_result = analyze_text_resume(text_resume)
    message = "Текстовое резюме успешно отправлено и проанализировано!"
    return templates.TemplateResponse("resume_form.html", {
        "request": request,
        "message": message,
        "ai_result": ai_result
    })

# Обработка видео резюме (только видео)
@app.post("/resume/video", response_class=HTMLResponse)
async def submit_video_resume(request: Request, video: UploadFile = File(...), db: Session = Depends(get_db)):
    video_path = f"static/{video.filename}"
    with open(video_path, "wb") as f:
        shutil.copyfileobj(video.file, f)

    create_resume(db, text="", video_filename=video.filename)

    ai_result = analyze_video_resume(video_path)
    message = "Видео успешно проанализировано!"

    return templates.TemplateResponse("resume_form.html", {
        "request": request,
        "message": message,
        "ai_result": ai_result
    })


# === Новый функционал тестов ===

@app.get("/tests", response_class=HTMLResponse)
def list_test_groups(request: Request, db: Session = Depends(get_db)):
    groups = get_all_test_groups(db)
    return templates.TemplateResponse("test_groups.html", {"request": request, "groups": groups})

@app.get("/tests/{group_id}", response_class=HTMLResponse)
def show_test(request: Request, group_id: int, db: Session = Depends(get_db)):
    group = get_test_group(db, group_id)
    return templates.TemplateResponse("tests.html", {"request": request, "tests": group.questions, "group": group})

@app.post("/tests/{group_id}", response_class=HTMLResponse)
async def submit_answers(request: Request, group_id: int, db: Session = Depends(get_db)):
    form = await request.form()
    correct_count = 0
    total = 0

    for question_id_str, user_answer in form.items():
        try:
            question_id = int(question_id_str)
        except ValueError:
            continue
        
        total += 1
        correct_answer = get_question_answer(db, question_id)
        if correct_answer is not None and user_answer.strip().lower() == correct_answer.strip().lower():
            correct_count += 1
        
        save_user_answer(db, question_id, user_answer)

    percent = (correct_count / total * 100) if total > 0 else 0

    group = get_test_group(db, group_id)
    return templates.TemplateResponse("tests.html", {
        "request": request,
        "tests": group.questions,
        "group": group,
        "message": f"Вы ответили правильно на {correct_count} из {total} вопросов.",
        "percent": f"{percent:.2f}%"
    })


@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db)):
    groups = get_all_test_groups(db)
    return templates.TemplateResponse("admin.html", {"request": request, "groups": groups})

@app.post("/admin/group", response_class=HTMLResponse)
def add_group(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    add_test_group(db, title)
    groups = get_all_test_groups(db)
    return templates.TemplateResponse("admin.html", {"request": request, "message": "Тест-группа добавлена!", "groups": groups})

@app.post("/admin/question", response_class=HTMLResponse)
def add_question(request: Request, group_id: int = Form(...), question: str = Form(...), answer: str = Form(...), db: Session = Depends(get_db)):
    add_question_to_group(db, group_id, question, answer)
    groups = get_all_test_groups(db)
    return templates.TemplateResponse("admin.html", {"request": request, "message": "Вопрос добавлен!", "groups": groups})
