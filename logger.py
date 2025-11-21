import sqlite3
import plotly.graph_objects as go
from tkinter import *
from tkinter import ttk,messagebox

class Logger:
	def __init__(self,root):
		self.root = root
		self.root.title("Logger")
		self.root.geometry("400x400")
		self.root.config(bg="#c0c0c0")
		#~ self.root.config(bg="#d2691e")
		self.conn = sqlite3.connect("logger.db")
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS log(
		matric TEXT,
		price INTEGER
		)""")
		self.root.resizable(width="false",height="false")
		try:
			self.root.iconbitmap("pics/my_nick_name.ico")
		except:
			pass
		self.front_title()

	def front_title(self):
		#~ this is for the title box
		self.frame1 = Frame(root, bg="#a52a2a")
		self.frame1.grid(row=0, column=0, columnspan=100, padx=140, pady=5)
		self.title_box = Label(self.frame1, text="LOGGER",bg="#a52a2a", font=("Arial", 21, "bold"))
		self.title_box.grid(row=0, column=0, pady=10)
		self.student_details()

	def student_details(self):
		#~ this handles student's details
		self.matric_num_label = Label(self.root, text="Matric no", font=("Arial", 20, "bold"))
		self.matric_num_label.grid(row=1, column=0, padx=(5,0), pady=15)
		self.matric_num_entry = Entry(self.root)
		self.matric_num_entry.grid(row=1, column=1, padx=(10,0))
		self.price_label = Label(self.root, text="price", font=("Arial", 20, "bold"))
		self.price_label.grid(row=2, column=0, pady=10)
		self.price_entry = Entry(self.root)
		self.price_entry.grid(row=2, column=1)
		self.log_btn = Button(self.root, text="LOG", font=("Arial", 10, "bold"),command=self.log_details)
		self.log_btn.grid(row=3, column=1)
		self.log_history_label = Button(self.root, text="Show log history", font=("Arial", 9, "bold"),command=self.log_history)
		self.log_history_label.grid(row=4, column=1, pady=20)

	def log_details(self):
		#~ this handles and check if the details are valid or not before adding it to the database
		try:
			self.mat_get = self.matric_num_entry.get()
			self.price_get = int(self.price_entry.get())
			if self.mat_get and self.price_get:			
				self.matric_num_entry.delete(0,END)
				self.price_entry.delete(0,END)
				self.c.execute("INSERT INTO log VALUES(:matric,:price)",
				{
				"matric" : self.mat_get,
				"price" : self.price_get
				})
				self.conn.commit()
				messagebox.showinfo("Info","Log successful")
			
		except:
			messagebox.showerror("info","An error occured check your values and try again!")

	def log_history(self):
		#~ handles the display of log history
		self.root = Tk()
		self.root.title("Logger history")
		self.root.geometry("300x400")
		self.c.execute("SELECT rowid,* FROM log")
		self.items = self.c.fetchall()
		self.print_log=""
		try:
			self.root.iconbitmap("pics/my_nick_name.ico")
		except:
			pass
	
		
		self.history_label = Label(self.root, text="Logger History", font=("Arial", 12, "bold"), bg="#d2691e")
		self.history_label.grid(row=0, column=0, padx=(90,0), pady=20)
		for self.print_log in self.items:
			self.mat_num = self.print_log[1].strip()
			self.prc = self.print_log[2]
			self.ids = self.print_log[0]
			self.text_label = Label(self.root, text=f"{self.ids}. {self.mat_num} spent #{self.prc}")
			self.text_label.grid()

if __name__ == "__main__":
	root = Tk()
	App = Logger(root)
	root.mainloop()
