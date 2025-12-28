import os
os.environ['TESTING'] = 'True'

import unittest
from . import test_db_setup
from app.models.book_model import Book

# Se definen constantes para los tests
STATUS_LOAN_AVAILABLE = "Disponible"
STATUS_LOAN_LOANED = "Prestado"
STATUS_LOAN_UNAVAILABLE = "No disponible"
STATUS = "Activo" 
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
        # Limpiar datos de tests anteriores pero mantener las tablas
		test_db_setup.clear_tables()
        
        # Insertar el usuario obligatorio para que la Foreign Key no falle
		conn = test_db_setup.get_test_connection()

		db_name = conn.execute("PRAGMA database_list").fetchall()[0][2]
		if "test_library.db" not in db_name:
			self.fail(f"¡PELIGRO! El test intentó conectarse a: {db_name}")

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
		"""Prueba que un nuevo libro se añade correctamente."""

		libro_a_agregar = ["Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1, STATUS,TEST_USER_ID]
		
		# Act: Intentamos insertar
		exito = Book.add_book(*libro_a_agregar)

		#Aseert
		self.assertTrue(exito, "La inserción falló")

	def test_buscar_por_id(self): 
		'''Asegura que get_book_by_id devuelve exactamente lo que se espera'''
		
		# PREPARACIÓN: Insertar un libro manualmente para tener algo que buscar
		libro_datos = ["Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1, STATUS, TEST_USER_ID]
		Book.add_book(*libro_datos)

		# Buscar el ID en la DB por el ISBN del libro
		conn = test_db_setup.get_test_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
		row = cursor.fetchone()
		generated_id = row[0]
		conn.close()

		# Act
		datos_libro = Book.get_book_by_id(generated_id)
		
		# Assert
		self.assertIsNotNone(datos_libro, "No se encontró el libro con el ID generado")
		
		# Verificar el libro encontrado por su titulo
		self.assertEqual(datos_libro[0][2], "Rayuela", "El título no coincide")	

	def test_buscar_por_id_inexistente(self):
		'''Asegura que si se busca un libro con un id inexistente devuelve el error'''
		
		# PREPARACIÓN: Insertar un libro manualmente para tener algo que buscar
		libro_datos = ["Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1, TEST_USER_ID, STATUS]
		Book.add_book(*libro_datos)

		# Buscar el ID del libro ingresado en la DB por el ISBN del libro
		conn = test_db_setup.get_test_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
		row = cursor.fetchone()
		generated_id = row[0]
		conn.close()

		# Id inexistente a buscar, se calcula en base al id generado.
		id_inexistente = generated_id + 1

		# Act
		datos_libro = Book.get_book_by_id(id_inexistente)
		
		# Assert
		self.assertIsNone(datos_libro, "Error: se encontró un libro con el ID ingresado")
		
	def test_actualizar_libro(self):

		"""Prueba que un libro existente se actualiza correctamente."""

		# PREPARACIÓN: Insertar un libro manualmente para tener algo que actualizar
		libro_datos = ["Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1, STATUS, TEST_USER_ID]
		Book.add_book(*libro_datos)

		# Buscar el ID en la DB por el ISBN del libro
		conn = test_db_setup.get_test_connection()
		cursor = conn.cursor()
		cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
		row = cursor.fetchone()
		generated_id = row[0]
		conn.close()

		print(Book.get_book_by_id(generated_id))

		# Crear los nuevps datps del libro
		nuevos_datos = [generated_id, "Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1, "Inactivo", None, TEST_USER_ID]
		
		# Act
		exito = Book.update_book(*nuevos_datos)

		# Assert
		self.assertTrue(exito, "La actualizacion fallo.")

		# Verificar el libro actualizado por su estado		
		libro_actualizado = Book.get_book_by_id(generated_id)
		print(libro_actualizado)
		self.assertEqual(libro_actualizado[0][6], "Inactivo", "El estado inicial no coincide")
		
		# Verificar que también ocurrió la consecuencia lógica (se modifico a "No disponible" el estado de las copias)
		self.assertEqual(libro_actualizado[3][0][3], "No disponible")	
		
	# def test_eliminar_libro(self): 
	# 	'''Verifica que al borrar un libro, también se borran sus copias (o se manejen las claves foráneas)'''
		
	# 	# PREPARACIÓN: Insertar un libro manualmente para tener algo que eliminar
	# 	libro_datos = ["Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1, TEST_USER_ID]
	# 	Book.add_book(*libro_datos)

	# 	# Buscar el ID del libro ingresado en la DB por el ISBN del libro
	# 	conn = test_db_setup.get_test_connection()
	# 	cursor = conn.cursor()
	# 	cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
	# 	row = cursor.fetchone()
	# 	generated_id = row[0]
	# 	conn.close()

	# 	# Act
	# 	datos_libro = Book.delete_b(generated_id)
		
	# 	# Assert
	# 	self.assertIsNone(datos_libro, "Error: se encontró un libro con el ID ingresado")

		



	