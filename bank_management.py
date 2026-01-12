import os
from datetime import date
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# Ensure directories exist
os.makedirs("./database/Admin", exist_ok=True)
os.makedirs("./database/Customer", exist_ok=True)
os.makedirs("./images", exist_ok=True)

# Backend python functions code starts :
def is_valid(customer_account_number):
    db_path = "./database/Customer/customerDatabase.txt"
    if not os.path.exists(db_path):
        with open(db_path, "w") as f:
            pass
        return True
    
    if check_credentials(customer_account_number, "DO_NOT_CHECK", 2, True):
        return False
    else:
        return True

def check_leap(year):
    return ((int(year) % 4 == 0) and (int(year) % 100 != 0)) or (int(year) % 400 == 0)

def check_date(date_str):
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_in_months_in_leap_year = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if date_str == "":
        return False

    try:
        date_elements = date_str.split("/")
        if len(date_elements) != 3:
            return False
        day = int(date_elements[0])
        month = int(date_elements[1])
        year = int(date_elements[2])

        if (year > 2026 or year < 1900) or (month > 12 or month < 1):
            return False
        else:
            if check_leap(year):
                num_of_days = days_in_months_in_leap_year[month - 1]
            else:
                num_of_days = days_in_months[month - 1]

            return 1 <= day <= num_of_days
    except (ValueError, IndexError):
        return False

def is_valid_mobile(mobile_number):
    return len(mobile_number) == 10 and mobile_number.isnumeric()

def append_data(database_path, data):
    with open(database_path, "a") as f:
        f.write(data)

def display_account_summary(identity, choice):
    db_path = "./database/Customer/customerDatabase.txt"
    if not os.path.exists(db_path):
        return "Database not found."
    
    output_message = ""
    found = False
    with open(db_path, "r") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if lines[i].strip() == str(identity):
                found = True
                if choice == 1:
                    output_message += f"Account number : {lines[i].strip()}\n"
                    output_message += f"Current balance : {lines[i+2].strip()}\n"
                    output_message += f"Date of account creation : {lines[i+3].strip()}\n"
                    output_message += f"Name of account holder : {lines[i+4].strip()}\n"
                    output_message += f"Type of account : {lines[i+5].strip()}\n"
                    output_message += f"Date of Birth : {lines[i+6].strip()}\n"
                    output_message += f"Mobile number : {lines[i+7].strip()}\n"
                    output_message += f"Gender : {lines[i+8].strip()}\n"
                    output_message += f"Nationality : {lines[i+9].strip()}\n"
                    output_message += f"KYC : {lines[i+10].strip()}\n"
                else:
                    output_message += f"Current balance : {lines[i+2].strip()}\n"
                break
            i += 12
    
    if not found:
        return "Account not found."
    return output_message

def delete_customer_account(identity, choice):
    db_path = "./database/Customer/customerDatabase.txt"
    if not os.path.exists(db_path):
        return
    
    new_data = []
    found = False
    with open(db_path, "r") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if lines[i].strip() == str(identity):
                found = True
                i += 12
            else:
                new_data.extend(lines[i:i+12])
                i += 12
                
    with open(db_path, "w") as f:
        f.writelines(new_data)
    
    msg = f"Account {identity} closed successfully!" if found else "Account not found!"
    if choice == 1:
        adminMenu.printMessage_outside(msg)
    print(msg)

def create_admin_account(identity, password):
    db_path = "./database/Admin/adminDatabase.txt"
    append_data(db_path, f"{identity}\n{password}\n*\n")
    msg = "Admin account created successfully!"
    adminMenu.printMessage_outside(msg)
    print(msg)

def delete_admin_account(identity):
    db_path = "./database/Admin/adminDatabase.txt"
    if not os.path.exists(db_path):
        return
    
    new_data = []
    found = False
    with open(db_path, "r") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if lines[i].strip() == str(identity):
                found = True
                i += 3
            else:
                new_data.extend(lines[i:i+3])
                i += 3
                
    with open(db_path, "w") as f:
        f.writelines(new_data)
    
    msg = f"Admin {identity} deleted!" if found else "Admin not found!"
    adminMenu.printMessage_outside(msg)
    print(msg)

def change_PIN(identity, new_PIN):
    db_path = "./database/Customer/customerDatabase.txt"
    lines = []
    with open(db_path, "r") as f:
        lines = f.readlines()
    
    for i in range(0, len(lines), 12):
        if lines[i].strip() == str(identity):
            lines[i+1] = str(new_PIN) + "\n"
            break
            
    with open(db_path, "w") as f:
        f.writelines(lines)
    
    msg = "PIN changed successfully."
    customerMenu.printMessage_outside(msg)

def transaction(identity, amount, choice):
    db_path = "./database/Customer/customerDatabase.txt"
    lines = []
    with open(db_path, "r") as f:
        lines = f.readlines()
    
    balance = 0
    found = False
    for i in range(0, len(lines), 12):
        if lines[i].strip() == str(identity):
            found = True
            balance = float(lines[i+2].strip())
            if choice == 2 and balance - amount < 10000:
                return -1
            
            if choice == 1:
                balance += amount
            else:
                balance -= amount
            
            lines[i+2] = str(balance) + "\n"
            break
            
    if found:
        with open(db_path, "w") as f:
            f.writelines(lines)
        return balance
    return None

def check_credentials(identity, password, choice, admin_access):
    folder = "./database/Admin" if choice == 1 else "./database/Customer"
    file = "/adminDatabase.txt" if choice == 1 else "/customerDatabase.txt"
    path = folder + file
    
    if not os.path.exists(path):
        if choice == 1:
            with open(path, "w") as f:
                f.write("admin\nadmin@123\n*\n")
        else:
            with open(path, "w") as f:
                pass
            return False

    with open(path, "r") as f:
        lines = f.readlines()
        step = 3 if choice == 1 else 12
        for i in range(0, len(lines), step):
            if lines[i].strip() == str(identity):
                stored_pass = lines[i+1].strip()
                if (password == "DO_NOT_CHECK_ADMIN" and choice == 1 and not admin_access) or \
                   (password == "DO_NOT_CHECK" and choice == 2 and admin_access) or \
                   (stored_pass == str(password)):
                    return True
    return False

# GUI Classes
class welcomeScreen:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.title("Welcome to Banking System")
        window.resizable(0, 0)
        
        self.canvas = Canvas(window, bg="#ffffff", height=494, width=743)
        self.canvas.place(x=0, y=0)
        
        try:
            self.bg_img = PhotoImage(file="./images/bank1.png")
            self.canvas.create_image(371, 247, image=self.bg_img)
        except:
            pass
            
        self.label = Label(window, text="Welcome to Our Bank", font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#00254a")
        self.label.place(relx=0.5, rely=0.2, anchor=CENTER)
        
        self.admin_btn = Button(window, text="Admin Login", command=self.admin_login, width=20, bg="#00254a", fg="white", font=("Segoe UI", 12))
        self.admin_btn.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.cust_btn = Button(window, text="Customer Login", command=self.customer_login, width=20, bg="#00254a", fg="white", font=("Segoe UI", 12))
        self.cust_btn.place(relx=0.5, rely=0.6, anchor=CENTER)

    def admin_login(self):
        self.master.withdraw()
        adminLogin(Toplevel(self.master))

    def customer_login(self):
        self.master.withdraw()
        customerLogin(Toplevel(self.master))

class adminLogin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.title("Admin Login")
        window.resizable(0, 0)
        
        self.canvas = Canvas(window, bg="#ffffff", height=494, width=743)
        self.canvas.place(x=0, y=0)
        
        try:
            self.img = PhotoImage(file="./images/adminLogin1.png")
            self.canvas.create_image(150, 247, image=self.img)
        except:
            pass
            
        Label(window, text="Admin ID:", bg="#ffffff").place(x=350, y=180)
        self.id_entry = Entry(window)
        self.id_entry.place(x=450, y=180)
        
        Label(window, text="Password:", bg="#ffffff").place(x=350, y=220)
        self.pass_entry = Entry(window, show="*")
        self.pass_entry.place(x=450, y=220)
        
        Button(window, text="Login", command=self.login, bg="#00254a", fg="white").place(x=450, y=270)
        Button(window, text="Back", command=self.back, bg="#00254a", fg="white").place(x=520, y=270)

    def login(self):
        if check_credentials(self.id_entry.get(), self.pass_entry.get(), 1, False):
            self.master.withdraw()
            adminMenu(Toplevel(self.master))
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

class customerLogin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.title("Customer Login")
        window.resizable(0, 0)
        
        self.canvas = Canvas(window, bg="#ffffff", height=494, width=743)
        self.canvas.place(x=0, y=0)
        
        try:
            self.img = PhotoImage(file="./images/customer.png")
            self.canvas.create_image(150, 247, image=self.img)
        except:
            pass
            
        Label(window, text="Account No:", bg="#ffffff").place(x=350, y=180)
        self.acc_entry = Entry(window)
        self.acc_entry.place(x=450, y=180)
        
        Label(window, text="PIN:", bg="#ffffff").place(x=350, y=220)
        self.pin_entry = Entry(window, show="*")
        self.pin_entry.place(x=450, y=220)
        
        Button(window, text="Login", command=self.login, bg="#00254a", fg="white").place(x=450, y=270)
        Button(window, text="Back", command=self.back, bg="#00254a", fg="white").place(x=520, y=270)

    def login(self):
        if check_credentials(self.acc_entry.get(), self.pin_entry.get(), 2, False):
            global customer_accNO
            customer_accNO = self.acc_entry.get()
            self.master.withdraw()
            customerMenu(Toplevel(self.master))
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

class adminMenu:
    _frame = None
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.title("Admin Menu")
        window.resizable(0, 0)
        window.configure(bg="#f0f0f0")
        
        Label(window, text="Admin Dashboard", font=("Segoe UI", 18, "bold"), bg="#f0f0f0").pack(pady=10)
        
        btn_frame = Frame(window, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        Button(btn_frame, text="Create Customer", command=self.create_cust, width=20).grid(row=0, column=0, padx=5, pady=5)
        Button(btn_frame, text="Close Customer", command=self.close_cust, width=20).grid(row=0, column=1, padx=5, pady=5)
        Button(btn_frame, text="Create Admin", command=self.create_adm, width=20).grid(row=1, column=0, padx=5, pady=5)
        Button(btn_frame, text="Delete Admin", command=self.delete_adm, width=20).grid(row=1, column=1, padx=5, pady=5)
        Button(btn_frame, text="Account Summary", command=self.summary, width=20).grid(row=2, column=0, padx=5, pady=5)
        Button(btn_frame, text="Logout", command=self.logout, width=20).grid(row=2, column=1, padx=5, pady=5)
        
        adminMenu._frame = Frame(window, bg="white", relief="sunken", borderwidth=2)
        adminMenu._frame.pack(fill="both", expand=True, padx=20, pady=20)

    def create_cust(self): createCustomerAccount(Toplevel(self.master))
    def close_cust(self): CloseAccountByAdmin(Toplevel(self.master))
    def create_adm(self): createAdmin(Toplevel(self.master))
    def delete_adm(self): deleteAdmin(Toplevel(self.master))
    def summary(self): checkAccountSummary(Toplevel(self.master))
    def logout(self):
        self.master.withdraw()
        adminLogin(Toplevel(self.master))

    @staticmethod
    def printMessage_outside(msg):
        if adminMenu._frame:
            for widget in adminMenu._frame.winfo_children(): widget.destroy()
            Label(adminMenu._frame, text=msg, bg="white", font=("Segoe UI", 12)).pack(pady=20)

class customerMenu:
    _frame = None
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.title("Customer Menu")
        window.resizable(0, 0)
        
        Label(window, text=f"Welcome, Account {customer_accNO}", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        btn_frame = Frame(window)
        btn_frame.pack(pady=10)
        
        Button(btn_frame, text="Deposit", command=self.deposit, width=15).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="Withdraw", command=self.withdraw, width=15).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="Balance", command=self.balance, width=15).grid(row=0, column=2, padx=5)
        Button(btn_frame, text="Change PIN", command=self.change_pin, width=15).grid(row=1, column=0, padx=5, pady=5)
        Button(btn_frame, text="Summary", command=self.summary, width=15).grid(row=1, column=1, padx=5, pady=5)
        Button(btn_frame, text="Logout", command=self.logout, width=15).grid(row=1, column=2, padx=5, pady=5)
        
        customerMenu._frame = Frame(window, bg="white", relief="sunken", borderwidth=2)
        customerMenu._frame.pack(fill="both", expand=True, padx=20, pady=20)

    def deposit(self): Deposit(Toplevel(self.master))
    def withdraw(self): Withdraw(Toplevel(self.master))
    def balance(self): customerMenu.printMessage_outside(display_account_summary(customer_accNO, 2))
    def change_pin(self): ChangePIN(Toplevel(self.master))
    def summary(self): customerMenu.printMessage_outside(display_account_summary(customer_accNO, 1))
    def logout(self):
        self.master.withdraw()
        customerLogin(Toplevel(self.master))

    @staticmethod
    def printMessage_outside(msg):
        if customerMenu._frame:
            for widget in customerMenu._frame.winfo_children(): widget.destroy()
            Label(customerMenu._frame, text=msg, bg="white", font=("Segoe UI", 10), justify=LEFT).pack(pady=10)

class createCustomerAccount:
    def __init__(self, window=None):
        self.master = window
        window.geometry("400x500")
        window.title("Create Customer Account")
        
        fields = ["Account No", "PIN", "Initial Balance", "Name", "Account Type", "DOB (DD/MM/YYYY)", "Mobile", "Gender", "Nationality", "KYC"]
        self.entries = {}
        for i, field in enumerate(fields):
            Label(window, text=field).grid(row=i, column=0, padx=10, pady=5)
            e = Entry(window)
            e.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = e
            
        Button(window, text="Create", command=self.create).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def create(self):
        acc = self.entries["Account No"].get()
        if not is_valid(acc):
            messagebox.showerror("Error", "Account already exists!")
            return
        
        data = ""
        for field in ["Account No", "PIN", "Initial Balance"]:
            data += self.entries[field].get() + "\n"
        data += str(date.today()) + "\n"
        for field in ["Name", "Account Type", "DOB (DD/MM/YYYY)", "Mobile", "Gender", "Nationality", "KYC"]:
            data += self.entries[field].get() + "\n"
            
        append_data("./database/Customer/customerDatabase.txt", data)
        messagebox.showinfo("Success", "Account Created!")
        self.master.destroy()

class CloseAccountByAdmin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("300x150")
        Label(window, text="Enter Account No:").pack(pady=10)
        self.e = Entry(window)
        self.e.pack()
        Button(window, text="Close Account", command=self.close).pack(pady=10)
    def close(self):
        delete_customer_account(self.e.get(), 1)
        self.master.destroy()

class createAdmin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("300x200")
        Label(window, text="Admin ID:").pack()
        self.id = Entry(window); self.id.pack()
        Label(window, text="Password:").pack()
        self.pw = Entry(window, show="*"); self.pw.pack()
        Button(window, text="Create", command=self.create).pack(pady=10)
    def create(self):
        create_admin_account(self.id.get(), self.pw.get())
        self.master.destroy()

class deleteAdmin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("300x150")
        Label(window, text="Admin ID:").pack()
        self.id = Entry(window); self.id.pack()
        Button(window, text="Delete", command=self.delete).pack(pady=10)
    def delete(self):
        delete_admin_account(self.id.get())
        self.master.destroy()

class checkAccountSummary:
    def __init__(self, window=None):
        self.master = window
        window.geometry("300x150")
        Label(window, text="Account No:").pack()
        self.acc = Entry(window); self.acc.pack()
        Button(window, text="Show", command=self.show).pack(pady=10)
    def show(self):
        res = display_account_summary(self.acc.get(), 1)
        adminMenu.printMessage_outside(res)
        self.master.destroy()

class Deposit:
    def __init__(self, window=None):
        self.master = window
        window.geometry("300x150")
        Label(window, text="Amount:").pack()
        self.amt = Entry(window); self.amt.pack()
        Button(window, text="Deposit", command=self.do).pack(pady=10)
    def do(self):
        res = transaction(customer_accNO, float(self.amt.get()), 1)
        customerMenu.printMessage_outside(f"Deposited! New Balance: {res}")
        self.master.destroy()

class Withdraw:
    def __init__(self, window=None):
        self.master = window
        window.geometry("300x150")
        Label(window, text="Amount:").pack()
        self.amt = Entry(window); self.amt.pack()
        Button(window, text="Withdraw", command=self.do).pack(pady=10)
    def do(self):
        res = transaction(customer_accNO, float(self.amt.get()), 2)
        if res == -1:
            messagebox.showerror("Error", "Insufficient Balance (Min 10000)")
        else:
            customerMenu.printMessage_outside(f"Withdrawn! New Balance: {res}")
        self.master.destroy()

class ChangePIN:
    def __init__(self, window=None):
        self.master = window
        window.geometry("300x150")
        Label(window, text="New PIN:").pack()
        self.pin = Entry(window, show="*"); self.pin.pack()
        Button(window, text="Change", command=self.do).pack(pady=10)
    def do(self):
        change_PIN(customer_accNO, self.pin.get())
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    welcomeScreen(root)
    root.mainloop()
