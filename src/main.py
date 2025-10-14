from fastapi.staticfiles import StaticFiles
import uvicorn 
from fastapi import FastAPI 
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routers import get_apps_routes

from src.config.db_data import settings

def get_app() -> FastAPI:
    application = FastAPI(title = settings.DB_NAME)
    # тут потом дописать router и подобное

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=True,
        allow_methods=["*"],
    )
    
    application.include_router(
        get_apps_routes()
    )
    return application


app = get_app()


@app.get("/")
def root():
    return "Hello World!"


# Подключаем папку static (если используешь картинки, CSS и т.п.)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Роут для HTML-страницы
@app.get("/trucks-page", response_class=HTMLResponse)
def trucks_page():
    try:
        with open("frontend/trucktable.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return HTMLResponse(content=f"<h1>Ошибка загрузки страницы</h1><p>{e}</p>", status_code=500)



if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        reload=True
    )