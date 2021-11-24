from abc import ABC, abstractmethod

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

    def __str__(self) -> str:
        return 'Cancion: {} // Artista: {}'.format(self.nombre_cancion, self.artista)

class IPerrotify(ABC):

    @abstractmethod
    def canciones_top(termino : str) -> list:
        pass

    def artistas_top(termino : str) -> list:
        pass

class IBaseDatos(ABC):

    @abstractmethod
    def insertar_usuario(self, nom):
        pass

    @abstractmethod
    def insertar_canciones(self, cancion : Cancion):
        #datos necesarios para insertar, id_usuario, cancion_nombre, artista
        pass

    @abstractmethod
    def seleccionar_usuario(self, id_usuario):
        pass

    @abstractmethod
    def seleccionar_canciones(self):
        pass

    @abstractmethod
    def filtrar_artistas(self, artista):
        pass