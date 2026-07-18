<div align="center">
  <h1>🌟 REFLECT 🌟</h1>
  <p><strong>An AI-powered emotion-aware journaling application that helps you understand your feelings.</strong></p>

  <p>
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" />
    <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  </p>
</div>

<br />

## 📖 About The Project

**REFLECT** is an intelligent AI-powered journaling platform designed to promote mindfulness and emotional awareness. Using Natural Language Processing (NLP), it analyzes the emotions expressed in your journal entries and provides meaningful insights into your emotional well-being over time.

### ✨ Key Features

- 📝 **Smart Journaling** – Write, edit, and securely store your daily journal entries.
- 🤖 **AI Emotion Detection** – Uses a Hugging Face Transformer model (`DistilRoBERTa`) to automatically identify the primary emotion in each journal entry.
- 📊 **Analytics Dashboard** – Track mood trends and emotional patterns through interactive charts and visualizations.
- 🔐 **Secure Authentication** – JWT-based authentication ensures your personal journal entries remain private.
- 📄 **Export Support** – Export journal entries as PDF *(planned feature)*.

---

## 🛠 Tech Stack

### Frontend

- React.js (Vite)
- Tailwind CSS
- Framer Motion
- Recharts
- React Hook Form

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- Hugging Face Transformers
- PyTorch
- Passlib
- Python-JOSE (JWT Authentication)

---

## 🚀 Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

Make sure the following are installed:

- Node.js (v18 or higher)
- Python (v3.10 or higher)
- Git

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/sanya-anand/reflect.git
cd reflect
```

---

## 2️⃣ Backend Setup

Navigate to the backend folder.

```bash
cd backend
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Copy the sample environment file.

```bash
cp .env.example .env
```

Update the `.env` file with your own values such as:

- SECRET_KEY
- JWT settings
- Allowed Origins

### Start the Backend

```bash
uvicorn main:app --reload
```

The backend will run at

```
http://127.0.0.1:8000
```

---

## 3️⃣ Frontend Setup

Open a new terminal.

Navigate to the frontend folder.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Start the development server.

```bash
npm run dev
```

The frontend will be available at

```
http://localhost:5173
```

---

## 🔌 API Documentation

FastAPI automatically generates interactive API documentation.

Once the backend is running, visit:

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 📂 Project Structure

```text
REFLECT/
│
├── backend/
│   ├── auth/                  # Authentication logic
│   ├── models/                # SQLAlchemy models
│   ├── routes/                # API endpoints
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic & NLP
│   ├── utils/                 # Helper functions
│   ├── main.py                # FastAPI entry point
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
└── README.md
```
