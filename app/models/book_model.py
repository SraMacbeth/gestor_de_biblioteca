import sqlite3
from . import db 

STATUS_LOAN_AVAILABLE = "Disponible"
STATUS_LOAN_LOANED = "Prestado"
STATUS_LOAN_UNAVAILABLE = "No disponible"
STATUS = "Activo" 

class Book():
	
	def __init__(self, book_id, isbn, title, publisher, genre_id, user_id, status, copies=0):
		self.book_id = book_id 
		self.isbn = isbn
		self.title = title
		self.publisher = publisher  
		self.genre_id = genre_id
		self.user_id = user_id
		self.status = status
		self.copies = copies
		
	@classmethod		
	def get_book_by_id(cls, book_id):
		
		"""
		Obtiene los datos del libro que coincide con el id ingresado
		Parametros: book_id(int) id del libro
		Retorna una tupla con los datos del libro si existe o None si no existe
		"""
		
		try:
			with db.get_db_connection() as connection: 
				cursor = connection.cursor()
								
				#Obtener datos del libro segun su ID
				cursor.execute("SELECT book_id, isbn, title, publisher, genre_id, user_id, status FROM book WHERE book_id = ?;", (book_id, ))
				
				book = cursor.fetchone()
				
				if book is not None:
				
					#Extraer ID del género del libro
					cursor.execute("SELECT genre_id FROM book WHERE book_id = ?;", (book_id, ))
					
					genre_id = cursor.fetchone()
									
					#Obtener nombre del género 
					cursor.execute("SELECT name FROM genre WHERE genre_id = ?;", (genre_id[0],))
					
					genre_name = cursor.fetchone()
					
					#Obtener ID del autor
					cursor.execute("SELECT author_id FROM book_author WHERE book_id = ?;", 
					(book_id,))
					
					author_id = cursor.fetchone()
											
					#Obtener nombre y apellido del autor
					cursor.execute("SeLECT first_name, last_name FROM author WHERE author_id = ?;", (author_id[0],))
					
					author_name = cursor.fetchall()
											
					#Obtener cantidad de copias
					cursor.execute("SELECT copy_id, copy_code, status_loan, unavailable_reason FROM copy WHERE book_id = ?;", (book_id,))
					
					copies = cursor.fetchall()
					
					return book, author_name, genre_name, copies
				
				else:
					return book
				
		except sqlite3.Error as e:
			print(e)
			
	@classmethod
	def add_book(cls, title, authors, genre, isbn, publisher, copies, status, user_id):
		
		"""
		Inserta los datos de un nuevo libro en la base de datos
		Parametros: 
		isbn(int) isbn del libro
		title(str) título del libro
		authors(str) nombre y apellido de los autores
		publisher(str) editorial
		genre(str) género al que pertenece el libro
		user_id(int) id del usuario que ingresó el libro
		copies(str) cantidad de copias ingresadas
		initial_status(str) estado inicial del libro en el inventario
		status_reason(str) motivo por el cual se produce el estado del libro en el inventario
		"""

		try:
			with db.get_db_connection() as connection: 
				cursor = connection.cursor()
				
				#Verificar si el libro existe en la base de datos
				cursor.execute("SELECT * FROM book WHERE isbn = ?", (isbn,))
				
				if cursor.fetchone():
					return False
					
				else:

					#Extraer genre_id o ingresar un nuevo género si no existe
					cursor.execute("SELECT genre_id FROM genre WHERE name = ?", (genre,))
					
					row = cursor.fetchone()
								
					if row:
						genre_id = row[0]
					else:
						cursor.execute("INSERT INTO genre (name) VALUES (?)", (genre,))
						genre_id = cursor.lastrowid
						
					#Insertar libro
					cursor.execute("INSERT INTO book (isbn, title, publisher, genre_id, user_id, status) VALUES(?, ?, ?, ?, ?, ?);", (isbn, title, publisher, genre_id, user_id, status))
					book_id = cursor.lastrowid
									
					#Verificar / insertar autores y asociar tablas
					for first_name, last_name in authors:
						cursor.execute("SELECT author_id FROM author WHERE first_name = ? AND last_name = ?", (first_name, last_name))
					
						row = cursor.fetchone()
										
						if row:
							author_id = row[0]
						else:
							cursor.execute("INSERT INTO author (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
							author_id = cursor.lastrowid
						
						cursor.execute("INSERT INTO book_author (book_id, author_id) VALUES (?, ?)", (book_id, author_id))
												
					#Insertar copias
					for i in range(copies):

						copy_code = f"{isbn}-{i+1}"

						cursor.execute("INSERT INTO copy (book_id, isbn, copy_code, status_loan, user_id) VALUES (?, ?, ?, ?, ?)", (book_id, isbn, copy_code, STATUS_LOAN_AVAILABLE, user_id))
						
					connection.commit()
					return True
					
		except sqlite3.Error as e:
			print(f"\n--- ERROR DE SQLITE EN ADD_BOOK: {e} ---")	
			return False

	@classmethod
	def update_book(cls, book_id, title, authors, genre, isbn, publisher, copies, status, unavailable_reason, user_id):
		
		"""
		Actualiza los datos de un libro existente en la base de datos
		Parametros: 
		isbn(int) isbn del libro
		title(str) título del libro
		authors(str) nombre y apellido de los autores
		publisher(str) editorial
		genre(str) género al que pertenece el libro
		user_id(int) id del usuario que ingresó el libro
		copies(str) cantidad de copias ingresadas
		initial_status(str) estado inicial del libro en el inventario
		status_reason(str) motivo por el cual se produce el estado del libro en el inventario
		"""
		
		try:
			with db.get_db_connection() as connection: 
				cursor = connection.cursor()

				# Validacion previa a la actualizacion para verificar el estado de las copias del libro antes de intentar pasarlo a Inactivo. 
				# Regla de integridad: un libro no puede estar inactivo si tiene copias prestadas
				if status == "Inactivo":

					# Cuenta la cantidad de copias prestadas
					cursor.execute("SELECT * FROM copy WHERE book_id = ? AND status_loan = ?;", (book_id, STATUS_LOAN_LOANED))
					
					loaned_copies = cursor.fetchall()
								
					loaned_copies_number = len(loaned_copies)

					if loaned_copies_number > 0:
						return False
				
				# Un libro no debería figurar como "Activo" (disponible en el catálogo) si el usuario ha decidido que tiene cero copias operativas.
				if status == "Activo" and copies == 0:
					return False

				#Extraer genre_id o ingresar un nuevo género si no existe
				cursor.execute("SELECT genre_id FROM genre WHERE name = ?", (genre,))
					
				row = cursor.fetchone()
								
				if row:
					genre_id = row[0]
				else:
					cursor.execute("INSERT INTO genre (name) VALUES (?)", (genre,))
					genre_id = cursor.lastrowid
				
				#Actualizar libro con los datos proporcionados
				cursor.execute("UPDATE book set isbn = ?, title = ?, publisher = ?, genre_id = ?, user_id = ?, status = ? WHERE book_id = ?", (isbn, title, publisher, genre_id, user_id, status, book_id))

				# Resetear las asociaciones de libro-autor en la tabla intermedia book_author antes de poner las nuevas
				cursor.execute("DELETE FROM book_author WHERE book_id = ?", (book_id,))

				# Insertar nuevos autores y asociar tablas
				for first_name, last_name in authors:
					cursor.execute("SELECT author_id FROM author WHERE first_name = ? AND last_name = ?", (first_name, last_name))
					
					row = cursor.fetchone()
										
					if row:
						author_id = row[0]
					else:
						cursor.execute("INSERT INTO author (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
						author_id = cursor.lastrowid
						
					cursor.execute("INSERT INTO book_author (book_id, author_id) VALUES (?, ?)", (book_id, author_id))

				# Si el usuario quiere pasar el libro a estado inacticvo, automaticamente todas sus copias se ponen como "No disponible"
				if status == "Inactivo":
					cursor.execute("UPDATE copy set status_loan = ?, unavailable_reason = 'Libro Inactivado' WHERE book_id = ?", (STATUS_LOAN_UNAVAILABLE, book_id))
				
				# De lo contrario, las copias se gestionan de manera independiente segun la cantidad que desee ajustar el usuario
				else:
					#Obtener cantidad de copias y actualizarlas
					cursor.execute("SELECT * FROM copy WHERE book_id = ?;", (book_id,))
					actual_copies = cursor.fetchall()
								
					actual_copies_number = len(actual_copies)
				
					if copies ==	actual_copies_number:
						
						pass
						
					elif copies > actual_copies_number:
						
						new_copies_to_insert = copies - actual_copies_number
						
						for _ in range(new_copies_to_insert):
							
							copy_code = f"{isbn}-{actual_copies_number + _ + 1}"

							cursor.execute("INSERT INTO copy (book_id, isbn, copy_code,status_loan, user_id) VALUES (?, ?, ?, ?, ?)", (book_id, isbn, copy_code, STATUS_LOAN_AVAILABLE, user_id))
							
					elif copies < actual_copies_number:
						
						copies_to_delete = actual_copies_number - copies
						
						cursor.execute("SELECT COUNT(*) FROM copy WHERE book_id = ? AND status_loan = ?;", (book_id, STATUS_LOAN_AVAILABLE))
						
						available_copies = cursor.fetchone()[0]
						
						if available_copies < copies_to_delete:
							return False

						# NO ELIMINAR LAS COPIAS SOLO PASARLAS A NO DISPONIBLE	
						cursor.execute("UPDATE copy SET status_loan = ?, unavailable_reason = ? WHERE rowid IN (SELECT rowid FROM copy WHERE book_id = ? AND status_loan = 'Disponible' LIMIT ?)", (STATUS_LOAN_UNAVAILABLE, unavailable_reason, book_id, copies_to_delete))

				connection.commit()

				return True				

		except sqlite3.Error as e:
			print(f"\n--- ERROR DE SQLITE EN UPDATE_BOOK: {e} ---")	
			return False	

	
				 
