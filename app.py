from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="datos_utpn"
)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        matricula = request.form["matricula"]
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        correo = request.form["correo"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        cursor = db.cursor()

        sql = """
        INSERT INTO datos_personales
        (matricula, nombre, apellidos, correo_personal, contrasena)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (matricula, nombre, apellidos, correo, hashed)

        cursor.execute(sql, values)
        db.commit()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        matricula = request.form["matricula"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM datos_personales WHERE matricula=%s", (matricula,))
        user = cursor.fetchone()

        if user and check_password_hash(user["contrasena"], password):
            session["usuario"] = user["matricula"]
            session["nombre"] = user["nombre"]
            return redirect("/dashboard")

        return "Credenciales incorrectas"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect("/login")
    return f"Bienvenido, {session['nombre']}"

if __name__ == "__main__":
    app.run(debug=True)