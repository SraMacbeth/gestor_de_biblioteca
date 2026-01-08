import os
os.environ['TESTING'] = 'True'

import unittest
from . import test_db_setup
from app.controllers import book_controller

# Se definen constantes para los tests
STATUS_LOAN_AVAILABLE = "Disponible"
STATUS_LOAN_LOANED = "Prestado"
STATUS_LOAN_UNAVAILABLE = "No disponible"
STATUS = "Activo" 
TEST_ISBN ="9789500739718"
TEST_USER_ID = 1

class TestBookController(unittest.TestCase):
    
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
    
    def test_estructura_de_busqueda(self):
        ''' Verifica que search_book_by_id devuelva un diccionario donde detalles[9] es efectivamente una lista de tuplas con las copias.'''

        # PREPARACIÓN:  
        # Insertar un libro manualmente para tener algo que buscar
            
        datos_libro = ["Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1]
            
        book_controller.add_book(*datos_libro)

        # Buscar el ID en la DB por el ISBN del libro
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = str(row[0])
        conn.close()

        # Obtener la lista de copias del libro de manera manual para comparar su estructura
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT copy_id, copy_code, status_loan, unavailable_reason FROM copy WHERE book_id = ?;", (generated_id,))
        copy_list = cursor.fetchall()
        conn.commit()

        # Act
        book = book_controller.search_book_by_id(generated_id)

        #Assert
        self.assertEqual(book['detalles'][9], copy_list, "La estructura de datos devuelta no es la esperada.")

    def test_inyeccion_de_usuario(self):
        '''Comprueba que al llamar a add_book desde el controlador, no se necesita pasar el ID de usuario, pero que en la base de datos el registro aparece con el ID 1 (CURRENT_USER_ID)'''

         # PREPARACIÓN: 
         # Datos del libro que se pasan al controlador y no incluyen el ID del usuario 
        datos_libro = ["Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1]

        # Act
        exito = book_controller.add_book(*datos_libro)

        # Buscar el ID del libro en la DB por su ISBN
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = str(row[0])
        conn.close()

        # Obtención del ID del usuario asignado en la DB
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM book WHERE book_id = ?;", (generated_id,))
        row = cursor.fetchone()
        user_id_in_db = row[0]
        conn.commit()

        # Assert
        self.assertEqual(user_id_in_db, book_controller.CURRENT_USER_ID , "El ID de usuario no coincide")
    
    def test_validar_copia_mayor_a_cero(self):

        '''
        Verifica que si se envía un 0 en el número de copias al agregar un libro, el controlador devuelve el mensaje de error esperado.
        '''

        # PREPARACIÓN:  
        # Insertar un libro con 0 copias manualmente     
        datos_libro = ["Rayuela", [("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 0]

        # Act    
        exito = book_controller.add_book(*datos_libro)

        # Assert
        self.assertEqual(exito["estado"], "error")
        self.assertEqual(exito["mensaje"], "El libro ingresado debe tener al menos una copia.")
        

