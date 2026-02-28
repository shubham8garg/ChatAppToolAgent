# 🚀 Quick Start Guide

## 30-Second Setup (Local)

### 1. Get Your API Key
- Go to https://console.groq.com
- Sign up for free
- Create an API key

### 2. Create `.streamlit/secrets.toml`
```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# Edit the file and paste your API key
```

### 3. Run It
```bash
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

Done! Open http://localhost:8501

---

## Deploy to Streamlit Cloud (5 Minutes)

1. Push your code to GitHub (repo must be public)
2. Go to https://share.streamlit.io
3. Click "New app" and select your repo
4. In Settings → Secrets, add your GROQ_API_KEY
5. Deploy!

Your URL will be: `https://yourname-yourrepo.streamlit.app`

---

## Test It

Try these questions:
- "What's the weather in Paris?"
- "What day is it today?"
- "Tell me about Einstein"
- "Calculate 2^10"

All tools should work now! ✅

---

## Need Help?

See [README.md](README.md) for detailed instructions.
