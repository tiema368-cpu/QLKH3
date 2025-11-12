from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os, json, uuid, functools

APP_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(APP_DIR, "data.json")
USERS_FILE = os.path.join(APP_DIR, "users.json")
SECRET_KEY_FILE = os.path.join(APP_DIR, ".secret_key")

def ensure_files():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    if not os.path.exists(USERS_FILE):
        # Default admin user: username=admin, password=ChangeMe123 (hashed)
        default = {{"username": "admin", "password": "scrypt:32768:8:1$gpzRrQsGfjqQNFmK$a46f69fa63b11854151280f96987904410cf39c1c34f149630f52e8fd30539017f014119b13b2873e036b8183ca6be958b08ddc75b4c2925466e421662cb5ab5"}}
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump([default], f, ensure_ascii=False, indent=2)
    if not os.path.exists(SECRET_KEY_FILE):
        import secrets
        with open(SECRET_KEY_FILE, "wb") as f:
            f.write(secrets.token_bytes(32))

ensure_files()

app = Flask(__name__)
# load secret key
with open(SECRET_KEY_FILE, "rb") as f:
    app.secret_key = f.read()

def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        users = load_users()
        for u in users:
            if u.get("username") == username and check_password_hash(u.get("password"), password):
                session["user"] = username
                flash("Đăng nhập thành công.", "success")
                nxt = request.args.get("next") or url_for("index")
                return redirect(nxt)
        flash("Tên đăng nhập hoặc mật khẩu không đúng.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Đã đăng xuất.", "info")
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    items = load_data()
    return render_template("index.html", items=items, user=session.get("user"))
@app.route("/add", methods=["POST"])
@login_required
def add():
    items = load_data()
    form = request.form
    new_item = {
        "id": str(uuid.uuid4()),
        "author": form.get("author","").strip(),
        "faculty": form.get("faculty","").strip(),
        "department": form.get("department","").strip(),
        "title": form.get("title","").strip(),
        "code": form.get("code","").strip(),
        "level": form.get("level","").strip(),
        "role": form.get("role","").strip(),
        "start_year": form.get("start_year","").strip(),
        "end_year": form.get("end_year","").strip(),
        "budget": form.get("budget","").strip(),
        "status": form.get("status","").strip()
    }
    items.append(new_item)
    save_data(items)
    flash("Đã thêm đề tài.", "success")
    return redirect(url_for("index"))


@app.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    items = load_data()
    item = next((i for i in items if i["id"] == id), None)
    if not item:
        flash("Không tìm thấy đề tài.", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        form = request.form
        item.update({
            "title": form.get("title","").strip(),
            "code": form.get("code","").strip(),
            "level": form.get("level","").strip(),
            "role": form.get("role","").strip(),
            "start_year": form.get("start_year","").strip(),
            "end_year": form.get("end_year","").strip(),
            "budget": form.get("budget","").strip(),
            "status": form.get("status","").strip()
        })
        save_data(items)
        flash("Đã cập nhật đề tài.", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", item=item)

@app.route("/delete/<id>", methods=["POST"])
@login_required
def delete(id):
    items = load_data()
    items = [i for i in items if i["id"] != id]
    save_data(items)
    flash("Đã xóa đề tài.", "info")
    return redirect(url_for("index"))

@app.route("/api/items")
@login_required
def api_items():
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)