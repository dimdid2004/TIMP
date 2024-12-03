from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from algorithms.scytale import encrypt_scytale, decrypt_scytale
from algorithms.scytale import ScytaleError

from algorithms.kardano import encrypt_grille, decrypt_grille
from algorithms.kardano import GrilleError

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/encrypt_scytale")
async def encrypt_scytale_view(request: Request, message: str = Form(...)):
    try:
        encrypted_message, encrypted_key = encrypt_scytale(message)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "encrypted_message": encrypted_message,
            "key": encrypted_key,
            "active_algorithm": "scytale"
        })
    except ScytaleError as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error_message": str(e),
            "active_algorithm": "scytale"
        })

@app.post("/decrypt_scytale")
async def decrypt_scytale_view(request: Request, encrypted_message: str = Form(...), key: str = Form(...)):
    try:
        decrypted_message = decrypt_scytale(encrypted_message, key)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "decrypted_message": decrypted_message,
            "active_algorithm": "scytale"
        })
    except ScytaleError as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error_message": str(e),
            "active_algorithm": "scytale"
        })

@app.post("/encrypt_grille")
async def encrypt_grille_view(request: Request, message: str = Form(...)):
    try:
        encrypted_message, encrypted_code = encrypt_grille(message)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "encrypted_message_grille": encrypted_message,
            "encrypted_code": encrypted_code,
            "active_algorithm": "kardano"
        })
    except GrilleError as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error_message": str(e),
            "active_algorithm": "kardano"
        })

@app.post("/decrypt_grille")
async def decrypt_grille_view(request: Request, encrypted_message: str = Form(...), encrypted_code: str = Form(...)):
    try:
        decrypted_message = decrypt_grille(encrypted_message, encrypted_code)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "decrypted_message_grille": decrypted_message,
            "active_algorithm": "kardano"
        })
    except GrilleError as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error_message": str(e),
            "active_algorithm": "kardano"
        })
