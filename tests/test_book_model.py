import unittest
from tests import test_db_setup
from models.book_model import Book

#STATUS_AVAILABLE = "Disponible"
#STATUS_LOANED = "Prestado"
#TEST_ISBN ="9789500739718"
#TEST_USER_ID = 1

class TestBookModel(unittest.TestCase):
		
	# --- Configuración del entorno de prueba --- 
	
	@classmethod
	def setUpClass(cls):
		""" Se ejecuta una vez: Crea las tablas de la DB de prueba. """
		test_db_setup.create_tables()
	
	@classmethod
	def setUp(self):
		""" Se ejecuta antes de cada test: Limpia la DB de datos viejos. """
		test_db_setup.clear_tables()
		
	@classmethod
	def tearDownClass(cls):
		"""Se ejecuta una vez después de TODAS las pruebas. Borra el archivo DB."""
		# Puedes comentar esta línea si quieres inspeccionar el archivo DB de prueba después de correr los tests
		#test_db_setup.drop_database()
		pass
		
	# --- TESTS DE INVENTARIO Y SEGURIDAD ---

	
	# --- TESTS DE INVENTARIO Y SEGURIDAD ---
		
	def test_insercion_correcta(self):
		"""Prueba que un nuevo libro con datos válidos se añade correctamente y puede ser recuperado."""
		
		libro_a_agregar = ["Libro 1", [("Juan", "Pérez")], "Terror" , "123456789", "Casita", 1, 1]
		
		resultado = Book.add_book(libro_a_agregar)
		
		# PREPARACIÓN:
		
		#Conexión a la base de datos y creación del cursor 
		conn = test_db_setup.get_test_connection()
		cursor = conn.cursor()
		
		#Insertar un género y un libro de prueba
		cursor.execute("INSERT INTO genre (name) VALUES (?)", ("Ficción",))
		genre_id = cursor.lastrowid
		print(f"GENRE ID: {genre_id}")
		
		cursor.execute("INSERT INTO book (isbn, title, publisher, genre_id, user_id) VALUES (?, ?, ?, ?, ?)", (TEST_ISBN, "Título Test", "Edit", genre_id, TEST_USER_ID))
		book_id = cursor.lastrowid
		print(f"BOOK ID: {book_id}")
		
		# Insertar 3 Prestadas y 1 Disponible (Total 4)
		self._insert_test_data(conn, book_id, STATUS_LOANED, 3)
		self._insert_test_data(conn, book_id, STATUS_AVAILABLE, 1)
		conn.close()
		
		get_all_book_by_id = Book.get_book_by_id(1)
		print(get_all_book_by_id)
	
		# 1. EJECUCIÓN: Intentar reducir el stock de 4 a 1 (Borrar 3 copias)
		# Solo hay 1 disponible para borrar. El sistema debe bloquearse.
				
		resultado = Book.update_book(book_id=book_id, title="Título Test", authors=[("Test", "Author")], genre="Misterio", isbn=TEST_ISBN, publisher="Edit", new_copies_number=1, user_id=TEST_USER_ID, )
		
		# 2. VERIFICACIÓN
		self.assertFalse(resultado, "La reducción DEBE fallar.")
		
		# 3. VERIFICACIÓN DE INTEGRIDAD: Comprobar que no se borró NADA
		conn = test_db_setup.get_test_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT COUNT(*) FROM copy WHERE book_id = ?;", (book_id,))
		self.assertEqual(cursor.fetchone()[0], 4, "El conteo final de copias debe seguir siendo 4.")
		conn.close()
	
	# ... Aquí añadirías más tests: test_reducir_a_cero_falla, test_anadir_copias, etc.
	