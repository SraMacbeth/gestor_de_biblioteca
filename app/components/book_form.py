from tkinter import *
from tkinter import ttk
from controllers import book_controller, genre_controller

class BookForm(Toplevel):
	
	"""
	Formulario que permite cargar un nuevo libro.	
	"""	
	def __init__(self, form_title, parent, controller, type_form="", book_id="", user=None, book_title="", author_firstname="", author_lastname="", genre="", isbn="", publisher="", copies=""):
		super().__init__(parent)
		self.form_title = form_title
		self.controller = controller
		self.type_form = type_form
		self.book_id = book_id
		self.user = user
		self.book_title = book_title 
		self.author_firstname = author_firstname 
		self.author_lastname = author_lastname
		self.genre = genre
		self.isbn = isbn 
		self.publisher = publisher 
		self.copies = copies
		
		self.title(self.form_title)
		self.geometry("500x500")
		self.resizable(False, False)
		
		container = Frame(self)
		container.grid(row=0, column=1, padx=10, pady=10)
		
		self.title_label = Label(container, text=self.form_title, font=(None, 18, "bold"))
		self.title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

		self.book_title_label = Label(container, text="Título:")
		self.book_title_label.grid(row=1, column=0, pady=10)

		self.book_title_entry = Entry(container)
		self.book_title_entry.insert(0, self.book_title)
		self.book_title_entry.grid(row=1, column=1, pady=10)
		
		self.first_name_author_label = Label(container, text="Nombre del autor:")
		self.first_name_author_label.grid(row=2, column=0, pady=10)

		self.first_name_author_entry = Entry(container)
		self.first_name_author_entry.insert(0, self.author_firstname)
		self.first_name_author_entry.grid(row=2, column=1, pady=10)
		
		self.last_name_author_label = Label(container, text="Apellido del autor:")
		self.last_name_author_label.grid(row=3, column=0, pady=10)

		self.last_name_author_entry = Entry(container)
		self.last_name_author_entry.insert(0, self.author_lastname)
		self.last_name_author_entry.grid(row=3, column=1, pady=10)

		self.genre_label = Label(container, text="Género:")
		self.genre_label.grid(row=4, column=0, pady=10)
		
		self.selected_genre = StringVar(value=self.genre)
		
		self.genre_selector = ttk.Combobox(container, textvariable=self.selected_genre, values=genre_controller.list_genres(), state="readonly")
		self.genre_selector.grid(row=4, column=1, pady=10)

		self.isbn_label = Label(container, text="ISBN:")
		self.isbn_label.grid(row=5, column=0, pady=10)
		
		self.isbn_entry = Entry(container)
		self.isbn_entry.insert(0, self.isbn)
		self.isbn_entry.grid(row=5, column=1, pady=10)

		self.publisher_label = Label(container, text="Editorial:")
		self.publisher_label.grid(row=6, column=0, pady=10)
		
		self.publisher_entry = Entry(container)
		self.publisher_entry.insert(0, self.publisher)
		self.publisher_entry.grid(row=6, column=1, pady=10)
		
		self.copies_label = Label(container, text="Número de copias:")
		self.copies_label.grid(row=7, column=0, pady=10)
		
		self.copies_entry = Entry(container)
		self.copies_entry.insert(0, self.copies)
		self.copies_entry.grid(row=7, column=1, pady=10)
				
		if type_form == "new_book_form":
			self.add_new_book_button = Button(container, text="Agregar libro", command = lambda : self.add_new_book(self.book_title_entry.get(), [(self.first_name_author_entry.get(), self.last_name_author_entry.get())], self.selected_genre.get(), self.isbn_entry.get(), self.publisher_entry.get(),
			int(self.copies_entry.get()), 1))
			self.add_new_book_button.grid(row=8, column=0, columnspan=2, pady=20)

		if type_form == "edit_book_form":
			self.edit_book_buttton = Button(container, text="Editar libro", command = lambda : self.update_book(self.book_id, self.book_title_entry.get(), [(self.first_name_author_entry.get(), self.last_name_author_entry.get())], self.selected_genre.get(), self.isbn_entry.get(), self.publisher_entry.get(),
			int(self.copies_entry.get()), 1))
			self.edit_book_buttton.grid(row=8, column=0, columnspan=2, pady=20)

		self.grid_rowconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(2, weight=1)
				
	def add_new_book(self, title, authors, genre, isbn, publisher, copies, user_id):
		
		result = book_controller.add_book(title, authors, genre, isbn, publisher, copies, user_id)
				
		if result["estado"] == "ok":
			messagebox.showinfo("Exito", result["mensaje"])
			self.destroy()
		else:
			messagebox.showerror("Error", result["mensaje"])
	
	def update_book(self, book_id, title, authors, genre, isbn, publisher, new_copies_number, user_id):
				
		result = book_controller.update_book(book_id, title, authors, genre, isbn, publisher, new_copies_number, user_id)
				
		if result["estado"] == "ok":
			messagebox.showinfo("Exito", result["mensaje"])
			self.destroy()
		else:
			messagebox.showerror("Error", result["mensaje"])