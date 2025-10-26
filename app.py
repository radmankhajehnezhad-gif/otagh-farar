from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import openai

# کلید API را از محیط دریافت می‌کنیم
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# اجازه دسترسی از همه دامنه‌ها (برای کاربران مختلف)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# پوشه جاری را برای Front-end mount می‌کنیم
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# مدل داده‌ای برای سوال کاربر
class Query(BaseModel):
    question: str

# مسیر POST برای دریافت سوال و ارسال جواب
@app.post("/ask")
async def ask(query: Query):
    prompt = f"به فارسی جواب بده: {query.question}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

# مسیر GET پیش‌فرض (اختیاری)
@app.get("/ping")
async def ping():
    return {"message": "سرور آماده است! برای دریافت جواب به /ask درخواست POST بدهید."}
