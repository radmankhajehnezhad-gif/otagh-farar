from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# خواندن API Key از متغیر محیطی
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

# فعال کردن CORS برای همه دامنه‌ها
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# صفحه HTML اصلی
@app.get("/", response_class=HTMLResponse)
async def get_index():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>هوش فرار</title>
    </head>
    <body>
        <h2>سوال خود را بپرس:</h2>
        <input type="text" id="question" placeholder="سوال خود را بنویس">
        <button onclick="sendQuestion()">ارسال</button>
        <p id="answer"></p>
        <script>
            async function sendQuestion() {
                const q = document.getElementById("question").value;
                const res = await fetch("/ask", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({question: q})
                });
                const data = await res.json();
                document.getElementById("answer").innerText = data.answer;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# مسیر /ask برای دریافت سوال و ارسال به OpenAI
@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # می‌توانی gpt-4 هم بزنی اگر دسترسی داری
            messages=[{"role": "user", "content": question}],
            max_tokens=200
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"خطا در دریافت پاسخ: {e}"

    return JSONResponse(content={"answer": answer})
