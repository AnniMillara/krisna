from flask_app.config.mysqlconnection import connectToMySQL

BASE = "esquema_peliculas"


class Comentario:
    def __init__(self, datos):
        self.id_comentario = datos["id_comentario"]
        self.contenido = datos["contenido"]
        self.usuario_id = datos["usuario_id"]
        self.pelicula_id = datos["pelicula_id"]
        self.created_at = datos["created_at"]
        self.updated_at = datos["updated_at"]
        self.autor_nombre = datos.get("autor_nombre")
        self.autor_apellido = datos.get("autor_apellido")

    @classmethod
    def crear(cls, datos):
        consulta = """
            INSERT INTO comentarios (contenido, usuario_id, pelicula_id, created_at, updated_at)
            VALUES (%(contenido)s, %(usuario_id)s, %(pelicula_id)s, NOW(), NOW());
        """
        return connectToMySQL(BASE).query_db(consulta, datos)

    @classmethod
    def obtener_por_id(cls, id_comentario):
        consulta = """
            SELECT id_comentario, contenido, usuario_id, pelicula_id, created_at, updated_at
            FROM comentarios WHERE id_comentario = %(id_comentario)s;
        """
        resultado = connectToMySQL(BASE).query_db(consulta, {"id_comentario": id_comentario})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def listar_por_pelicula(cls, id_pelicula):
        consulta = """
            SELECT c.id_comentario, c.contenido, c.usuario_id, c.pelicula_id,
                   c.created_at, c.updated_at,
                   u.nombre AS autor_nombre, u.apellido AS autor_apellido
            FROM comentarios c
            JOIN usuarios u ON c.usuario_id = u.id_usuario
            WHERE c.pelicula_id = %(pelicula_id)s
            ORDER BY c.created_at DESC, c.id_comentario DESC;
        """
        resultados = connectToMySQL(BASE).query_db(consulta, {"pelicula_id": id_pelicula})
        return [cls(fila) for fila in resultados]

    @classmethod
    def borrar(cls, id_comentario):
        consulta = "DELETE FROM comentarios WHERE id_comentario = %(id_comentario)s;"
        return connectToMySQL(BASE).query_db(consulta, {"id_comentario": id_comentario})
