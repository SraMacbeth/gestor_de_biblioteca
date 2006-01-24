from tkinter import *
from components.header_bar_frame import HeaderBar

class BaseView(Frame):
	
	"""
	Clase base para todas las vistas que requieren mostrar HeaderBar con nombre de usuario y botón de logout.
	"""
	
	def __init__(self, parent):
		super().__init__(parent)
		
		self.header = HeaderBar(self, logout_callback=self.logout)
		self.header.pack(fill="x", pady=10)
		
		self.main_area = Frame(self)
		self.main_area.pack(expand=True ,fill="both")
	
	def update_data(self, data):
		username = data.get("username", "")
		self.header.set_username(username)
		
	def logout(self):
		self.actual_user = None
		self.controller.show_frame("LoginFrame")