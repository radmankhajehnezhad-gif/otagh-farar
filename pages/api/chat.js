import OpenAI from "openai";
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const { question } = req.body || {};
  if (!question) return res.status(400).json({ error: "سوال ارسال نشده" });

  try {
    const systemPrompt = "تو یک دستیار ایرانی هستی. همیشه به فارسی و مختصر جواب بده. سوال کاربر را تکرار نکن.";
    const resp = await client.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: question }
      ],
      max_tokens: 400,
      temperature: 0.6
    });
    const answer = resp.choices?.[0]?.message?.content ?? "پاسخی دریافت نشد.";
    res.status(200).json({ answer });
  } catch (err) {
    res.status(500).json({ error: "خطا در اتصال به سرویس: " + err.message });
  }
}