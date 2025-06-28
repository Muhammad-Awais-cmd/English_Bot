# Englishh_Assisting_Bot 🤖📘

A free, fast, and professional English learning Telegram bot that helps users:

- ✅ Define English words (general, scientific, borrowed terms, etc.)
- ✅ Get accurate synonyms
  
---

## 🔍 Features

- **/start** – Introduction and usage help  
- **/help** – All available commands  
- **/define `<word>`** – Provides detailed definitions  
- **/synonym `<word>`** – Lists synonyms
- 📑 Supports multi-user usage with command tracking
- ⚡ Fast response time (~5 seconds)

---

## ⚙️ How I Built It

- **Language**: Python 3.12  
- **Frameworks**: `python-telegram-bot`, `httpx`, `asyncio`  
- **Project Structure**: Modularized with `utils/`, `session_manager.py`, and command handlers
- **Hosting**: Deployed on [Railway](https://railway.app) for 24/7 uptime

---

## 🧠 Design Philosophy

This bot is designed with these goals in mind:
- Clear and professional responses
- No downtime
- Lightweight and easy to extend
- Anonymous, low-maintenance interface

---

## 🧪 If You're Forking or Copying This

Keep these things in mind:
- **Do not run this bot locally** unless you're okay with it shutting down when you close your PC.
- The bot uses **long polling**, which needs continuous execution.
- You **must deploy it to a cloud host** to stay live 24/7 (see deployment section below).
- The bot requires a valid **Telegram Bot Token**.

---

## 🚀 Deployment on Railway (Free for Trial Use)

You can easily deploy this bot using [Railway](https://railway.app):

1. **Create a Railway account**
2. Link your GitHub repo
3. Add an environment variable:
   - `BOT_TOKEN=your-telegram-bot-token`
4. Deploy and let it run continuously

> 🔥 Note: Railway offers free credits when you first sign up. Once they expire, your bot will stop unless you upgrade to a paid plan. Consider switching to Replit + UptimeRobot or Render for free hosting alternatives.

---

## 📄 License

MIT License.  
Use freely, contribute responsibly.

---

## 🤖 Made by Muhammad Awais  
GitHub: [Muhammad-Awais-cmd](https://github.com/Muhammad-Awais-cmd)
