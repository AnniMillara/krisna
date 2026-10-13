from flask import redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario


@app.route("/comentarios/crear/<int:pelicula_id>", methods=["POST"])
def publicar_comentario(pelicula_id):
    if "id_usuario" not in session:
        flash("Inicia sesión para comentar.", "error")
        return redirect(url_for("portada"))
    pelicula = Pelicula.obtener_por_id(pelicula_id)
    if not pelicula:
        flash("La película no existe.", "error")
        return redirect(url_for("panel_peliculas"))
    if pelicula.usuario_id == session["id_usuario"]:
        flash("No puedes comentar tu propia película.", "error")
        return redirect(url_for("ver_pelicula", id=pelicula_id))
    contenido = request.form.get("contenido", "").strip()
    if len(contenido) < 1:
        flash("El comentario no puede estar vacío.", "error")
        return redirect(url_for("ver_pelicula", id=pelicula_id))
    Comentario.crear({
        "contenido": contenido,
        "pelicula_id": pelicula_id,
        "usuario_id": session["id_usuario"],
    })
    flash("Comentario publicado.", "success")
    return redirect(url_for("ver_pelicula", id=pelicula_id))


@app.route("/comentarios/eliminar/<int:id>", methods=["POST"])
def remover_comentario(id):
    if "id_usuario" not in session:
        flash("Inicia sesión.", "error")
        return redirect(url_for("portada"))
    comentario = Comentario.obtener_por_id(id)
    if not comentario:
        flash("El comentario no existe.", "error")
        return redirect(url_for("panel_peliculas"))
    if comentario.usuario_id != session["id_usuario"]:
        flash("No puedes borrar comentarios de otros.", "error")
        return redirect(url_for("ver_pelicula", id=comentario.pelicula_id))
    pelicula_id = comentario.pelicula_id
    Comentario.borrar(id)
    flash("Comentario eliminado.", "success")
    return redirect(url_for("ver_pelicula", id=pelicula_id))
