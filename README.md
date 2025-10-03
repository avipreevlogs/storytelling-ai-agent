# Storytelling Agent

यह प्रोजेक्ट आपके लिए एक **AI आधारित Hindi Storytelling Agent** है जो:
- कहानी generate करता है (OpenAI से)
- Voiceover और background music जोड़ता है
- वीडियो बनाता है
- और उसे YouTube पर upload करता है 🚀

## कैसे उपयोग करें (GitHub Actions के साथ)

1. Repo को GitHub पर upload करें।
2. GitHub → Settings → Secrets and variables → Actions में ये secrets add करें:
   - `OPENAI_API_KEY` = आपकी OpenAI API key
   - `CLIENT_SECRET_JSON` = आपके YouTube OAuth client_secret.json का पूरा JSON
3. Actions → Run workflow पर जाएँ और workflow run करें।
4. Build पूरा होने पर आपको artifact मिलेगा जिसमें `.exe` file होगी।

## Local build (optional)
```bash
pip install -r requirements.txt
pyinstaller --onefile storyteller_youtube_agent.py
```

⚠️ ध्यान रखें: API keys या JSON को कभी public repo में commit मत करें।
