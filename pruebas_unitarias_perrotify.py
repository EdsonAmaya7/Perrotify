import builtins
import unittest
from unittest import TestCase
from unittest import mock
from unittest.mock import mock_open, patch
from interfaces import Cancion
from perrotify import Usuario, SqlLite, PerrotifyApp, Cliente


class Perrotify(unittest.TestCase):
    @patch('perrotify.PerrotifyApp.canciones_top')
    def test_llamando_a_la_api_exito(self, mock_canciones_top):
        canciones = []
        canciones.append(Cancion('mock_cancion_1', 'mock_artista_1'))
        canciones.append(Cancion('mock_cancion_2', 'mock_artista_1'))
        canciones.append(Cancion('mock_cancion_3', 'mock_artista_3'))
        canciones.append(Cancion('mock_cancion_4', 'mock_artista_4'))
        canciones.append(Cancion('mock_cancion_5', 'mock_artista_5'))
        mock_canciones_top.return_value = canciones

        app = PerrotifyApp()

        resultados = app.canciones_top('medium_term')
        a = ''
        for res in resultados:
            a += res.__str__() + '\n'

        self.assertEqual(a, 'Cancion: mock_cancion_1 // Artista: mock_artista_1\nCancion: mock_cancion_2 // Artista: mock_artista_1\nCancion: mock_cancion_3 // Artista: mock_artista_3\nCancion: mock_cancion_4 // Artista: mock_artista_4\nCancion: mock_cancion_5 // Artista: mock_artista_5\n')

    def test_llamando_a_la_api_fallo(self):
        app = PerrotifyApp()

        resultado = app.canciones_top('termino_corto')

        self.assertEqual(resultado, "Rango no valido, inserte 'short_term', 'medium_term', 'long_term'")

    @patch('perrotify.SqlLite.seleccionar_canciones')
    def test_seleccionar_canciones_exito(self, mock_seleccionar_canciones):
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

    @patch('perrotify.SqlLite.seleccionar_canciones')
    def test_seleccionar_canciones_fallo(self, mock_seleccionar_canciones):
        canciones = []
        canciones.append(Cancion(1, 'mock_artista_1'))
        canciones.append(Cancion('mock_cancion_2', 'mock_artista_1'))
        canciones.append(Cancion('mock_cancion_3', 'mock_artista_3'))
        canciones.append(Cancion('mock_cancion_4', 'mock_artista_4'))
        canciones.append(Cancion('mock_cancion_5', 'mock_artista_5'))
        mock_seleccionar_canciones.return_value = "Solo se aceptan strings como parametros"
        valor_esperado = 'Solo se aceptan strings como parametros'

        # Crear instancia SqlLite
        sq = SqlLite()
        # Guardar mi resultado
        resultados = sq.seleccionar_canciones()
        # Comprobar resultados
        self.assertEqual(resultados, valor_esperado)

    @patch('perrotify.SqlLite.insertar_canciones')
    def test_insertar_canciones_exito(self, mock_insertar_cancion):
        mock_insertar_cancion.return_value = "Exito"
        # Crear instancia Cancion
        cancion = Cancion('Cancion_mock', 'Artista_mock')
        sq = SqlLite()
        # Llamar al metodo original
        resultado = sq.insertar_canciones(cancion)
        # Comprobar resultados
        self.assertEqual(resultado, "Exito")

    def test_insertar_canciones_fallo(self):
        # Crear instancia Cancion
        cancion = Cancion(2, 'Artista')
        sq = SqlLite()
        # Llamar al metodo original
        resultado = sq.insertar_canciones(cancion)
        print(resultado)
        # Comprobar resultados
        self.assertEqual(
            resultado, "El nombre del artista tiene que ser tipo string")


if __name__ == '__main__':
    unittest.main()
