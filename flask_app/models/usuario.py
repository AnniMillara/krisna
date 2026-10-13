import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

PATRON_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
BASE = "esquema_peliculas"


class Usuario:
    def __init__(self, datos):
        self.id_usuario = datos["id_usuario"]
        self.nombre = datos["nombre"]
        self.apellido = datos["apellido"]
        self.email = datos["email"]
        self.contrasena = datos["contrasena"]
        self.created_at = datos["created_at"]
        self.updated_at = datos["updated_at"]

    @classmethod
    def crear(cls, datos):
        consulta = """
            INSERT INTO usuarios (nombre, apellido, email, contrasena, created_at, updated_at)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(contrasena)s, NOW(), NOW());
        """
        return connectToMySQL(BASE).query_db(consulta, datos)

    @classmethod
    def obtener_por_id(cls, id_usuario):
        consulta = """
            SELECT id_usuario, nombre, apellido, email, contrasena, created_at, updated_at
            FROM usuarios WHERE id_usuario = %(id_usuario)s;
        """
        resultado = connectToMySQL(BASE).query_db(consulta, {"id_usuario": id_usuario})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def obtener_por_email(cls, email):
        consulta = """
            SELECT id_usuario, nombre, apellido, email, contrasena, created_at, updated_at
            FROM usuarios WHERE email = %(email)s;
        """
        resultado = connectToMySQL(BASE).query_db(consulta, {"email": email})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def borrar(cls, id_usuario):
        consulta = "DELETE FROM usuarios WHERE id_usuario = %(id_usuario)s;"
        return connectToMySQL(BASE).query_db(consulta, {"id_usuario": id_usuario})

    @staticmethod
    def validar_datos(datos):
        valido = True
        nombre = datos.get("nombre", "").strip()
        apellido = datos.get("apellido", "").strip()
        email = datos.get("email", "").strip()
        contrasena = datos.get("contrasena", "")

        if len(nombre) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "error")
            valido = False
        if len(apellido) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "error")
            valido = False
        if not email:
            flash("El email es obligatorio.", "error")
            valido = False
        elif not PATRON_EMAIL.match(email):
            flash("El email no tiene un formato válido.", "error")
            valido = False
        elif Usuario.obtener_por_email(email):
            flash("Ese email ya está registrado.", "error")
            valido = False
        if len(contrasena) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            valido = False
        if datos.get("confirmar_contrasena") is not None and contrasena != datos.get("confirmar_contrasena"):
            flash("Las contraseñas no coinciden.", "error")
            valido = False
        return valido
