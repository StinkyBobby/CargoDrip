import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from src.config.db_data import settings
from src.routers import get_apps_routes

app = FastAPI(title=settings.DB_NAME)



# Шаблоны (если используешь Jinja2)
templates = Jinja2Templates(directory="frontend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
for router in get_apps_routes():
    app.include_router(router)

# Статика
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Главная страница
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h2>Добро пожаловать!</h2>
    <p>Открой <a href='/docs'>Swagger</a> или <a href='/trucks-page'>таблицу грузовиков</a>.</p>
    """

# HTML-страница
@app.get("/trucks-page", response_class=HTMLResponse)
def trucks_page(request: Request):
    try:
        return templates.TemplateResponse("trucktable.html", {"request": request})
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Ошибка загрузки страницы</h1><p>{e}</p>",
            status_code=500
        )

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
