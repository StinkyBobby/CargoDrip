import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from src.config.db_data import settings
from src.routers import get_apps_routes

app = FastAPI(title=settings.DB_NAME)

templates = Jinja2Templates(directory="frontend")


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

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h2>Добро пожаловать!</h2>
    <p>Открой <a href='/docs'>Swagger</a> или <a href='/trucks-page'>таблицу грузовиков</a>.</p>
    """


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    try:
        return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Ошибка загрузки страницы</h1><p>{e}</p>",
            status_code=500
        )
        
@app.get("/admin_dashboard", response_class=HTMLResponse)
def admin_dashboard_page(request: Request):
    try:
        return templates.TemplateResponse("admin_dashboard.html", {"request": request})
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Ошибка загрузки страницы</h1><p>{e}</p>",
            status_code=500
        )

@app.get("/driver_dashboard", response_class=HTMLResponse)
def driver_dashboard_page(request: Request):
    try:
        return templates.TemplateResponse("driver_dashboard.html", {"request": request})
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Ошибка загрузки страницы</h1><p>{e}</p>",
            status_code=500
        )

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
