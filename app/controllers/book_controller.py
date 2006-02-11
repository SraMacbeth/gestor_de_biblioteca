from models.book_model import Book
import re

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
						
		id_book = book_items[0]
		
		title = book_items[2]
				
		author_firstname, author_lastname = author_name[0]
		
		genre = genre_name[0]
		
		isbn = book_items[1]
		
		publisher = book_items[3]
		
		copies_number = len(copies)
		
		book_details = [id_book, title,author_firstname, author_lastname, genre, isbn, publisher, copies_number]
				
		return {"estado": "ok", "mensaje":"Libro encontrado", "detalles" : book_details} 
