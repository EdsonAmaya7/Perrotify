import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import  patch
from interfaces import *
from perrotify import *

class Perrotify(unittest.TestCase):

    def test_seleccionar_canciones(self):
        # Creamos nuestro patch a nuestra base de datos
        with patch('perrotify.sqlite3') as mocksql:
            # Hacemos que el fetchall nos regrese canciones
            mocksql.connect().cursor().fetchall.return_value = [(0, 'Cancion_mock0', 'Artista_mock0'), (1, 'Cancion_mock1', 'Artista_mock1'), (2, 'Cancion_mock2', 'Artista_mock2')]
            # Creamos una instancia de SqlLite() donde se encuentra nuestro metodo seleccionar_usuario
            sql = SqlLite()
            # Llamamos a nuestro metodo seleccionar canciones, el cual nos deberia de traer nuestras
            # canciones mockeadas
            canciones = sql.seleccionar_canciones()
            # Comprobamos que cada cancion de nuestro select sea igual a nuestra salida esperada
            for i, cancion in enumerate(canciones):
                cancion_actual = cancion.__str__()
                self.assertEqual(cancion_actual, 'Cancion: Cancion_mock{} // Artista: Artista_mock{}'.format(i, i))

    def test_canciones_top(self):
        # Creamos nuestro patch de nuestra API, especificamente del curret_user_top_tracks, que se encarga de traernos nuestras canciones top de Spotify
        with patch('perrotify.spotipy.Spotify.current_user_top_tracks') as mockSpotipy:
            # Hacemos que solo nos regrese 2 canciones para nuestra prueba
            mockSpotipy.return_value = {'items': [
            {'artists': [{'name': 'Boney M.'}],'name': 'Ma Baker'}, 
            {'artists': [{'name': 'Iron Maiden'}],'name': 'The Trooper'}
            ]}
            # Creamos una instancia de PerrotifyApp() donde se encuentra nuestro metodo canciones_top
            app = PerrotifyApp()
            # Llamamos a canciones_top que este metodo nos regresa una lista de tipo Cancion, ahi es donde tambien se hace el llamado a nuestra api, y las almacenamos en una variable canciones
            canciones = app.canciones_top()
            # Creamos nuestras comparaciones, estos sera con lo que nuestra salida se comparara
            cancion_comparar = ['Ma Baker', 'The Trooper']
            artista_comparar = ['Boney M.', 'Iron Maiden']
            # Comprobamos que cada elemento la lista de tipo Cancion que nos regresa nuestro metodo canciones_top sea igual a nuestras comparaciones anteriores
            for i, cancion in enumerate(canciones):
                cancion_actual = cancion.__str__()
                self.assertEqual(cancion_actual, 'Cancion: {} // Artista: {}'.format(cancion_comparar[i], artista_comparar[i]))

    def test_filtrar_canciones(self):
        # Creamos nuestro patch a nuestra base de datos
        with patch('perrotify.sqlite3') as mocksql:
            # Hacemos que el fetchall nos regrese canciones
            mocksql.connect().cursor().execute.return_value = [(0, 'Cancion_mock0', 'Artista_mock0'), (1, 'Cancion_mock1', 'Artista_mock1'), (2, 'Cancion_mock2', 'Artista_mock2')]
            # Creamos una instancia de SqlLite() donde se encuentra nuestro metodo filtar_canciones
            sql = SqlLite()
            # Llamamos a nuestro metodo filtrar canciones, el cual nos deberia de traer nuestras
            # canciones mockeadas
            canciones = sql.filtrar_artistas('Artista_mock0')
            # Comprobamos que cada cancion de nuestro select where sea igual a nuestra salida esperada
            for i, cancion in enumerate(canciones):
                cancion_actual = cancion.__str__()
                self.assertEqual(cancion_actual, 'Cancion: Cancion_mock{} // Artista: Artista_mock{}'.format(i, i))
                




if __name__ == '__main__':
    unittest.main()
