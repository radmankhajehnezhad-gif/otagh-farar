# این فایل ZIP آماده برای Render است
# شامل:
# - app.py
# - index.html
# - requirements.txt
# - start.sh

# برای استفاده:
# 1. این کد را در محیط پایتون اجرا کن
# 2. فایل ZIP ساخته شده را آپلود روی Render کن

import zipfile
import os

# ایجاد پوشه موقت
os.makedirs('hooshfarar', exist_ok=True)

# ساخت app.py
with open('hooshfarar/app.py', 'w', encoding='utf-8') as f:
    f.write('''from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Query(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "هوش فرار آماده است. از مسیر /ask سوال بپرسید."}

@app.post("/ask")
async def ask(query: Query):
    prompt = f"به فارسی جواب بده: {query.question}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        print("OpenAI response:", response)
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
''')

# ساخت index.html
with open('hooshfarar/index.html', 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<title>هوش فرار - چت فارسی</title>
<style>
body { font-family: Tahoma, sans-serif; direction: rtl; padding: 20px; background: #f5f5f5; }
#chat { max-width: 600px; margin: auto; }
.message { padding: 10px; margin: 5px 0; border-radius: 5px; }
.user { background: #d1e7dd; text-align: right; }
.bot { background: #f8d7da; text-align: left; }
input[type="text"] { width: 80%; padding: 10px; }
button { padding: 10px; }
</style>
</head>
<body>
<h2>هوش فرار - چت فارسی</h2>
<div id="chat"></div>
<input type="text" id="question" placeholder="سوال خود را بنویسید...">
<button onclick="sendQuestion()">ارسال</button>
<script>
async function sendQuestion() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();
    if (!question) return;
    const chatDiv = document.getElementById('chat');
    const userMsg = document.createElement('div');
    userMsg.className = 'message user';
    userMsg.innerText = question;
    chatDiv.appendChild(userMsg);
    questionInput.value = '';
    chatDiv.scrollTop = chatDiv.scrollHeight;
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        const data = await response.json();
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';
        if(data.answer){
            botMsg.innerText = data.answer;
        } else if(data.error){
            botMsg.innerText = "خطا: " + data.error;
        } else {
            botMsg.innerText = "پاسخی دریافت نشد.";
        }
        chatDiv.appendChild(botMsg);
        chatDiv.scrollTop = chatDiv.scrollHeight;
    } catch (err) {
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';
        botMsg.innerText = "خطا در اتصال به سرور.";
        chatDiv.appendChild(botMsg);
    }
}
</script>
</body>
</html>
''')

# ساخت requirements.txt
with open('hooshfarar/requirements.txt', 'w', encoding='utf-8') as f:
    f.write('''fastapi
uvicorn
openai
pydantic
''')

# ساخت start.sh
with open('hooshfarar/start.sh', 'w', encoding='utf-8') as f:
    f.write('''#!/bin/bash
uvicorn app:app --host 0.0.0.0 --port $PORT
''')

# ساخت فایل ZIP
zipf = zipfile.ZipFile('hooshfarar.zip','w', zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk('hooshfarar'):
    for file in files:
        zipf.write(os.path.join(root, file), arcname=os.path.join(os.path.relpath(root,'hooshfarar'),file))
zipf.close()

print("فایل ZIP آماده شد: hooshfarar.zip")