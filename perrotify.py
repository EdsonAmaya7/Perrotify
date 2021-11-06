from sqlite3.dbapi2 import Cursor
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sqlite3
from interfaces import *


class Usuario:

    def __init__(self, usuario) -> None:
        self.usuario = usuario
        self.canciones = []

    def set_usuario(self, usuario):
        self.usuario = usuario

    def get_usuario(self):
        return self.usuario

    def set_songs(self, canciones: list):
        self.canciones = canciones

    def get_songs(self):
        return self.canciones


class Cancion:

    def __init__(self, nombre_cancion, artista) -> None:
        self.nombre_cancion = nombre_cancion
        self.artista = artista

    def set_nombre_cancion(self, nombre_cancion):
        self.nombre_cancion = nombre_cancion

    def get_nombre_cancion(self):
        return self.nombre_cancion

    def set_artista(self, nombre_artista):
        self.artista = nombre_artista

    def get_artista(self):
        return self.artista


class SqlLite(IBaseDatos):

    def __init__(self) -> None:
        # Conectarnos a nuestra base de datos.
        self.mi_conexion = sqlite3.connect("database/spotify.db")
        # Declarar nuestro cursor, para hacer queries.
        self.cursor = self.mi_conexion.cursor()
        # Imprimir un mensaje de exito.
        print('-----------------Conectado exitosamente-----------------')

    def insertar_usuario(self, nom):
        # Ejecutar query INSERT pasandole 'nom' como argumento.
        self.cursor.execute(
            "insert into usuario(nombre) values ('{}')".format(nom))
        # Hacer un commit para que se guarden los cambios permanentemente.
        self.mi_conexion.commit()

    def insertar_canciones(self, id_usuario, cancion_nombre):
        # Ejecutar query INSERT pasandole 'id_usuario' y 'cancion_nombre' como argumento.
        self.cursor.execute("insert into cancion(nombreCancion, idUsuario) values ('{}', {})".format(
            cancion_nombre, id_usuario))
        # Hacer un commit para que se guarden los cambios permanentemente.
        self.mi_conexion.commit()

    def seleccionar_usuario(self, id_usuario):
        # Ejecutar query SELECT pasandole 'id_usuario' como argumento.
        self.cursor.execute(
            "select * from usuario where idUsuario = {}".format(id_usuario))
        # Recuperar nuestro SELECT en la variable datos
        datos = self.cursor.fetchall()
        # Mostrar nuestro SELECT
        print(datos)

    def seleccionar_canciones_usuario(self, id_usuario):
        # Ejecutar query SELECT pasandole 'id_usuario' como argumento.
        self.cursor.execute(
            "select u.nombre, c.nombreCancion from usuario as u inner join cancion as c on u.idUsuario = c.idUsuario where c.idUsuario = {}".format(id_usuario))
        # Recuperar nuestro SELECT en la variable datos
        datos = self.cursor.fetchall()
        # Mostrar nuestro SELECT
        print(datos)


class PerrotifyApp(IPerrotify):

    def canciones_top(self, termino: str):
        # Usar client_id, client_secret, redirect_uri, scope para conectarnos a nuestra cuenta de desarrollador.
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='',
                                                       client_secret='',
                                                       redirect_uri='https://open.spotify.com/collection/tracks',
                                                       scope='user-top-read'))

        ranges = [termino]

        # Imprimir las canciones top en nuestro rango de tiempo.
        for sp_range in ranges:
            print("Rango:", sp_range)
            results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
            for i, item in enumerate(results['items']):
                print(i, item['name'], '//', item['artists'][0]['name'])
            print()


class Cliente:
    # LOGICA PRINCIPAL DEL PROGRAMA

    sq = SqlLite()
    sp = PerrotifyApp()

    # ---------------INSERTAR USUARIOS---------------
    # sq.insertar_usuario('Chuy')
    # sq.insertar_usuario('Edson')
    # sq.insertar_usuario('Mario')

    # ---------------DEBUG: SELECT USUARIOS---------------
    # sq.seleccionar_usuario(1)
    # sq.seleccionar_usuario(2)
    # sq.seleccionar_usuario(3)

    # ---------------INSERT CANCIONES---------------
    sq.insertar_canciones(1, 'Genitallica - The Unforgiven')
    sq.insertar_canciones(1, 'Deathgasm - The Blood Spitter')
    sq.insertar_canciones(2, 'Bugs bunny - Perreo Hasta el Nucleo de la Tierra')
    sq.insertar_canciones(2, 'Copper Maiden - The Number of God')
    sq.insertar_canciones(3, 'Thangorodrim - Gil Estel')
    sq.insertar_canciones(3, 'Elffor - Dra Sad III')

    # ---------------DEBUG: SELECT CANCIONES POR IDUSUARIO---------------
    sq.seleccionar_canciones_usuario(1)
    sq.seleccionar_canciones_usuario(2)
    sq.seleccionar_canciones_usuario(3)

    # ---------------SPOTIPY API : CANCIONES TOP---------------
    sp.canciones_top('long_term')


if __name__ == '__main__':
    app = Cliente()


# ---------------PROXIMO A IMPLEMENTAR---------------
# 1.- Agregar el usuario automaticamente a la base de datos.
# 2.- Agregar canciones a la tabla Cancion y al Usuario correspondiente
#     automaticamente al llamar canciones_top.

    # ---------------ACLARACION---------------
#     1.- Solo habra un usuario (el actual) en la base de datos, a menos que se
#         implemente publicamente.

# 3.- Agregar pruebas de software.

# -----------------------------------------------------------------------------------------------------------

# 1.- Hacer interfaz por consola, que nos de a elegir: (Complejidad: Bajo)
#     -Canciones Top
#     -Artistas Top
#     -Consultas BD > Select Usuarios > Select Canciones
#     -Categorizar Canciones Top por Genero (Sí es que se puede, sino buscar otra forma de categorizar.)

# 2.- Cambiar el código para que funcione de acuerdo a lo que dijo ChioCode. (Complejidad: Medio)

# 3.- Agregar el metodo artistas_top (o similar) en la interfaz IPerrotify, y agregar su lógica en la clase 
# PerrotifyApp. (Complejidad: Medio)