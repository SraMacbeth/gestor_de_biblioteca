from tkinter import *
from models import db
from views.login_view import LoginFrame
from views.reset_password_view import ResetPasswordFrame
from views.register_view import RegisterFrame
from views.home_view import HomeFrame

class App(Tk):
	
	def __init__(self):
		super().__init__()
		self.title("BiblioApp")
		self.geometry("1024x768")
		
		self.frames = {}

		for F in (LoginFrame, ResetPasswordFrame, RegisterFrame, HomeFrame):
			nombre = F.__name__
			frame = F(parent=self, controller=self)
			frame.grid(row=0, column=0, sticky="nsew")
			self.frames[nombre] = frame
		self.show_frame("LoginFrame")
	
	def show_frame(self, nombre):
		frame = self.frames[nombre] 
		frame.tkraise()

if __name__ == "__main__":
	db.setup_database()
	app = App()
	app.mainloop()