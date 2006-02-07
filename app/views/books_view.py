from tkinter import *
from views.base_view import BaseView
from components.search_bar_frame import SearchBar


class BooksView(BaseView):
	
	def __init__(self, parent, controller, user=None):
		super().__init__(parent, controller)
		self.controller = controller
		self.user = user
		
		self.search_bar = SearchBar(self.main_area, search_callback=self.search, search_type='book', show_entity_selection=False)
		self.search_bar.grid(row=0, column=0, sticky="w")
		
		text_label_updated = self.search_bar.set_text_label("Ingrese el ID del libro que desea buscar:")

		self.text_search_label = Label(self.main_area, text="")
		self.text_search_label .grid(row=1, column=0, pady=10, sticky="w")
		
		self.result_label = Label(self.main_area, text="")
		self.result_label.grid(row=2, column=0, pady=10, sticky="w")
		
		self.grid_rowconfigure(1, weight=1)
	
	def search(self):
		
		search_text = self.search_bar.get_search_text()
		self.text_search_label.config(text=f"Resultado encontrado para la búsqueda: {search_text}")

		search_entity = self.search_bar.get_search_entity()
		
		print("Buscando...")
		
		