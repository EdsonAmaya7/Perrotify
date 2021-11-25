import builtins
import unittest
from unittest import TestCase
from unittest import mock
from unittest.mock import mock_open, patch
from interfaces import Cancion
from perrotify import Usuario,SqlLite,PerrotifyApp,Cliente


class Perrotify(unittest.TestCase):
    @patch('perrotify.PerrotifyApp.canciones_top')
    def test_llamando_a_la_api(self, mock_canciones_top):
        canciones  = []
        canciones.append(Cancion('mock_cancion_1', 'mock_artista_1'))
        canciones.append(Cancion('mock_cancion_2', 'mock_artista_1'))
        canciones.append(Cancion('mock_cancion_3', 'mock_artista_3'))
        canciones.append(Cancion('mock_cancion_4', 'mock_artista_4'))
        canciones.append(Cancion('mock_cancion_5', 'mock_artista_5'))
        mock_canciones_top.return_value = canciones

        app = PerrotifyApp()

        resultados = app.canciones_top()
        a = ''
        for res in resultados:
            a += res.__str__() + '\n'

        self.assertEqual(a, 'Cancion: mock_cancion_1 // Artista: mock_artista_1\nCancion: mock_cancion_2 // Artista: mock_artista_1\nCancion: mock_cancion_3 // Artista: mock_artista_3\nCancion: mock_cancion_4 // Artista: mock_artista_4\nCancion: mock_cancion_5 // Artista: mock_artista_5\n')

    @patch('perrotify.SqlLite.seleccionar_canciones')
    def test_seleccionar_canciones(self, mock_seleccionar_canciones):
        canciones = []
        canciones.append(Cancion('mock_cancion_1', 'mock_artista_1'))
        canciones.append(Cancion('mock_cancion_2', 'mock_artista_1'))
        canciones.append(Cancion('mock_cancion_3', 'mock_artista_3'))
        canciones.append(Cancion('mock_cancion_4', 'mock_artista_4'))
        canciones.append(Cancion('mock_cancion_5', 'mock_artista_5'))
        mock_seleccionar_canciones.return_value = canciones

        sq = SqlLite()

        resultados = sq.seleccionar_canciones()
        a = ''
        for res in resultados:
            a += res.__str__() + '\n'

        self.assertEqual(a, 'Cancion: mock_cancion_1 // Artista: mock_artista_1\nCancion: mock_cancion_2 // Artista: mock_artista_1\nCancion: mock_cancion_3 // Artista: mock_artista_3\nCancion: mock_cancion_4 // Artista: mock_artista_4\nCancion: mock_cancion_5 // Artista: mock_artista_5\n')

    @patch('perrotify.SqlLite.insertar_canciones')
    def test_insertar_canciones(self, mock_insertar_cancion):
        mock_insertar_cancion.return_value = "Exito"

        # Crear instancia Cancion
        cancion = Cancion('Cancion_mock', 'Artista_mock')
        sq = SqlLite()
        # Llamar al metodo original
        resultado = sq.insertar_canciones(cancion)
        #Comprobar resultados
        self.assertEqual(resultado, "Exito")

    @patch('perrotify.SqlLite.filtrar_artistas')
    def test_filtrar_canciones(self, mock_filtrar_artistas):
        canciones = []
        canciones.append(Cancion("mock_cancion_1", "mock_artista_1"))
        canciones.append(Cancion("mock_cancion_2", "mock_artista_1"))
        canciones.append(Cancion("mock_cancion_3", "mock_artista_1"))
        canciones.append(Cancion("mock_cancion_4", "mock_artista_1"))
        canciones.append(Cancion("mock_cancion_5", "mock_artista_1"))
        mock_filtrar_artistas.return_value = canciones

        sq = SqlLite()

        resultados = sq.filtrar_artistas('mock_artista_1')
        a = ''
        for res in resultados:
            a += res.__str__() + '\n'

        self.assertEqual(a, 'Cancion: mock_cancion_1 // Artista: mock_artista_1\nCancion: mock_cancion_2 // Artista: mock_artista_1\nCancion: mock_cancion_3 // Artista: mock_artista_1\nCancion: mock_cancion_4 // Artista: mock_artista_1\nCancion: mock_cancion_5 // Artista: mock_artista_1\n')


if __name__ == '__main__':
    unittest.main()

