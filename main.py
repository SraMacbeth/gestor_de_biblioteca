from tkinter import *
from models import db
from views.login_view import LoginFrame
from views.reset_password_view import ResetPasswordFrame
from views.register_view import RegisterFrame
from views.home_view import HomeFrame
from views.search_view import SearchFrame
from views.books_view import BooksFrame
from views.members_view import MembersFrame
from views.loan_view import LoanFrame

class App(Tk):
	
	"""
	Clase principal de aplicación.
	Administra la ventana raíz y la navegación entre vistas(frames), utilizando un sistema centralizado para mostrar y actualizar frames.
	También puede mantener el estado global del usuario autenticado.
	Hereda de Tk: ventana principal de Tkinter.
	"""
	
	def __init__(self):
		super().__init__()
		self.title("BiblioApp")
		self.resizable(False, False)
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		self.actual_user = None
		
		public_views = (LoginFrame, ResetPasswordFrame, RegisterFrame)
			
		for F in public_views:
			name = F.__name__
			frame = F(parent=self, controller=self)
			frame.grid(row=0, column=0, sticky="nsew")
			self.frames[name] = frame
		
		self.show_frame("LoginFrame")
			
	def load_private_views(self):
		
		private_views = (HomeFrame, SearchFrame, BooksFrame, MembersFrame, LoanFrame)
		
		for F in private_views:
			name = F.__name__
			frame = F(parent=self, controller=self, user=self.actual_user)
			frame.grid(row=0, column=0, sticky="nsew")
			self.frames[name] = frame
		
	def show_frame(self, name, data=None):
		frame = self.frames[name] 
		if data and hasattr(frame, "update_data"):
			frame.update_data(data)
		frame.tkraise()

if __name__ == "__main__":
	db.setup_database()
	app = App()
	app.mainloop()