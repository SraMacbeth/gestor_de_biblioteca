from tkinter import *
from views.base_view import BaseView

class HomeFrame(BaseView):
	
	def __init__(self, parent, controller, user=None):
		super().__init__(parent, controller)
		self.controller = controller
		self.user = user
		
		self.header.return_home_button.grid_remove()
				
		access = [("Buscador", "images/search.png", "SearchFrame"), ("Gestión de Libros", "images/book.png", "BooksFrame"), ("Alta y baja de Socios", "images/member.png", "MembersFrame"), ("Préstamos y Devoluciones", "images/borrow.png", "LoanFrame")]
		
		self.images = []
		
		for i, (text, path, next_view) in enumerate(access):
			try:
				img = PhotoImage(file=path)
			except:
				img = None
		
			self.images.append(img)
			
			btn = Button(self.main_area, text=text, image=img, compound="top", bg="white", font=(None, 10, "bold"), width=150, height=200, wraplength=100, command = lambda value = next_view : self.on_btn_click(value))
			
			btn.grid(row=0, column=i, padx=10, pady=20, sticky="nsew")
			
	def on_btn_click(self, value):
		self.controller.show_frame(value, data={"username": self.user})

	