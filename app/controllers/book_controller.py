from models.book_model import Book, STATUS
import re

# TODO: Reemplazar por el ID del usuario logueado cuando el sistema de login esté conectado
CURRENT_USER_ID = 1

def is_id_valid(book_id):
	
	"""
	Valida el formato del ID ingresado por el uuario
	Parametros: 
	book_id(int) ID del libro buscado
	Retorna True si el ID coincide con el patron establecido o False si no coincide
	"""
	
	return bool(re.fullmatch(r'\d+', book_id))

def search_book_by_id(book_id):
			
	if book_id == "":
		return {"estado": "error", "mensaje":"El campo de búsqueda no puede estar vacío."}
	if not is_id_valid(book_id):
		return {"estado": "error", "mensaje":"El ID ingresado sólo puede contener números."}
	
	book = Book.get_book_by_id(book_id)
	
	if book == None:
		return {"estado": "error", "mensaje":"No existen libros registrados para el ID ingresado."}
	else:
		
		book_items, author_name, genre_name, copies = book

		total_copies = len(copies)
						
		id_book = book_items[0]
		
		title = book_items[2]
				
		author_firstname, author_lastname = author_name[0]
		
		genre = genre_name[0]
		
		isbn = book_items[1]
		
		publisher = book_items[3]
		
		status = book_items[6]
		
		book_details = [id_book, title,author_firstname, author_lastname, genre, isbn, publisher, total_copies, status,copies]
				
		return {"estado": "ok", "mensaje":"Libro encontrado", "detalles" : book_details} 

def add_book(title, authors, genre, isbn, publisher, copies):
	
	"""
	agrega un nuevo libro en la base de datos
	Parametros: 
	isbn(int) isbn del libro
	title(str) título del libro
	authors(str) nombre y apellido de los autores
	publisher(str) editorial
	genre(str) género al que pertenece el libro
	user_id(int) id del usuario que ingresó el libro
	copies(str) cantidad de copias ingresadas
	Retorna diferentes mensajes en funcion de los casos
	"""	
	
	if title == "" or authors[0][0] == "" or authors[0][1] == "" or genre == "" or isbn == "" or publisher == "" or copies == "":
		return {"estado": "error", "mensaje":"Los campos no pueden estar vacíos"}
		
	new_book = Book.add_book(title, authors, genre, isbn, publisher, copies, status=STATUS,user_id=CURRENT_USER_ID)
	
	if new_book == False:
		return {"estado": "error", "mensaje": f"El libro que intenta ingresar ISBN {isbn} ya se encuentra en la base de datos. \nUse el formulario de Edición para ajustar la cantidad de copias."}
	else:
		return {"estado": "ok", "mensaje":"Libro ingresado exitosamente."}

def update_book(book_id, title, authors, genre, isbn, publisher, copies, status, unavailable_reason):

	"""
	actualiza un libro existente en la base de datos
	Parametros: 
	book_id (int) identificador del libro
	title(str) título del libro
	authors(str) nombre y apellido de los autores
	genre(str) género al que pertenece el libro
	isbn(int) isbn del libro
	publisher(str) editorial
	copies(str) cantidad de copias ingresadas
	status (str) estado del libro en el inventario
	unavailable_reason (str) motivo por el cual un libro no esta disponible para prestamo
	user_id(int) id del usuario que ingresó el libro
	Retorna diferentes mensajes en funcion de los casos
	"""

	if title == "" or authors[0][0] == "" or authors[0][1] == "" or genre == "" or isbn == "" or publisher == "" or copies == "" or status == "":
		return {"estado": "error", "mensaje":"Los campos no pueden estar vacíos"}
		
	updated_book = Book.update_book(book_id, title, authors, genre, isbn, publisher, copies, status, unavailable_reason, user_id=CURRENT_USER_ID)
	
	if updated_book == False:
		return {"estado": "error", "mensaje": updated_book[1]}
	else:
		return {"estado": "ok", "mensaje":updated_book[1]}