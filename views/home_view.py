from tkinter import *
from views.base_view import BaseView

class HomeFrame(BaseView):
	
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		
		access = [("Buscador", "images/search.png"), ("Gestión de Libros", "images/book.png"), ("Alta y baja de Socios", "images/member.png"), ("Préstamos y Devoluciones", "images/borrow.png")]
		
		self.images = []
		
		for i, (text, path) in enumerate(access):
			try:
				img = PhotoImage(file=path)
			except:
				img = None
		
			self.images.append(img)
			
			btn = Button(self.main_area, text=text, image=img, compound="top", bg="white", font=(None, 10, "bold"), width=150, height=200, wraplength=100)
			
			btn.grid(row=0, column=i, padx=10, pady=20, sticky="nsew")
			
			#self.main_area.grid_columnconfigure(i, weight=1)
		
		
		
		#self.search_image = PhotoImage(file="images/search.png")
		#self.book_image = PhotoImage(file="images/book.png")
		#self.member_image = PhotoImage(file="images/member.png")
		#self.loan_image = PhotoImage(file="images/borrow.png")

		#search_button = Button(self.main_area, image=self.search_image, text="Buscador", font=(None, 10, "bold"), compound="top", width=150, height=150, wraplength=90, bg="white")
		#search_button.pack(padx=10, side=LEFT)
		
		#book_management_button = Button(self.main_area, image=self.book_image, text="Gestión de Libros", font=(None, 10, "bold"), compound="top", width=150, height=150, wraplength=90, bg="white")
		#book_management_button.pack(padx=10, side=LEFT)
		
		#member_management_button = Button(self.main_area, image=self.member_image, text="Alta y baja de Socios", font=(None, 10, "bold"), compound="top", width=150, height=150, wraplength=90, bg="white")
		#member_management_button.pack(padx=10, side=LEFT)
		
		#loan_button = Button(self.main_area, image=self.loan_image, text="Préstamos y Devoluciones", font=(None, 10, "bold"), compound="top", width=150, height=150, wraplength=100, bg="white")
		#loan_button.pack(padx=10, side=LEFT)
		
		
		
	