import builtins
import unittest
from unittest import TestCase
from unittest import mock
from unittest.mock import mock_open, patch
from interfaces import Cancion
from perrotify import Usuario, SqlLite, PerrotifyApp, Cliente


class PerrotifyIntegration(unittest.TestCase):
    # comentado causa conflictos con los test porque el mock inserta los registros en la bd
    # @patch('perrotify.PerrotifyApp.canciones_top')
    # def test_cliente_con_insertar_canciones(self, mock_canciones_top):
    #     canciones = []
    #     canciones.append(Cancion('mock_cancion_1', 'mock_artista_1'))
    #     canciones.append(Cancion('mock_cancion_1', 'mock_artista_2'))
    #     canciones.append(Cancion('mock_cancion_1', 'mock_artista_3'))
    #     mock_canciones_top.return_value = canciones
    #     # mock_insertar_cancion.return_value = "Exito"
    #     app = PerrotifyApp()
    #     sq = SqlLite()
    #     canciones_top = app.canciones_top()
    #     # resultados = app.canciones_top()

    #     for cancion in canciones_top:
    #         res = sq.insertar_canciones(cancion)
    #         self.assertEqual(res, "Exito")
    #         # print(cancion)

    # ---------------------------------------------------------------------------
    #                            esto ya estaba comentado
    # ---------------------------------------------------------------------------
    # @patch('perrotify.PerrotifyApp.canciones_top')
    # def test_canciones_top(self,mock_canciones_top):
    #     mock_canciones_top.return_value = 'Cancion: Cancion_mock // Artista: Artista_mock\nCancion: Cancion_mock // Artista: Artista_mock\nCancion: Cancion_mock // Artista: Artista_mock\n'

    #     sq = SqlLite()
    #     res = sq.seleccionar_canciones()

    #     a = ''
    #     for result in res:
    #         a += result.__str__() + '\n'

    #     self.assertEqual(a,mock_canciones_top.return_value)

    # ---------------------------------------------------------------------------
    #    prueba integraicion, seleccionar_canciones con insertar_canciones
    # ---------------------------------------------------------------------------

    def test_seleccionar_canciones_con_insertar_cancion(self):
        canciones = []
        with patch('perrotify.SqlLite.seleccionar_canciones', return_value=canciones):
            canciones.append(Cancion('mock_cancion_1', 'mock_artista_1'))
            sq = SqlLite()

            resultados = sq.seleccionar_canciones()
            a = ''
            for res in resultados:
                a += res.__str__()

            self.assertEqual(
                a, 'Cancion: mock_cancion_1 // Artista: mock_artista_1')


# ---------------------------------------------------------------------------
#            prueba integraicion con 1 real, el de seleccionar?canciones()
# ---------------------------------------------------------------------------


    def test_seleccionar_canciones(self):
        with patch('perrotify.SqlLite.seleccionar_canciones', return_value='Cancion: cancion de la hogera // Artista: Bob Esponja'):
            sq = SqlLite()
            resultados = sq.seleccionar_canciones()
            a = ''
            for res in resultados:
                a += res.__str__()
            self.assertEqual(
                a, "Cancion: cancion de la hogera // Artista: Bob Esponja")


# ===========================================================================
#                            prueba integracion 1 real
# ===========================================================================


    def test_filtrar_artista(self):
        with patch('perrotify.SqlLite.filtrar_artistas', return_value='Cancion: s // Artista: ZZ Top'):
            artista = 'ZZ Top'
            sq = SqlLite()
            resultados = sq.filtrar_artistas(artista)
            a = ''
            for res in resultados:
                a += res.__str__()
            print('a', a)
            self.assertEqual(a, "Cancion: s // Artista: ZZ Top")

# ===========================================================================
#                      prueba integracion  canciones_top
# ===========================================================================
    @patch('builtins.input')
    def test_canciones_top(self, mock_input):
        # with patch('builtins.input', return_value=2):
        # Hacemos que solo nos regrese 2 canciones para nuestra prueba
        mock_input.return_value = 2
        salida_esperada = 'Cancion: Sharp Dressed Man - 2008 Remaster  // Artista: ZZ Top'
        sq = SqlLite()

        resultados = sq.seleccionar_canciones()
        a = ''
        for res in resultados:
            a += res.__str__()
            print('a,a', a)
        self.assertEqual(salida_esperada, a)

# ---------------------------------------------------------------------------
#                            prueba integraicion con dos reales
# ---------------------------------------------------------------------------

    def test_filtrar_artista(self):
        artista = 'ZZ Top'
        sq = SqlLite()
        resultados = sq.filtrar_artistas(artista)
        a = ''
        for res in resultados:
            a += res.__str__()
        self.assertEqual(
            a, "Cancion: Sharp Dressed Man - 2008 Remaster  // Artista: ZZ Top")


if __name__ == '__main__':
    unittest.main()