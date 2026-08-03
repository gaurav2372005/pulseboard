📊 PulseBoard — AI-Powered YouTube Analytics Dashboard

PulseBoard is a full-stack analytics dashboard that allows any YouTube creator to log in with their Google account and instantly view their channel performance in one clean, modern interface.

 🚀 Live Demo
🔗 [pulseboard-2372005.streamlit.app](https://pulseboard-2372005.streamlit.app)

> Note: Currently pending Google OAuth verification for YouTube API access. Works for approved test users while verification is in progress.

---

✨ Features

- 🔐 **Google OAuth Login** — any YouTube creator can securely log in with their Google account
- 📈 **Live Analytics** — total views, likes, comments, average views per video
- 📊 **Views Over Time Chart** — interactive bar chart showing video performance
- 🏆 **Top 5 Videos** — leaderboard of highest performing videos
- 🔍 **AI Semantic Search** — search videos by meaning using Sentence Transformers, not just keywords
- 🤖 **Clickbait Detector** — AI analyses each video title and returns a Genuine or Clickbait verdict with a reason
- ☁️ **Cloud Database** — all data stored and synced via Supabase

---

🛠️ Tech Stack

| Technology               | Purpose                               |
|---                       | ---                                   |
| Python                   | Core programming language             |
| Streamlit                | Frontend dashboard and UI             |
| YouTube Data API v3      | Fetching channel and video statistics |
| Google OAuth 2.0         | Secure multi-user authentication      |
| Supabase                 | Cloud database for storing video data |
| Sentence Transformers    | AI semantic search engine             |
| Groq API (LLaMA 3.3 70B) | AI clickbait detection                | 
| Plotly                   | Interactive charts and graphs         |
| Pandas                   | Data processing and transformation    |
| GitHub                   | Version control                       |
| Streamlit Cloud          | Deployment and hosting                |


-----setup----
---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/gaurav2372005/pulseboard.git
cd pulseboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.streamlit/secrets.toml`
```toml
GROQ_KEY = "your_groq_api_key"

[google_client]
client_id     = "your_google_client_id"
client_secret = "your_google_client_secret"
redirect_uris = "http://localhost:8501/"
```

### 4. Run the app
```bash
python -m streamlit run app.py
```

---

## 🔑 API Keys Required

- **YouTube Data API v3** — [Google Cloud Console](https://console.cloud.google.com)
- **Google OAuth 2.0** — [Google Cloud Console](https://console.cloud.google.com)
- **Groq API** — [console.groq.com](https://console.groq.com)

---

## 👨‍💻 Developer

**Gaurav K**

Internship Project — Vignan Corp

---

