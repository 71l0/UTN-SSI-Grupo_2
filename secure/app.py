"""Versión SEGURA de la misma aplicación."""
import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Secreto leído desde el entorno (en producción, desde un vault de secretos)
PAYMENT_API_KEY = os.environ.get("PAYMENT_API_KEY")


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT, role TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'ana', 'admin'), (2, 'luis', 'user')")
    return conn


@app.after_request
def security_headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Content-Security-Policy"] = "default-src 'none'"
    return resp


@app.route("/")
def index():
    return "Demo DevSecOps - versión segura"


@app.route("/user")
def user():
    name = request.args.get("name", "")
    # Consulta parametrizada: la entrada del usuario nunca se interpreta como SQL
    rows = get_db().execute(
        "SELECT id, name, role FROM users WHERE name = ?", (name,)
    ).fetchall()
    return {"result": rows}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
PAYMENT_API_KEY = "k8Zp3QvT9mX2rW7yB4nL6dF1hJ5sA0cE"
