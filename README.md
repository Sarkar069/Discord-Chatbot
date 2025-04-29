# Discord Chatbot 🤖

A powerful chatbot for Discord servers built with **[Disnake.py](https://docs.disnake.dev/)** and integrated with **GROQ API** for intelligent AI responses.

---

## 📚 About

This bot can chat intelligently in selected channels, maintain conversation history, and includes useful slash commands to manage its behavior.  
Ideal for Discord servers that want an AI assistant or chat companion!

---

## ✨ Features

- **GROQ API Integration**: Smart, context-aware conversation generation.
- **Channel Restriction**: Only responds in approved channels.
- **History Management**: Deletes previous conversations when needed.
- **Simple and Clean Code**: Easy to understand and expand.

---

## 🛠 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Sarkar069/Discord-Chatbot.git
cd Discord-Chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> ⚡ Make sure you have Python 3.8 or above.

### 3. Setup your `.env` file

Create a `.env` file in the root directory:


### 4. Run the bot

```bash
python3 main.py
```

---

## 📂 Project Structure

```
├── cogs/
│   └── groq.py            # Slash commands for channel toggle and history clear 
├── botlog.py                  # Logging setup
├── main.py                    # Main bot file
├── requirements.txt           # Dependencies
├── .env                       # Environment variables (not committed)
└── README.md                  # Project info
```

---

## 🧹 Slash Commands

| Command            | Description                                           |
| ------------------ | ----------------------------------------------------- |
| `/toggle_channel`  | Sets the channel where the bot will respond.           |
| `/clear_history`   | Clears the stored conversation history for the session.|
| `/switch model `   | model a different model to chat with.                  |
---

## 📋 Requirements

- [Python 3.8+](https://www.python.org/)
- [Disnake.py](https://pypi.org/project/disnake/)
- Access to [GROQ API](https://groq.com/)

---


## 📢 Notes

- Slash commands may take a few minutes to register globally after the bot starts, that's why we are using DEV_GUILD_ID
- Ensure you invite the bot with the correct permissions:  
  - `applications.commands`
  - `bot` permissions to read/send messages.
- Make sure you have Message Content Intent enabled on [DISCORD DEV PORTAL](https://discord.com/developers/docs/intro)

---

# Happy chatting! 🎉
