from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import os
import openai

app = FastAPI()

# متغیر محیطی OPENAI_API_KEY را بعداً تنظیم می‌کنیم
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")
    if not question:
        return {"error": "question missing"}

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    answer = response.choices[0].message.content
    return {"answer": answer}
