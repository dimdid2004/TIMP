from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# Подключаем папку с шаблонами
templates = Jinja2Templates(directory="templates")

# Маршрут для первого шаблона
@app.get("/template1")
async def render_template1(request: Request):
    return templates.TemplateResponse("template1.html", {"request": request, "message": "Это сообщение для первого шаблона"})

# Маршрут для второго шаблона
@app.get("/template2")
async def render_template2(request: Request):
    return templates.TemplateResponse("template2.html", {"request": request, "message": "Это сообщение для второго шаблона"})
