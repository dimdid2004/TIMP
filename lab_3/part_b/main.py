from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import get_db, Base, engine
from database import add_user_inf
from models import UserRegister
from sqlalchemy.orm import Session

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники (или ограничь нужными доменами)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

Base.metadata.create_all(bind=engine)

# Подключаем папку для html
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "API работает!"}

# Маршрут для получения данных от клиента
@app.post("/submit-info")
async def submit_info(request: Request, client_info: UserRegister, db: Session=Depends(get_db)):
    # Получение IP-адреса клиента
    ip_address = request.client.host
    
    add_user_inf(db, ip_address, client_info)

    return {"message": "Информация успешно сохранена"}