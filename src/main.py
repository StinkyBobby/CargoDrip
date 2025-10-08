import uvicorn
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from src.config.db_data import settings

def get_app() -> FastAPI:
    application = FastAPI(title = settings.DB_NAME)
    # тут потом дописать router и подобное
    return application

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=True,
        allow_methods=["*"],
    )

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