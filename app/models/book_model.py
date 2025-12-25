import sqlite3
from . import db 

STATUS_AVAILABLE = "Disponible"
STATUS_LOANED = "Prestado"
INITIAL_STATUS = "Activo" 
STATUS_REASON = "Alta"

class Book():
	
	def __init__(self, book_id, isbn, title, publisher, genre_id, user_id, initial_status, status_reason, copies=0):
		self.book_id = book_id 
		self.isbn = isbn
		self.title = title
		self.publisher = publisher  
		self.genre_id = genre_id
		self.user_id = user_id
		self.initial_status = initial_status
		self.status_reason = status_reason
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
				cursor.execute("SELECT book_id, isbn, title, publisher, genre_id, user_id, initial_status, status_reason FROM book WHERE book_id = ?;", (book_id, ))
				
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
					cursor.execute("SELECT * FROM copy WHERE book_id = ?;", (book_id,))
					
					copies = cursor.fetchall()
					
					return book, author_name, genre_name, copies,INITIAL_STATUS, STATUS_REASON
				
				else:
					return book
				
		except sqlite3.Error as e:
			print(e)
			
	@classmethod
	def add_book(cls, title, authors, genre, isbn, publisher, copies, initial_status, status_reason, user_id):
		
		"""
		Inserta los datos de un nuevo libro en la base de datos
		Parametros: 
		isbn(int) idstr) isbn del libro
		title(str) título del libro
		authors(str) nombre y apellido de los autores
		publisher(str) editorial
		genre(str) género al que pertenece el libro
		user_id(int) id del usuario que ingresó el libro
		copies(str) cantidad de copias ingresadas
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
					cursor.execute("INSERT INTO book (isbn, title, publisher, genre_id, user_id, initial_status, status_reason) VALUES(?, ?, ?, ?, ?, ?, ?);", (isbn, title, publisher, genre_id, user_id, initial_status, status_reason))
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
						cursor.execute("INSERT INTO copy (book_id, isbn, status, user_id) VALUES (?, ?, ?, ?)", (book_id, isbn, STATUS_AVAILABLE, user_id))
						
					connection.commit()
					return True
					
		except sqlite3.Error as e:
			print(f"\n--- ERROR DE SQLITE EN ADD_BOOK: {e} ---") # Esta línea te dirá la verdad			
			return False
	

	
				 
