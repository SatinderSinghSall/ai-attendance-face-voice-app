# 🤖 AI Attendance System – Main Application

# Intelligent AI Attendance - Face & Voice

### Face Recognition & Voice Biometrics for Smart Attendance

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Supabase](https://img.shields.io/badge/Database-Supabase-green)
![Machine Learning](https://img.shields.io/badge/AI-Face%20%2B%20Voice-purple)

---

# 📌 Overview

The **AI Attendance Application** is a biometric attendance platform that uses **face recognition and voice biometrics** to automatically mark classroom attendance.

The application is built using **Streamlit for the UI**, and integrates **machine learning pipelines** for identity verification.

---

# 🎯 Key Features

### 👨‍🏫 Teacher Features

- Create subjects or courses
- Generate QR code for enrollment
- Start face attendance
- Start voice attendance
- View attendance records
- Manage student enrollment

### 👨‍🎓 Student Features

- Join subjects via QR code
- Upload face profile
- Enroll voice profile
- Mark attendance using biometrics

---

# 🧠 AI Pipelines

The system uses two biometric pipelines.

---

## 📸 Face Recognition

Pipeline steps:

```
Camera Image
     │
     ▼
Face Detection (dlib)
     │
     ▼
Face Embedding Generation
     │
     ▼
Embedding Similarity Comparison
     │
     ▼
Student Identification
     │
     ▼
Attendance Logged
```

---

## 🎙️ Voice Recognition

Pipeline steps:

```
Audio Recording
     │
     ▼
Audio Feature Extraction (Librosa)
     │
     ▼
Speaker Embedding (Resemblyzer)
     │
     ▼
Embedding Comparison
     │
     ▼
Identity Verification
     │
     ▼
Attendance Logged
```

---

# 🏗️ Project Structure

```
ai-attendance-project-app-main
│
├── src
│   ├── components
│   │   ├── dialog_*.py
│   │   ├── header.py
│   │   └── footer.py
│   │
│   ├── database
│   │   ├── config.py
│   │   └── db.py
│   │
│   ├── pipelines
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   │
│   ├── screens
│   │   ├── home_screen.py
│   │   ├── teacher_screen.py
│   │   └── student_screen.py
│   │
│   └── ui
│       └── base_layout.py
│
├── app.py
└── requirements.txt
```

---

# 🖥️ Technology Stack

| Category          | Technology         |
| ----------------- | ------------------ |
| UI                | Streamlit          |
| Machine Learning  | dlib, scikit-learn |
| Voice Recognition | Resemblyzer        |
| Audio Processing  | Librosa            |
| Data Processing   | NumPy, Pandas      |
| Image Processing  | Pillow             |
| Database          | Supabase           |
| Security          | bcrypt             |

---

# ⚙️ Installation

Navigate to the application folder:

```bash
cd ai-attendance-project-app-main
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

# 🗄️ Database

The application uses **Supabase** for cloud database management.

Stored data includes:

- Students
- Subjects
- Enrollment records
- Face embeddings
- Voice embeddings
- Attendance logs

---

# 🔬 Methodology

Identity verification is performed using **embedding similarity comparison**.

Steps:

1. Extract biometric embedding
2. Compute similarity with stored embeddings
3. Apply similarity threshold
4. Identify user
5. Record attendance

---

# 🚀 Future Improvements

- Face liveness detection
- Anti-spoofing mechanisms
- Mobile device support
- Attendance analytics dashboard
- Real-time attendance monitoring

---

# 👨‍💻 Author

Satinder Singh Sall
AI / ML
Full-Stack Web & Mobile Engineer

Developed as part of the **AI Projects Module**

---

# 📜 License

This project is licensed under the **MIT License**.
