# 🧠 TinyLabs.ai — AI-Powered Children's Story Generator

A fun and educational web application that lets children and parents generate imaginative stories using artificial intelligence. Built with Django, Django REST Framework, and Hugging Face models.

---

## 🚀 Features

- ✨ Generate short children's stories based on a **theme, characters, and moral**
- 🔁 Revise generated stories using **instructional feedback**
- 💡 AI rewrites the story — e.g., "Make it shorter" or "Add a parrot"
- 🔄 **Fallback AI model support** in case primary model fails
- 📜 Stories are saved in a database for reference or editing
- User Login and 📜 Stories ownership

---

## 🛠️ Tech Stack

- **Backend**: Django + Django REST Framework
- **AI Models**: Hugging Face Inference API
  - Primary: `moonshotai/Kimi-K2-Instruct:novita`
  - Fallback: `google/flan-t5-large`
- **Data Storage**: SQLite (default for development)

