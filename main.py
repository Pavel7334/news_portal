from fastapi import FastAPI

app = FastAPI(
    title="Новостной портал"
)


@app.get("/")
def get_hello():
    return "Hello world"

