from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import os
import time

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cloudpulse-dev-secret-key")

START_TIME = time.time()

MONGO_URI = os.environ.get("MONGO_URL") or os.environ.get("MONGO_URI", "mongodb://localhost:27017/cloudpulse")

_client = None

def get_col(name):
    global _client
    if _client is None:
        _client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )
    return _client["cloudpulse"][name]

@app.before_request
def log_request():
    if not request.path.startswith("/static"):
        try:
            get_col("request_logs").insert_one({
                "path": request.path,
                "method": request.method,
                "ip": request.remote_addr,
                "user": session.get("username", "anonymous"),
                "timestamp": datetime.utcnow()
            })
        except Exception as e:
            print("MongoDB Error:", e)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        users = get_col("users")
        if not username or not email or not password:
            error = "All fields are required."
        elif users.find_one({"username": username}):
            error = "Username already taken."
        elif users.find_one({"email": email}):
            error = "Email already registered."
        else:
            users.insert_one({
                "username": username,
                "email": email,
                "password": generate_password_hash(password),
                "created_at": datetime.utcnow(),
                "role": "user"
            })
            session["username"] = username
            return redirect(url_for("dashboard"))
    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_col("users").find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        error = "Invalid credentials."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session["username"])

@app.route("/api/metrics")
@login_required
def api_metrics():
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    one_day_ago = now - timedelta(days=1)
    logs = get_col("request_logs")
    users = get_col("users")
    uptime_seconds = int(time.time() - START_TIME)
    hours, rem = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"
    total_users = users.count_documents({})
    active_users = logs.distinct("user", {"timestamp": {"$gte": one_hour_ago}, "user": {"$ne": "anonymous"}})
    total_requests = logs.count_documents({})
    requests_today = logs.count_documents({"timestamp": {"$gte": one_day_ago}})
    recent_logs = list(logs.find({}, {"_id": 0, "path": 1, "method": 1, "user": 1, "ip": 1, "timestamp": 1}).sort("timestamp", -1).limit(10))
    for log in recent_logs:
        log["timestamp"] = log["timestamp"].strftime("%H:%M:%S")
    hourly = []
    for i in range(11, -1, -1):
        start = now - timedelta(hours=i+1)
        end = now - timedelta(hours=i)
        count = logs.count_documents({"timestamp": {"$gte": start, "$lt": end}})
        hourly.append({"hour": start.strftime("%H:00"), "count": count})
    pipeline = [{"$group": {"_id": "$path", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": 5}]
    top_routes = [{"path": r["_id"], "count": r["count"]} for r in logs.aggregate(pipeline)]
    return jsonify({"uptime": uptime_str, "total_users": total_users, "active_users": len(active_users), "total_requests": total_requests, "requests_today": requests_today, "recent_logs": recent_logs, "hourly_chart": hourly, "top_routes": top_routes, "server_status": "ONLINE"})

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
