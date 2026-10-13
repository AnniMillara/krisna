from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario


def requiere_sesion():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "error")
        return False
    return True


@app.route("/peliculas")
def panel_peliculas():
    if not requiere_sesion():
        return redirect(url_for("portada"))
    peliculas = Pelicula.listar_todas()
    return render_template("peliculas_lista.html", peliculas=peliculas)


@app.route("/peliculas/nueva")
def formulario_nueva():
    if not requiere_sesion():
        return redirect(url_for("portada"))
    return render_template("pelicula_form.html", pelicula=None, modo="crear")


@app.route("/peliculas/crear", methods=["POST"])
def registrar_pelicula():
    if not requiere_sesion():
        return redirect(url_for("portada"))
    datos = {
        "titulo": request.form.get("titulo", "").strip(),
        "director": request.form.get("director", "").strip(),
        "fecha_estreno": request.form.get("fecha_estreno", "").strip(),
        "sinopsis": request.form.get("sinopsis", "").strip(),
        "usuario_id": session["id_usuario"],
    }
    if not Pelicula.validar_datos(datos):
        return render_template("pelicula_form.html", pelicula=datos, modo="crear")
    Pelicula.crear(datos)
    flash("Película registrada correctamente.", "success")
    return redirect(url_for("panel_peliculas"))


@app.route("/peliculas/detalle/<int:id>")
def ver_pelicula(id):
    if not requiere_sesion():
        return redirect(url_for("portada"))
    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula:
        flash("Película no encontrada.", "error")
        return redirect(url_for("panel_peliculas"))
    comentarios = Comentario.listar_por_pelicula(id)
    return render_template("pelicula_detalle.html", pelicula=pelicula, comentarios=comentarios)


@app.route("/peliculas/editar/<int:id>")
def formulario_editar(id):
    if not requiere_sesion():
        return redirect(url_for("portada"))
    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula:
        flash("Película no encontrada.", "error")
        return redirect(url_for("panel_peliculas"))
    if pelicula.usuario_id != session["id_usuario"]:
        flash("No puedes editar una película que no es tuya.", "error")
        return redirect(url_for("panel_peliculas"))
    return render_template("pelicula_form.html", pelicula=pelicula, modo="editar")


@app.route("/peliculas/modificar/<int:id>", methods=["POST"])
def guardar_cambios(id):
    if not requiere_sesion():
        return redirect(url_for("portada"))
    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula or pelicula.usuario_id != session["id_usuario"]:
        flash("No puedes editar una película que no es tuya.", "error")
        return redirect(url_for("panel_peliculas"))
    datos = {
        "id_pelicula": id,
        "titulo": request.form.get("titulo", "").strip(),
        "director": request.form.get("director", "").strip(),
        "fecha_estreno": request.form.get("fecha_estreno", "").strip(),
        "sinopsis": request.form.get("sinopsis", "").strip(),
    }
    if not Pelicula.validar_datos(datos):
        return render_template("pelicula_form.html", pelicula=datos, modo="editar")
    Pelicula.actualizar(datos)
    flash("Película actualizada correctamente.", "success")
    return redirect(url_for("panel_peliculas"))


@app.route("/peliculas/eliminar/<int:id>", methods=["POST"])
def remover_pelicula(id):
    if not requiere_sesion():
        return redirect(url_for("portada"))
    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula or pelicula.usuario_id != session["id_usuario"]:
        flash("No puedes borrar una película que no es tuya.", "error")
        return redirect(url_for("panel_peliculas"))
    Pelicula.borrar(id)
    flash("Película eliminada.", "success")
    return redirect(url_for("panel_peliculas"))
