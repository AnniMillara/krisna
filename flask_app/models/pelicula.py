from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

BASE = "esquema_peliculas"


class Pelicula:
    def __init__(self, datos):
        self.id_pelicula = datos["id_pelicula"]
        self.titulo = datos["titulo"]
        self.director = datos["director"]
        self.fecha_estreno = datos["fecha_estreno"]
        self.sinopsis = datos["sinopsis"]
        self.usuario_id = datos["usuario_id"]
        self.created_at = datos["created_at"]
        self.updated_at = datos["updated_at"]
        self.autor_nombre = datos.get("autor_nombre")
        self.autor_apellido = datos.get("autor_apellido")

    @classmethod
    def crear(cls, datos):
        consulta = """
            INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, usuario_id, created_at, updated_at)
            VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s, NOW(), NOW());
        """
        return connectToMySQL(BASE).query_db(consulta, datos)

    @classmethod
    def listar_todas(cls):
        consulta = """
            SELECT p.id_pelicula, p.titulo, p.director, p.fecha_estreno, p.sinopsis,
                   p.usuario_id, p.created_at, p.updated_at,
                   u.nombre AS autor_nombre, u.apellido AS autor_apellido
            FROM peliculas p
            JOIN usuarios u ON p.usuario_id = u.id_usuario
            ORDER BY p.id_pelicula;
        """
        resultados = connectToMySQL(BASE).query_db(consulta)
        return [cls(fila) for fila in resultados]

    @classmethod
    def obtener_por_id(cls, id_pelicula):
        consulta = """
            SELECT p.id_pelicula, p.titulo, p.director, p.fecha_estreno, p.sinopsis,
                   p.usuario_id, p.created_at, p.updated_at,
                   u.nombre AS autor_nombre, u.apellido AS autor_apellido
            FROM peliculas p
            JOIN usuarios u ON p.usuario_id = u.id_usuario
            WHERE p.id_pelicula = %(id_pelicula)s;
        """
        resultado = connectToMySQL(BASE).query_db(consulta, {"id_pelicula": id_pelicula})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def obtener_por_titulo(cls, titulo):
        consulta = """
            SELECT id_pelicula, titulo, director, fecha_estreno, sinopsis,
                   usuario_id, created_at, updated_at
            FROM peliculas WHERE titulo = %(titulo)s;
        """
        resultado = connectToMySQL(BASE).query_db(consulta, {"titulo": titulo})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def actualizar(cls, datos):
        consulta = """
            UPDATE peliculas
            SET titulo = %(titulo)s, director = %(director)s,
                fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s,
                updated_at = NOW()
            WHERE id_pelicula = %(id_pelicula)s;
        """
        return connectToMySQL(BASE).query_db(consulta, datos)

    @classmethod
    def borrar(cls, id_pelicula):
        consulta = "DELETE FROM peliculas WHERE id_pelicula = %(id_pelicula)s;"
        return connectToMySQL(BASE).query_db(consulta, {"id_pelicula": id_pelicula})

    @staticmethod
    def validar_datos(datos):
        valido = True
        titulo = datos.get("titulo", "").strip()
        if len(titulo) < 3:
            flash("El nombre de la película debe tener al menos 3 caracteres.", "error")
            valido = False
        else:
            existente = Pelicula.obtener_por_titulo(titulo)
            if existente and str(getattr(existente, "id_pelicula", "")) != str(datos.get("id_pelicula", "")):
                flash("Ya existe una película con ese nombre.", "error")
                valido = False

        director = datos.get("director", "").strip()
        if len(director) < 3:
            flash("El director debe tener al menos 3 caracteres.", "error")
            valido = False

        fecha = str(datos.get("fecha_estreno") or "").strip()
        if not fecha:
            flash("La fecha de estreno no puede estar vacía.", "error")
            valido = False
        else:
            from datetime import date
            try:
                date.fromisoformat(fecha)
            except ValueError:
                flash("La fecha de estreno no es válida.", "error")
                valido = False

        sinopsis = datos.get("sinopsis", "").strip()
        if len(sinopsis) < 3:
            flash("La sinopsis debe tener al menos 3 caracteres.", "error")
            valido = False
        return valido
