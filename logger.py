import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from data_handler import DataHandler


class Logger:
    def __init__(self, root):
        self.root = root
        self.root.title("Logger")
        self.root.geometry("400x500")
        self.root.config(bg="#c0c0c0")

        self.data_handler = DataHandler()

        self.conn = sqlite3.connect("logger.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS log(
            matric TEXT,
            name TEXT,
            bank TEXT,
            price INTEGER,
            timestamp TEXT,
            flags TEXT
        )""")
        self.root.resizable(width="false", height="false")
        try:
            self.root.iconbitmap("pics/my_nick_name.ico")
        except:
            pass
        self.front_title()

    def front_title(self):
        self.frame1 = Frame(self.root, bg="#a52a2a")
        self.frame1.grid(row=0, column=0, columnspan=100, padx=140, pady=5)
        self.title_box = Label(
            self.frame1, text="LOGGER", bg="#a52a2a", font=("Arial", 21, "bold")
        )
        self.title_box.grid(row=0, column=0, pady=10)
        self.student_details()

    def student_details(self):
        # Matric number
        self.matric_num_label = Label(
            self.root, text="Matric no", font=("Arial", 20, "bold")
        )
        self.matric_num_label.grid(row=1, column=0, padx=(5, 0), pady=15)
        self.matric_num_entry = Entry(self.root)
        self.matric_num_entry.grid(row=1, column=1, padx=(10, 0))

        # Student name display (shows after validation)
        self.name_display = Label(self.root, text="", font=("Arial", 12), fg="green")
        self.name_display.grid(row=1, column=2, padx=5)

        # Validate button
        self.validate_btn = Button(
            self.root,
            text="Validate",
            font=("Arial", 10, "bold"),
            command=self.validate_student,
        )
        self.validate_btn.grid(row=1, column=3, padx=5)

        # Bank dropdown
        self.bank_label = Label(self.root, text="Bank", font=("Arial", 20, "bold"))
        self.bank_label.grid(row=2, column=0, pady=10)
        self.bank_var = StringVar()
        self.bank_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.bank_var,
            values=self.data_handler.valid_banks,
            state="readonly",
            width=18,
        )
        self.bank_dropdown.grid(row=2, column=1)

        # Price
        self.price_label = Label(self.root, text="Price", font=("Arial", 20, "bold"))
        self.price_label.grid(row=3, column=0, pady=10)
        self.price_entry = Entry(self.root)
        self.price_entry.grid(row=3, column=1)

        # Log button
        self.log_btn = Button(
            self.root,
            text="LOG",
            font=("Arial", 10, "bold"),
            command=self.log_details,
            state=DISABLED,
        )
        self.log_btn.grid(row=4, column=1)

        # History button
        self.log_history_label = Button(
            self.root,
            text="Show log history",
            font=("Arial", 9, "bold"),
            command=self.log_history,
        )
        self.log_history_label.grid(row=5, column=1, pady=20)

        # Variable to store validated student info
        self.validated_student = None

    def validate_student(self):
        """Validate student matric before allowing purchase"""
        matric = self.matric_num_entry.get().strip()

        if not matric:
            messagebox.showerror("Error", "Please enter matric number")
            return

        # Validate matric exists
        is_valid, name, department = self.data_handler.validate_matric(matric)

        if is_valid:
            self.name_display.config(text=f"✓ {name}", fg="green")
            self.validated_student = {
                "matric": matric,
                "name": name,
                "department": department,
            }
            self.log_btn.config(state=NORMAL)
            messagebox.showinfo("Success", f"Student validated: {name}\n{department}")
        else:
            self.name_display.config(text="✗ Invalid", fg="red")
            self.validated_student = None
            self.log_btn.config(state=DISABLED)
            messagebox.showerror("Error", "Matric number not found in database!")

    def log_details(self):
        """Log transaction with full validation"""
        try:
            # Check if student was validated
            if not self.validated_student:
                messagebox.showerror("Error", "Please validate student matric first!")
                return

            matric = self.validated_student["matric"]
            name = self.validated_student["name"]

            # Get and validate bank
            bank = self.bank_var.get()
            if not bank:
                messagebox.showerror("Error", "Please select a bank!")
                return

            is_valid_bank, error_msg = self.data_handler.validate_bank(bank)
            if not is_valid_bank:
                messagebox.showerror("Error", error_msg)
                return

            # Get and validate price
            price_input = self.price_entry.get()
            is_valid_price, price, error_msg = self.data_handler.validate_price(
                price_input
            )
            if not is_valid_price:
                messagebox.showerror("Error", error_msg)
                return

            # Check time window
            is_valid_time, error_msg = self.data_handler.check_time_window()
            if not is_valid_time:
                result = messagebox.askyesno(
                    "Warning", f"{error_msg}\nDo you want to continue anyway?"
                )
                if not result:
                    return

            # Check for rapid purchases
            is_rapid, warning_msg = self.data_handler.check_duplicate_recent(matric)
            if is_rapid:
                result = messagebox.askyesno(
                    "Warning", f"{warning_msg}\nDo you want to continue?"
                )
                if not result:
                    return

            # Check daily limit
            at_limit, warning_msg = self.data_handler.check_daily_limit(matric)
            if at_limit:
                result = messagebox.askyesno(
                    "Warning", f"{warning_msg}\nDo you want to continue?"
                )
                if not result:
                    return

            # Generate flags
            flags = self.data_handler.generate_flags(matric, price)

            # Get timestamp
            timestamp = self.data_handler.get_timestamp()

            # Insert into database
            self.c.execute(
                """INSERT INTO log VALUES(:matric, :name, :bank, :price, :timestamp, :flags)""",
                {
                    "matric": matric,
                    "name": name,
                    "bank": bank,
                    "price": price,
                    "timestamp": timestamp,
                    "flags": flags,
                },
            )
            self.conn.commit()

            # Clear form
            self.matric_num_entry.delete(0, END)
            self.bank_var.set("")
            self.price_entry.delete(0, END)
            self.name_display.config(text="")
            self.validated_student = None
            self.log_btn.config(state=DISABLED)

            # Success message
            flag_msg = f"\nFlags: {flags}" if flags else ""
            messagebox.showinfo("Success", f"Log successful!{flag_msg}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def log_history(self):
        """Display log history"""
        history_window = Tk()
        history_window.title("Logger history")
        history_window.geometry("600x400")
        try:
            history_window.iconbitmap("pics/my_nick_name.ico")
        except:
            pass

        self.c.execute("SELECT rowid, * FROM log")
        items = self.c.fetchall()

        history_label = Label(
            history_window,
            text="Logger History",
            font=("Arial", 12, "bold"),
            bg="#d2691e",
        )
        history_label.grid(row=0, column=0, padx=(200, 0), pady=20)

        for idx, record in enumerate(items, start=1):
            row_id = record[0]
            matric = record[1]
            name = record[2]
            bank = record[3]
            price = record[4]
            timestamp = record[5]
            flags = record[6]

            text = f"{row_id}. {matric} - {name} | {bank} | ₦{price}"
            if flags:
                text += f" | ⚠️ {flags}"

            text_label = Label(history_window, text=text, font=("Arial", 10))
            text_label.grid(row=idx, column=0, sticky=W, padx=10)


if __name__ == "__main__":
    root = Tk()
    App = Logger(root)
    root.mainloop()
