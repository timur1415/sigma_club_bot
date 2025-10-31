from server.fastapi_init import init_fastapi_app
import uvicorn


app = init_fastapi_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
