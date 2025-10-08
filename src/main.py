import uvicorn 
from fastapi import FastAPI 
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




if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        reload=True
    )