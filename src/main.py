from fastapi import FastAPI

app = FastAPI(title="FastAPI Shop")

@app.get("/")
async def root():
    return {"message": "Hello World"}