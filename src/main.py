import uvicorn
from fastapi import FastAPI


def get_app():
    application = FastAPI()

    return application

app = get_app()


#endPoint
@app.get("/")
def root():
    return "Hello World!"

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        reload=True
    )