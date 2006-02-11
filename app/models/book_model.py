import sqlite3
from models import db 

class Book():
	
	def __init__(self, book_id, isbn, title, genre_id, user_id):
		self_book_id = book_id
		self.isbn = isbn
		self.title = title
		self.genre_id = genre_id
		self.user_id = user_id
		
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
				cursor.execute("SELECT * FROM book WHERE book_id = ?;", (book_id, ))
				
				book = cursor.fetchone()
				
				if book is not None:
				
					#Extraer ID del género del libro
					cursor.execute("SELECT genre_id FROM book WHERE book_id = ?;", (book_id, ))
					
					genre_id = cursor.fetchone()
									
					#Obtener nombre del género 
					cursor.execute("SeLECT name FROM genre WHERE genre_id = ?;", (genre_id[0],))
					
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
					
					return book, author_name, genre_name, copies
				
				else:
					return book
				
		except sqlite3.Error as e:
			print(e)
				 
