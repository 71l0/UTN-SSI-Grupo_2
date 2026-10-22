"""Versión VULNERABLE (solo para la demostración). No usar en producción."""
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# [Falla 1] Secreto escrito directamente en el código
PAYMENT_API_KEY = "k8Zp3QvT9mX2rW7yB4nL6dF1hJ5sA0cE"


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT, role TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'ana', 'admin'), (2, 'luis', 'user')")
    return conn


@app.route("/")
def index():
    return "Demo DevSecOps - versión vulnerable"


@app.route("/user")
def user():
    name = request.args.get("name", "")
    # [Falla 2] Inyección SQL: la consulta se arma concatenando entrada del usuario
    query = f"SELECT id, name, role FROM users WHERE name = '{name}'"
    rows = get_db().execute(query).fetchall()
    return {"result": rows}


if __name__ == "__main__":
    # [Falla 3] debug activo y escucha en todas las interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
