import { useState } from "react";

export default function Home() {
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  async function send() {
    if (!q.trim()) return;
    const userMsg = { role: "user", text: q };
    setMessages((m)=>[...m, userMsg]);
    setQ("");
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg.text })
      });
      const data = await res.json();
      if (data.error) {
        setMessages((m)=>[...m, { role: "bot", text: "خطا: " + data.error }]);
      } else {
        setMessages((m)=>[...m, { role: "bot", text: data.answer }]);
      }
    } catch (e) {
      setMessages((m)=>[...m, { role: "bot", text: "خطا در اتصال به سرور." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <header style={styles.header}>
          <h1 style={{margin:0}}>هوش فرار</h1>
          <p style={{margin: "6px 0 0 0", color: "#666"}}>چت فارسی — سریع و ساده</p>
        </header>

        <div style={styles.chat} id="chat">
          {messages.length === 0 && (
            <div style={{textAlign:"center", color:"#888", paddingTop:40}}>
              سلام! سوالت رو تایپ کن و روی ارسال بزن.
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} style={m.role === "user" ? styles.userMsg : styles.botMsg}>
              {m.text}
            </div>
          ))}
        </div>

        <div style={styles.inputRow}>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e)=> e.key === "Enter" && send()}
            placeholder="سوال خود را بنویس..."
            style={styles.input}
            disabled={loading}
          />
          <button onClick={send} style={styles.btn} disabled={loading}>
            {loading ? "در حال ارسال..." : "ارسال"}
          </button>
        </div>

        <footer style={styles.footer}>
          <small>ساخته شده برای «هوش فرار» — پاسخ‌ها به زبان فارسی تولید می‌شوند.</small>
        </footer>
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight:"100vh", display:"flex", alignItems:"center", justifyContent:"center", background: "linear-gradient(180deg,#eef2ff 0%, #ffffff 100%)", padding:20 },
  card: { width: "100%", maxWidth:800, background:"#fff", borderRadius:12, boxShadow:"0 8px 30px rgba(16,24,40,0.08)", overflow:"hidden" },
  header: { padding:20, borderBottom:"1px solid #f0f0f5" },
  chat: { minHeight: 360, maxHeight: 560, overflowY: "auto", padding: 20, display:"flex", flexDirection:"column", gap:10 },
  userMsg: { alignSelf:"flex-end", background:"#dbeafe", color:"#033", padding:"10px 14px", borderRadius:12, maxWidth:"85%" },
  botMsg: { alignSelf:"flex-start", background:"#ecfccb", color:"#063", padding:"10px 14px", borderRadius:12, maxWidth:"85%" },
  inputRow: { display:"flex", gap:10, padding:16, borderTop:"1px solid #f0f0f5" },
  input: { flex:1, padding:12, borderRadius:10, border:"1px solid #e6edf3", fontSize:16 },
  btn: { padding:"10px 18px", borderRadius:10, border:"none", background:"#4f46e5", color:"#fff", cursor:"pointer" },
  footer: { padding:12, textAlign:"center", color:"#8891a6" }
};