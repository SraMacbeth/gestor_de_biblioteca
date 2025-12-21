import unittest
from tests import test_db_setup
from models.book_model import Book

# Se definen constantes para los tests
STATUS_AVAILABLE = "Disponible"
STATUS_LOANED = "Prestado"
TEST_ISBN ="9789500739718"
TEST_USER_ID = 1

class TestBookModel(unittest.TestCase):
		
	# --- Configuración del entorno de prueba --- 
	
	@classmethod
	def setUpClass(cls):
		""" Se ejecuta una vez: Crea las tablas de la DB de prueba. """
		test_db_setup.create_tables()
	
	def setUp(self):
		""" Se ejecuta antes de cada test. """
        # Asegurar que las tablas existan (por si el archivo se borró o está vacío
		test_db_setup.create_tables()
        
        # Limpiar datos de tests anteriores pero mantener las tablas
		test_db_setup.clear_tables()
        
        # Volver a llamar a create_tables para que se carguen los GÉNEROS (ya que clear_tables borró la tabla genre)
		test_db_setup.create_tables()
        
        # Insertar el usuario obligatorio para que la Foreign Key no falle
		conn = test_db_setup.get_test_connection()
		cursor = conn.cursor()
		cursor.execute(
            "INSERT INTO user (user_id, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)",
            (TEST_USER_ID, "Admin", "Test", "admin@test.com", "1234")
        )
		conn.commit()
		conn.close()

	@classmethod
	def tearDownClass(cls):
		"""Se ejecuta una vez después de TODAS las pruebas. Borra el archivo DB."""
		# Puedes comentar esta línea si quieres inspeccionar el archivo DB de prueba después de correr los tests
		#test_db_setup.drop_database()
		pass
		
	# --- TESTS DE INVENTARIO Y SEGURIDAD ---
	def test_insercion_correcta(self):
		"""Prueba que un nuevo libro se añade y se recupera por su ID."""

		libro_a_agregar = ["Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1, TEST_USER_ID]
		
		# Act: Intentamos insertar
		exito = Book.add_book(*libro_a_agregar)
		self.assertTrue(exito, "La inserción falló")

		# Verificación: Como es el primer test, el ID debería ser 1
		# Pero lo más profesional es buscarlo en la DB por su ISBN para obtener el ID real
		conn = test_db_setup.get_test_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
		row = cursor.fetchone()
		generated_id = row[0]
		conn.close()

		# Ahora probamos TU función get_book_by_id con ese ID
		datos_libro = Book.get_book_by_id(generated_id)
		
		# Assert
		self.assertIsNotNone(datos_libro, "No se encontró el libro con el ID generado")
		# Según tu modelo, datos_libro[0] es la tupla del libro
		self.assertEqual(datos_libro[0][2], "Rayuela", "El título no coincide")	
		