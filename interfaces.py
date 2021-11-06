from abc import ABC, abstractmethod

class IPerrotify(ABC):

    @abstractmethod
    def canciones_top(termino : str):
        pass

class IBaseDatos(ABC):

    @abstractmethod
    def insertar_usuario(self, nom):
        pass

    @abstractmethod
    def insertar_canciones(self, id_usuario, cancion_nombre):
        pass

    @abstractmethod
    def seleccionar_usuario(self, id_usuario):
        pass

    @abstractmethod
    def seleccionar_canciones_usuario(self, id_usuario):
        pass