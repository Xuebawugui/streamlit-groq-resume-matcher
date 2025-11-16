# AI Resume Matcher (Groq Ultra Fast)

Built for Japan IT job hunting | Llama3-70B | High free quota | Streamlit single-page app

## Features
- Upload a PDF resume and parse text automatically
- Paste a Japanese company JD and get instant AI analysis
- Output 0–100 match score, strengths/weaknesses, Japanese suggestions, custom interview questions (JSON)
- Multilingual UI (English/中文/日本語) and selectable output language (Japanese/English)

## Tech Stack
- Python 3.11+
- Streamlit (Web UI)
- Groq API (Llama3-70B / Mixtral)
- pdfplumber (PDF parsing)
- python-dotenv (.env loading)

## Project Structure
```
.
├─ app.py               # Main app entry (Streamlit single page)
├─ requirements.txt     # Dependencies
├─ .env.example         # Environment variables sample (copy to .env)
├─ .gitignore           # Ignore .env and Secrets
└─ 项目说明.txt          # Project description (Chinese)
```

## Environment Variables & Secrets
- Copy `.env.example` to `.env` and set your Groq key:
```
GROQ_API_KEY=YOUR_GROQ_API_KEY
```
- Or set Streamlit Cloud Secrets:
```
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
- Read order: `st.secrets["GROQ_API_KEY"]` first, fallback to `os.getenv("GROQ_API_KEY")` (`c:\Users\wugui1314\Desktop\Myitems\202511moth\9\app.py:100-103`)
- `.env` loading: `load_dotenv()` 

## Local Setup (optional)
- Install dependencies:
```
pip install -r requirements.txt
```
- Run:
```
streamlit run app.py
```
- Visit: `http://localhost:8501`

## Deploy (Streamlit Cloud)
1. Push this repo to GitHub
2. Go to https://share.streamlit.io and create a new app from your repo
3. Add `GROQ_API_KEY` in Settings → Secrets
4. Deploy and share the URL

## Usage
- Choose model and languages in the sidebar (UI language vs output language)
- Paste JD, upload a PDF resume, click Analyze
- If strict JSON is returned, it renders structured JSON; otherwise shows the raw output for inspection (`c:\Users\wugui1314\Desktop\Myitems\202511moth\9\app.py:136-144`)

## Internationalization
- UI languages: English / 中文 / 日本語 
- Output language: 日本語 / English (controls model response)

## Security
- Do not commit real keys to GitHub; `.gitignore` ignores `.env` and `.streamlit/secrets.toml`
- Do not hardcode keys in code; use Secrets or environment variables only

## License
- Personal and learning use preferred; check dependencies and Groq policy for commercial use
