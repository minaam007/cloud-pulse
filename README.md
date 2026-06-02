# ☁️ CloudPulse — Scalable Web App Deployment on Cloud

> **Cloud Computing Capstone Project** | Python Flask + MongoDB Atlas + Render

A production-style cloud-hosted web application with real-time monitoring, user authentication, and a live analytics dashboard — built to satisfy all 5 modules of the capstone project.

---

## 🚀 Live Demo

https://cloud-pulse-l4lr.onrender.com/login

---

## 🏗️ Architecture

```
User Browser
     │
     ▼
[ Render Cloud (Web Service) ]
     │
     ├── Flask App (Gunicorn, 2 workers)
     │       ├── Auth routes (/login, /register, /logout)
     │       ├── Dashboard (/dashboard)
     │       └── API (/api/metrics, /api/health)
     │
     └── MongoDB Atlas (Cloud Database)
             ├── users        → hashed passwords, registration data
             ├── request_logs → every HTTP request logged automatically
             └── metrics      → uptime + analytics data
```

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JS (no framework needed) |
| Backend | Python 3.11, Flask 3.0 |
| Database | MongoDB Atlas (free tier) |
| Cloud Platform | Render (free tier) |
| Containerization | Docker |
| CI/CD | GitHub → Render auto-deploy |

---

## 📁 Project Structure

```
cloudpulse/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container config
├── render.yaml            # Render deployment config
├── .gitignore
├── README.md
└── templates/
    ├── login.html         # Login page
    ├── register.html      # Registration page
    └── dashboard.html     # Live monitoring dashboard
```

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/cloudpulse.git
cd cloudpulse
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file:
```
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/cloudpulse
SECRET_KEY=your-secret-key-here
```

### 4. Run locally
```bash
python app.py
```
Open `http://localhost:5000`

---

## ☁️ Deploy to Render (Free)

### Step 1 — MongoDB Atlas
1. Go to [mongodb.com/atlas](https://www.mongodb.com/atlas) → Create free cluster
2. Create a database user (username + password)
3. Whitelist IP: `0.0.0.0/0` (allow all)
4. Copy your **connection string**: `mongodb+srv://user:pass@cluster.../cloudpulse`

### Step 2 — GitHub
```bash
git init
git add .
git commit -m "Initial commit: CloudPulse"
git remote add origin https://github.com/YOUR_USERNAME/cloudpulse.git
git push -u origin main
```

### Step 3 — Render
1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repo
3. Render auto-detects `render.yaml`
4. Add environment variable: `MONGO_URI` → paste your Atlas connection string
5. Click **Deploy** → done in ~2 minutes ✅

---

## 📊 Features (Capstone Modules Covered)

| Module | Feature | Status |
|--------|---------|--------|
| Module 1 | Web App: Login, Register, Dashboard | ✅ |
| Module 2 | Cloud Deployment on Render | ✅ |
| Module 3 | MongoDB Atlas Integration | ✅ |
| Module 4 | Docker + GitHub CI/CD auto-deploy | ✅ |
| Module 5 | Live Monitoring Dashboard | ✅ |

### Dashboard Metrics (Live, auto-refresh every 10s)
- ✅ Server status (ONLINE/OFFLINE)
- ✅ Application uptime
- ✅ Total & active users (last 1 hour)
- ✅ Total requests & requests today
- ✅ Requests per hour chart (last 12 hours)
- ✅ Recent request logs (path, method, user, timestamp)
- ✅ Top 5 most visited routes

---

## 👩‍💻 Author

