from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario


@app.route("/")
def portada():
    if "id_usuario" in session:
        return redirect(url_for("panel_peliculas"))
    return render_template("login.html")


@app.route("/registro", methods=["POST"])
def registrar():
    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "apellido": request.form.get("apellido", "").strip(),
        "email": request.form.get("email", "").strip(),
        "contrasena": request.form.get("contrasena", ""),
        "confirmar_contrasena": request.form.get("confirmar_contrasena", ""),
    }
    if not Usuario.validar_datos(datos):
        return redirect(url_for("portada"))

    hash_pw = bcrypt.generate_password_hash(datos["contrasena"]).decode("utf-8")
    nuevo_id = Usuario.crear({
        "nombre": datos["nombre"],
        "apellido": datos["apellido"],
        "email": datos["email"],
        "contrasena": hash_pw,
    })
    if not nuevo_id:
        flash("No fue posible crear el usuario.", "error")
        return redirect(url_for("portada"))

    session.clear()
    session["id_usuario"] = nuevo_id
    session["nombre"] = datos["nombre"]
    flash("Usuario registrado correctamente.", "success")
    return redirect(url_for("panel_peliculas"))


@app.route("/login", methods=["POST"])
def autenticar():
    email = request.form.get("email", "").strip()
    contrasena = request.form.get("contrasena", "")
    if not email or not contrasena:
        flash("Debes indicar email y contraseña.", "error")
        return redirect(url_for("portada"))

    usuario = Usuario.obtener_por_email(email)
    if not usuario or not bcrypt.check_password_hash(usuario.contrasena, contrasena):
        flash("Email o contraseña incorrectos.", "error")
        return redirect(url_for("portada"))

    session.clear()
    session["id_usuario"] = usuario.id_usuario
    session["nombre"] = usuario.nombre
    flash("Bienvenido de vuelta.", "success")
    return redirect(url_for("panel_peliculas"))


@app.route("/logout", methods=["GET", "POST"])
def salir():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("portada"))
