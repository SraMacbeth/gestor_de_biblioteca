import sqlite3

def get_db_connection():
	
	"""
	Establece la conexion con la base de datos
	No recibe parametros
	Retorna la conexion
	""" 	
	
	return sqlite3.connect("db/biblioteca.db")

def setup_database():
	
	"""
	Crea la base de datos
	No recibe parametros
	"""
	
	try:
		connection = get_db_connection()
		cursor = connection.cursor()
		
		cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);")
		
		cursor.execute("CREATE TABLE IF NOT EXISTS author (author_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL);")
		
		cursor.execute("CREATE TABLE IF NOT EXISTS member (member_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, address TEXT NOT NULL, email TEXT NOT NULL, phone_number TEXT NOT NULL);")
		
		cursor.execute("CREATE TABLE IF NOT EXISTS genre (genre_id INTEGER PRIMARY KEY, name TEXT NOT NULL);")
		
		cursor.execute("CREATE TABLE IF NOT EXISTS book (book_id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, title TEXT NOT NULL, genre_id INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (genre_id) REFERENCES genre(genre_id), FOREIGN KEY (user_id) REFERENCES user(user_id));")
		
		cursor.execute("CREATE TABLE IF NOT EXISTS book_author (book_id INTEGER, author_id INTEGER, FOREIGN KEY (book_id) REFERENCES book(book_id), FOREIGN KEY (author_id) REFERENCES author(author_id));")
		
		cursor.execute("CREATE TABLE IF NOT EXISTS book_genre (book_id INTEGER, genre_id INTEGER, FOREIGN KEY (book_id) REFERENCES book(book_id), FOREIGN KEY (genre_id) REFERENCES genre(genre_id));")
		
		cursor.execute("CREATE TABLE IF NOT EXISTS copy (copy_id INTEGER PRIMARY KEY, book_id INTEGER, isbn TEXT NOT NULL, status TEXT NOT NULL, user_id INTEGER, FOREIGN KEY (book_id) REFERENCES book(book_id), FOREIGN KEY (user_id) REFERENCES user(user_id));")
		
		cursor.execute("CREATE TABLE IF NOT EXISTS loan (loan_id INTEGER PRIMARY KEY, member_id INTEGER, copy_id INTEGER, loan_date DATE NOT NULL, due_date DATE NOT NULL, return_date DATE NOT NULL, user_id INTEGER, FOREIGN KEY (member_id) REFERENCES member(member_id), FOREIGN KEY (copy_id) REFERENCES copy(copy_id), FOREIGN KEY (user_id) REFERENCES user(user_id));")
		
		connection.commit()
		connection.close()
	except sqlite3.Error as e:
		print(e)
