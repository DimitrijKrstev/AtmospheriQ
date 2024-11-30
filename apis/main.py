from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def say_hello():
