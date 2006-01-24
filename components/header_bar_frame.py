from tkinter import *

class HeaderBar(Frame):
	
	"""
	Barra superior que muestra el nombre del usuario actual y un botón de logout.
	Args:
	parent(Tk.Widget): El widget padre.
	logout_callback(function): Función que se ejecuta al presionar el botón de cerrar sesión.	
	"""
	
	def __init__(self, parent, logout_callback):
		super().__init__(parent)
		self.logout_callback = logout_callback

		self.username_label = Label(self, text="")
		self.username_label.pack(padx=10, side=LEFT)
		
		logout_button = Button(self, text="Cerrar sesión", command = self.logout_callback)
		logout_button.pack(padx=10, side=LEFT)
		
	def set_username(self, username):
		self.username_label.config(text=f"Usuario conectado: {username}")