import re
import sqlite3
import unicodedata
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "knowledge.db"

app = FastAPI(title="Chat con Adquisición del Conocimiento")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Utilidades

def normalizar(texto: str) -> str:
    """
    Normaliza para lograr match "perfecto" más realista:
    - minúsculas
    - sin acentos
    - sin signos
    - espacios limpios
    """
    texto = texto.strip().lower()

    # quitar acentos (cómo -> como)
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

    # quitar signos/puntuación (deja letras, números y espacios)
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def db_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_norm TEXT UNIQUE NOT NULL,
            question_raw  TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    # Semilla: 3 conocimientos básicos (también coincide con las 3 líneas precargadas)
    seed = [
        ("hola", "Hola", "¡Hola! 👋 ¿Cómo estás?"),
        ("como estas", "¿Cómo estás?", "Bien 🙂 ¿y tú cómo estás?"),
        ("de que te gustaria hablar", "¿De qué te gustaría hablar?",
         "Podemos hablar de IA, videojuegos, escuela o proyectos. Tú dime 😄")
    ]

    for qn, qr, a in seed:
        try:
            cur.execute(
                "INSERT INTO knowledge (question_norm, question_raw, answer, created_at) VALUES (?, ?, ?, ?)",
                (qn, qr, a, datetime.now().isoformat())
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()


def buscar_respuesta(question_norm: str):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT answer FROM knowledge WHERE question_norm = ?", (question_norm,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def guardar_conocimiento(question_raw: str, answer: str):
    qn = normalizar(question_raw)
    conn = db_conn()
    cur = conn.cursor()
    # INSERT OR REPLACE para permitir actualizar conocimiento si repites la pregunta
    cur.execute("""
        INSERT OR REPLACE INTO knowledge (question_norm, question_raw, answer, created_at)
        VALUES (?, ?, ?, ?)
    """, (qn, question_raw.strip(), answer.strip(), datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Modelos API

class ChatIn(BaseModel):
    message: str


class TeachIn(BaseModel):
    question: str
    answer: str

# Rutas

@app.on_event("startup")
def _startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat")
def chat(payload: ChatIn):
    user_msg = payload.message.strip()
    if not user_msg:
        return JSONResponse({"reply": "Escribe algo 🙂", "matched": False, "need_training": False})

    qn = normalizar(user_msg)
    answer = buscar_respuesta(qn)

    if answer is not None:
        return JSONResponse({"reply": answer, "matched": True, "need_training": False})

    # No hubo match perfecto -> activar adquisición de conocimiento
    prompt = (
        f"No tengo esa respuesta aún. 😅\n"
        f"¿Cuál debería ser la respuesta correcta cuando alguien pregunte:\n"
        f"“{user_msg}”?\n\n"
        f"Escríbela y la guardaré en mi base de conocimientos."
    )
    return JSONResponse({
        "reply": prompt,
        "matched": False,
        "need_training": True,
        "question_to_learn": user_msg
    })


@app.post("/api/teach")
def teach(payload: TeachIn):
    q = payload.question.strip()
    a = payload.answer.strip()

    if not q or not a:
        return JSONResponse({"ok": False, "msg": "Falta pregunta o respuesta."}, status_code=400)

    guardar_conocimiento(q, a)
    return JSONResponse({"ok": True, "msg": "¡Listo! Ya aprendí esa respuesta. ✅"})