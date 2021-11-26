from sqlite3.dbapi2 import Cursor
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sqlite3
from interfaces import Cancion, IPerrotify, IBaseDatos
import configparser


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

    def insertar_canciones(self, cancion: Cancion):
        cancion_nombre = cancion.get_nombre_cancion()
        artista = cancion.get_artista()
        # Ejecutar query INSERT pasandole 'id_usuario' y 'cancion_nombre' como argumento.
        self.cursor.execute('insert into cancion(nombreCancion, artista) values ("{}", "{}")'.format(
            cancion_nombre, artista))

        # Hacer un commit para que se guarden los cambios permanentemente.
        # Comprobar si se inserto
        if not isinstance(cancion_nombre, int):
            if (self.cursor.rowcount == 1):
                self.mi_conexion.commit()
                return "Exito"
            else:
                return "Fallo"
        else:
            return "El nombre del artista tiene que ser tipo string"

    def seleccionar_usuario(self, id_usuario):
        # Ejecutar query SELECT pasandole 'id_usuario' como argumento.
        self.cursor.execute(
            "select * from usuario where idUsuario = {}".format(id_usuario))
        # Recuperar nuestro SELECT en la variable datos
        datos = self.cursor.fetchall()
        # Mostrar nuestro SELECT
        print(datos)

    def seleccionar_canciones(self):
        # Ejecutar query SELECT
        self.cursor.execute("select * from cancion")
        # Recuperar nuestro SELECT en la variable datos
        datos = self.cursor.fetchall()
        # Var para concatenar resultados
        if (datos):
            canciones = []
            for dato in datos:
                if (not isinstance(dato, str)):
                    canciones.append(Cancion(dato[1], dato[2]))
                else:
                    return "Solo se aceptan strings como parametros"
            return canciones
        else:
            return "Fallo"

    def filtrar_artistas(self, artista):
        # Ejecutar query SELECT
        self.cursor.execute(
            "select * from cancion WHERE artista = '{}'".format(artista))
        # Recuperar nuestro SELECT en la variable datos
        datos = self.cursor.fetchall()
        canciones = []
        for dato in datos:
            canciones.append(Cancion(dato[1], dato[2]))
            print(dato)

        return canciones

class PerrotifyApp(IPerrotify):

    def __init__(self) -> None:
        # Leer credenciales del archivo credenciales.ini
        # self.leer = configparser.ConfigParser()
        # self.leer.read("credenciales.ini")

        self.leer = configparser.ConfigParser()
        self.leer.read("credenciales.ini")
        self.cliente_ID = self.leer.get("Credenciales", "client_id")
        self.cliente_secret = self.leer.get("Credenciales", "client_secret")

    def canciones_top(self, range):
        # Usar client_id, client_secret, redirect_uri, scope para conectarnos a nuestra cuenta de desarrollador.
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='231ff96968584dfa9078830f4b75ccec',
                                                       client_secret='4250cbcc6f1948d18b8050c63a2e96cb',
                                                       redirect_uri='https://open.spotify.com/collection/tracks',
                                                       scope='user-top-read'))

        if (range == 'short_term' or range == 'medium_term' or range == 'long_term'):
            ranges = [range]
            canciones = []
        else:
            return "Rango no valido, inserte 'short_term', 'medium_term', 'long_term'"

        # Recorrer una lista de resultados de la API, y crear una lista de clase Cancion
        for sp_range in ranges:
            print("range:", sp_range)
            results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
            if (results):
                for i, item in enumerate(results['items']):
                    canciones.append(
                        Cancion(item['name'], item['artists'][0]['name']))
                return canciones
            else:
                return "Datos no recolectados aaah que rabia"


class Cliente:

    def menu(self):
        sq = SqlLite()
        sp = PerrotifyApp()

        ans = True

        while ans:
            print('----Menu----'.center(100, "="))
            print("""\n
                                                ---Opciones---
        1.- Canciones Top

        --- Consutas de la BD ---

        2.- Seleccionar Canciones
        3.- Ordenar por Artista
        0.- --- Exit ---
        """)
            ans = input("Ingresa la opcion que deseas: ")
            if ans == "1":
                print("\n---Canciones Top---")
                # Traer canciones top y crear clases Cancion con los datos traidos de la API.
                canciones = sp.canciones_top('medium_termss')
                if (isinstance(canciones, list)):
                    for cancion in canciones:
                        sq.insertar_canciones(cancion)

            elif ans == "2":
                print("\n---Seleccionar Canciones---")
                # Imprimir canciones top traidas desde la DB.
                canciones = sq.seleccionar_canciones()
                for cancion in canciones:
                    print(cancion.__str__())

            elif ans == "3":
                print("\n---Ordenar por Artista---")
                # Pedir entrada
                artista = input("Escribe el artista: ")
                # Imprimir cancion por artista
                sq.filtrar_artistas(artista)

            elif ans == "0":
                print("\n Adios!!!")
                ans = None
            else:
                print("\n Opcion no valida reintente otro valor")


if __name__ == '__main__':
    app = Cliente()
    app.menu()


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
