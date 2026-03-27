from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from tkinter.ttk import Style
from datetime import datetime
from tkcalendar import Calendar
import re
import pickle


## Window Creation ##
root = Tk()
root.geometry("1000x600")
root.title("Booksly")


## underlined font ##
underlined_font = font.Font(family = "Helvatica", size = 12, underline = True)


## Creating Classes ##
class Profile:
    personalID_cntr = 1
   
    def __init__(self, firstname: str, surname: str, dob: list, phone_number: str, email: str):
        self.personalID = self.personalID_cntr
        Profile.personalID_cntr += 1
       
        self.firstname = firstname
        self.surname = surname
        self.dob = datetime(dob[0], dob[1], dob[2])
        self.phone_number = phone_number
        self.email = email
        self.date_created = datetime.now().strftime("%d/%m/%Y, %H:%M:")
       
        self.valid = True     



class User(Profile):
   
    staff_cntr = 1
   
    def __init__(self, firstname: str, surname: str, dob: str, phone_number: str, email: str, postcode: str, username: str, staff_password: str, working_hours: dict, services: list, notes: str, isAdmin = False, isStaff = False):
        super().__init__(firstname, surname, dob, phone_number, email)
       
        self.postcode = postcode
        self.isAdmin = isAdmin
        self.isStaff = isStaff
        self.username = username
        self.staff_password = staff_password
        self.working_hours = working_hours
        self.services = services
        self.notes = notes
        
        self.bookings = {
            "January": [],
            "February": [],
            "March": [],
            "April": [],
            "May": [],
            "June": [],
            "July": [],
            "August": [],
            "September": [],
            "October": [],
            "November": [],
            "December": [],
        }
       
        self.staff_id = self.staff_cntr
        User.staff_cntr += 1
        
    @classmethod
    def validate_personal_info(cls, firstname: str, surname: str, dob: dict,  window: Frame, ID: int = 0) -> bool:
        firstname = firstname.strip()
        surname = surname.strip()
        
        firstname_pattern = r"^[A-Z][a-z]{2,19}$"
        
        if not bool(re.match(firstname_pattern, firstname)):
            messagebox.showerror("Error", "Firstname is incorrect")
            window.lift()
            window.focus_force()
            return False
        
        surname_pattern = r"^[A-Z][a-z]{2,19}$"
        
        if not bool(re.match(surname_pattern, surname)):
            messagebox.showerror("Error", "Surname is incorrect")
            window.lift()
            window.focus_force()
            return False


        # DoB
        months = {
            "01": 31,
            "02": 28,
            "03": 31,
            "04": 30,
            "05": 31,
            "06": 30,
            "07": 31,
            "08":31, 
            "09":30, 
            "10": 31,
            "11": 30,
            "12": 31
        }


        if not dob["day"].isdigit():
            messagebox.showerror("Error", "Invalid Day")
            window.lift()
            window.focus_force()
            return False
        
        if not(dob["month"] in months):
                messagebox.showerror("Error", "Invalid Month")
                window.lift()
                window.focus_force()
                return False
            
        if int(dob["day"]) > months[dob["month"]] or int(dob["day"]) < 1:
            messagebox.showerror("Error", "Invalid Day")
            window.lift()
            window.focus_force()
            return False
        
        if not isinstance(dob["month"], str):
            messagebox.showerror("Error", "Invalid Month")
            window.lift()
            window.focus_force()
            return False
        
        if not(dob["year"].isdigit()):
            messagebox.showerror("Wrong", "Invalid Year")
            window.lift()
            window.focus_force()
            return
        
        if int(dob["year"]) > datetime.now().year or int(dob["year"]) < datetime.now().year - 100:
            messagebox.showerror("Error", "Invalid Year")
            window.lift()
            window.focus_force()
            return False


        dob_object = datetime(int(dob["year"]), int(dob["month"]), int(dob["day"]))
        today = datetime.today()
        age = today.year - dob_object.year
        
        if (today.month, today.day) < (dob_object.month, dob_object.day):
            age -= 1
        
        if age < 18:
            messagebox.showerror("Error", "Staff is less than 18 years old")
            window.lift()
            window.focus_force()
            return False
            
        #check staff accounts
        with open("user_data.pickle","rb") as f: 
            users = pickle.load(f)
            
            if ([x for x in users if x.firstname == firstname and x.staff_id != ID] and 
                [x for x in users if x.surname == surname and x.staff_id != ID] and 
                [x for x in users if x.dob.strftime("%d/%m/%Y") == f"{dob["day"]}/{dob["month"]}/{dob["year"]}" and x.staff_id != ID]):
                            
                if not messagebox.askyesno("Account Creation", "An account with this name and date of birth already exist. Continue?"):
                    window.lift()
                    window.focus_force()
                    return False
            
            # check customer accounts
            with open("customer_data.pickle","rb") as f:
                customers = pickle.load(f)
                
                if ([x for x in customers if x.firstname == firstname] and 
                    [x for x in customers if x.surname == surname] and 
                    [x for x in customers if x.dob.strftime("%d/%m/%Y") == f"{dob["day"]}/{dob["month"]}/{dob["year"]}"]):
                    
                    if not messagebox.askyesno("Account Creation", "An account with this name and date of birth already exist. Continue?"):
                        window.lift()
                        window.focus_force()
                        return False
        
        return True
   
    @classmethod
    def validate_contact_info(cls, email: str, c_email: str, phone_number: str, postcode: str, window: Frame, ID: int = 0) -> bool:
        email = email.strip()
        c_email = c_email.strip()
        phone_number = phone_number.strip()
        postcode = postcode.strip()
        
        # Email # 
        if email == "": 
            messagebox.showerror("Error", "Invalid email")
            window.lift()
            window.focus_force()
            return False
        
        if email == c_email:
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"




            if not re.match(email_pattern, email):
                messagebox.showerror("Error", "Invalid email")
                window.lift()
                window.focus_force()
                return False
        else:
            messagebox.showerror("Error", "Invalid email")
            window.lift()
            window.focus_force()
            return False
        
        # Phone number #
        pattern = r"^[0-9]{8,13}$"
        
        if not bool(re.match(pattern, phone_number)):
            messagebox.showerror("Error", "Phone Number is incorrect")
            window.lift()
            window.focus_force()
            return False
        
        # Postcode # 
        postcode = postcode.replace(" ", "").upper()
        
        pattern = r"^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2}$"
        
        if not bool(re.match(pattern, postcode)):
            messagebox.showerror("Error", "Postcode is invalid")
            window.lift()
            window.focus_force()
            return False
        
        # check customer accounts
        with open("user_data.pickle","rb") as f:
            users = pickle.load(f)








            if [x for x in users if x.email == email and x.staff_id != ID]:
                messagebox.showerror("Error", "A different account already has this email")
                window.lift()
                window.focus_force()
                return False
                
            if [x for x in users if x.phone_number == phone_number and x.staff_id != ID]:
                messagebox.showerror("Error", "A different account already has this phone number")
                window.lift()
                window.focus_force()
                return False
            
        # check customer accounts
        with open("customer_data.pickle","rb") as f:
            customers = pickle.load(f)
                
            if [x for x in customers if x.email == email]:
                messagebox.showerror("Error", "A different account already has this email")
                window.lift()
                window.focus_force()
                return False
                
            if [x for x in customers if x.phone_number == phone_number]:
                messagebox.showerror("Error", "A different account already has this phone number")
                window.lift()
                window.focus_force()
                return False
                    
        return True




    @classmethod
    def validate_account_info(cls, username: str, password: str, role:str, window: Frame, exists = False) -> bool:
        username = username.strip()
        password = password.strip()
        role = role.strip()








        if role not in["Admin", "Both", "Staff"]:
            messagebox.showerror("Error","Choose a staff role")
            window.lift()
            window.focus_force()
            return False
        
        # Username #
        if username == "1" and password == "1": return True
        
        pattern = r"^(?!.*[_-]{2})[a-zA-Z][a-zA-Z0-9_-]{2,19}$"
        
        if not bool(re.match(pattern, username)):
            messagebox.showerror("Error","Invalid username format")
            window.lift()
            window.focus_force()
            return False
        
        with open("user_data.pickle", "rb") as f: user = pickle.load(f)








        for i in range(len(user)):
            if exists == True: break
            if username == user[i].username:
                messagebox.showerror("Error", "Username is already taken")
                window.lift()
                window.focus_force()
                return False




        # Password # 
        
        if len(password) < 5 or len(password) > 20:
            messagebox.showerror("Error", "Password is too long or too short")
            window.lift()
            window.focus_force()
            return False
        
        # Check for uppercase letter
        if not re.search(r"[A-Z]", password):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter")
            window.lift()
            window.focus_force()
            return False
        
        # Check for lowercase letter
        if not re.search(r"[a-z]", password):
            messagebox.showerror("Error", "Password must contain at least one lowercase letter")
            window.lift()
            window.focus_force()
            return False
        
        # Check for digit
        if not re.search(r"\d", password):
            messagebox.showerror("Error", "Password must contain at least one number")
            window.lift()
            window.focus_force()
            return False
        
        # Check for special character
        if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
            messagebox.showerror("Error", "Some of the characters in the password are not allowed")
            window.lift()
            window.focus_force()
            return False
        
        return True
    
    @classmethod
    def validate_work_hours(cls, work_hours_dict: dict, role: str, window: Frame) -> bool:
        role = role.strip()
        
        if role not in ["Both","Staff", "Admin"]:
            messagebox.showerror("Error", "Role chosen is incorrect")
            window.lift()
            window.focus_force()
            return False
        
        ## work hours ##
        if role != "Admin":




            if  not any(any(hour != "" for hour in day) for day in work_hours_dict.values()):
                messagebox.showerror("Error", "One working day has to be done")
                window.lift()
                window.focus_force()
                return False
            
            for day in work_hours_dict.keys():
                start = work_hours_dict[day][0]
                end = work_hours_dict[day][1]
                
                if len(start) == 0 and len(end) != 0:
                    messagebox.showerror("Error", f"Start of {day} has not been filled")
                    window.lift()
                    window.focus_force()
                    return False
                elif len(start) != 0 and len(end) == 0:
                    messagebox.showerror("Error", f"End of {day} has not been filled")
                    window.lift()
                    window.focus_force()
                    return False
                elif len(start) == 0 and len(end) == 0:
                    continue
                
                if start.isdigit():
                    if start not in ["7","8","9"]:
                        x = f"Staff cannot start this early on {day}\n Choose from: 7, 8, 9" if int(start) < 7 else f"Staff cannot start this late on {day}\n Choose from: 7, 8, 9"
                        messagebox.showerror("Error", x)
                        window.lift()
                        window.focus_force()
                        return False
                else:
                    messagebox.showerror("Error", f"{day} start has to be number only")
                    window.lift()
                    window.focus_force()
                    return False
                
                if end.isdigit():
                    if end not in ["17","18","19"]:
                        x = f"Staff cannot end this early {day}\n Choose from: 17, 18, 19" if int(end) < 17 else f"Staff cannot end this late {day}\n Choose from: 17, 18, 19"
                        messagebox.showerror("Error", x)
                        window.lift()
                        window.focus_force()
                        return False
                else:
                    messagebox.showerror("Error", f"{day} start has to be number only")
                    window.lift()
                    window.focus_force()
                    return False
            
            return True
        else:
            if  any(any(hour != "" for hour in day) for day in work_hours_dict.values()):
                messagebox.showerror("Error", "Admin cannot have any working hours")
                window.lift()
                window.focus_force()
                return False
            return True
        
    @classmethod
    def validate_work_services(cls, services: list, role: str, window: Frame) -> bool:
        role = role.strip()
        
        ## services ##
        if role == "Admin" and len(services) != 0:
            messagebox.showerror("Error","Admins cannot ave any services")
            window.lift()
            window.focus_force()
            return False
        elif role == "Admin":
            return True
        if role != "Admin" and len(services) == 0:
            messagebox.showerror("Error","At least one service must be selected")
            window.lift()
            window.focus_force()
            return False
        
        allowed_services = [
            "Haircut", "Hair trim", "Wash and blow-dry", 
            "Restyle", "Fringe trim", "Full hair dye","Root touch-up", 
            "Highlights", "Balayage", "Toner application", "Beard trim", 
            "Beard shaping", "Beard colouring","Hot towel shave", 
            "Deep conditioning treatment", "Hair mask treatment", "Keratin treatment"
            ]
        
        if services == "": 
            return True
        
        for service in services:
            if service not in allowed_services: 
                messagebox.showerror("Error","One of the services is entered wrong")
                window.lift()
                window.focus_force()
                return False
        
        return True
        
    @classmethod
    def validate_notes_info(cls, notes: str, window: Frame)-> bool:
        notes = notes.strip()
        
        if len(notes) > 100: 
            messagebox.showerror("Error", "Notes are too long")
            window.lift()
            window.focus_force()
            return False
        else:
            return True








class Staff(User):




    def __init__(self, firstname, surname, dob, phone_number, email, postcode, username, staff_password, working_hours, services, notes, isAdmin = False, isStaff = False):
        super().__init__( firstname, surname, dob, phone_number, email, postcode, username, staff_password, working_hours, services, notes, isAdmin, isStaff)








class Admin(User):
   
    def __init__(self, firstname, surname, dob, phone_number, email, postcode, username, staff_password, working_hours, services, notes, isAdmin = False, isStaff = False):
        super().__init__(firstname, surname, dob, phone_number, email, postcode, username, staff_password, working_hours, services,notes, isAdmin, isStaff)








class Customer(Profile):
   
    customer_cntr = 1
   
    def __init__(self, firstname: str, surname: str, dob: list, phone_number: str, email: str, c_email: str, notes: str):
        super().__init__(firstname, surname, dob, phone_number, email)
        
        self.customer_id = self.customer_cntr
        self.c_email = c_email
        self.notes = notes
       
        Customer.customer_cntr += 1
    
    @classmethod
    def validate_customer(self, firstname: str, surname: str, dob: dict, phone_number: str, email: str, c_email: str, window: Frame, ID: int = 0) -> bool:
        firstname = firstname.strip()
        surname = surname.strip()
        phone_number = phone_number.strip()
        email = email.strip()
        c_email = c_email.strip()
        
        # Firstname Validation
        firstname_pattern = r"^[A-Z][a-z]{2,19}$"
        
        if not bool(re.match(firstname_pattern, firstname)):
            
            messagebox.showerror("Error", "Firstname is incorrect")
            window.lift()
            window.focus_force()
            return False
        # Surname Validation
        surname_pattern = r"^[A-Z][a-z]{2,29}$"




        if not bool(re.match(surname_pattern, surname)):
            messagebox.showerror("Error", "Surname is incorrect")
            window.lift()
            window.focus_force()
            return False








        # Date of Birth validaiton
        months = {
            "01": 31,
            "02": 28,
            "03": 31,
            "04": 30,
            "05": 31,
            "06": 30,
            "07": 31,
            "08":31, 
            "09":30, 
            "10": 31,
            "11": 30,
            "12": 31
        }








        if not dob["day"].isdigit():
            messagebox.showerror("Error", "Invalid Day")
            window.lift()
            window.focus_force()
            return False
        
        if not(dob["month"] in months):
                messagebox.showerror("Error", "Invalid Month")
                window.lift()
                window.focus_force()
                return False
            
        if int(dob["day"]) > months[dob["month"]] or int(dob["day"]) < 1:
            messagebox.showerror("Error", "Invalid Day")
            window.lift()
            window.focus_force()
            return False
        
        if not isinstance(dob["month"], str):
            messagebox.showerror("Error", "Invalid Month")
            window.lift()
            window.focus_force()
            return False
        
        if not(dob["year"].isdigit()):
            messagebox.showerror("Wrong", "Invalid Year")
            window.lift()
            window.focus_force()
            return
        
        if int(dob["year"]) > datetime.now().year or int(dob["year"]) < datetime.now().year - 100:
            messagebox.showerror("Error", "Invalid Year")
            window.lift()
            window.focus_force()
            return False








        # Phone nomber validation
        phone_number_pattern = r"^[0-9]{8,13}$"
        
        if not bool(re.match(phone_number_pattern, phone_number)):
            messagebox.showerror("Error", "Phone Number is incorrect")
            window.lift()
            window.focus_force()
            return False








        # Email Validation
        if email == "": 
            messagebox.showerror("Error", "Invalid email")
            window.lift()
            window.focus_force()
            return False
        
        
        if email == c_email:
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"








            if not re.match(email_pattern, email):
                messagebox.showerror("Error", "Invalid email")
                window.lift()
                window.focus_force()
                return False
        else:
            messagebox.showerror("Error", "Invalid email")
            window.lift()
            window.focus_force()
            return False
        
            
        # check customer accounts
        with open("customer_data.pickle","rb") as f:
            customers = pickle.load(f)




            # check for an existing customer account so no duplicate emails
            if [x for x in customers if x.email == email and x.customer_id != ID]:
                messagebox.showerror("Error", "A different account already has this email")
                window.lift()
                window.focus_force()
                return False
            
            # check for an existing customer account so no duplicate phone numbers
            if [x for x in customers if x.phone_number == phone_number and x.customer_id != ID]:
                messagebox.showerror("Error", "A different account already has this phone number")
                window.lift()
                window.focus_force()
                return False
            
            # check for an exisitng customer account for firstname, surname, and date of birth to inform user
            if ([x for x in customers if x.firstname == firstname and x.customer_id != ID] and 
                [x for x in customers if x.surname == surname and x.customer_id != ID] and 
                [x for x in customers if x.dob.strftime("%d/%m/%Y") == f"{dob["day"]}/{dob["month"]}/{dob["year"]}" and x.customer_id != ID]):
                    
                if not messagebox.askyesno("Account Creation", "An account with this name and date of birth already exist. Continue?"):
                    window.lift()
                    window.focus_force()
                    return False
            
            # check staff accounts
            with open("user_data.pickle","rb") as f: 
                users = pickle.load(f)
            
                if ([x for x in users if x.firstname == firstname] and 
                    [x for x in users if x.surname == surname] and 
                    [x for x in users if x.dob.strftime("%d/%m/%Y") == f"{dob["day"]}/{dob["month"]}/{dob["year"]}"]):
                                
                    if not messagebox.askyesno("Account Creation", "An account with this name and date of birth already exist. Continue?"):
                        window.lift()
                        window.focus_force()
                        return False
                        
                if [x for x in users if x.email == email]:
                    messagebox.showerror("Error", "A different account already has this email")
                    window.lift()
                    window.focus_force()
                    return False
                        
                if [x for x in users if x.phone_number == phone_number]:
                    messagebox.showerror("Error", "A different account already has this phone number")
                    window.lift()
                    window.focus_force()
                    return False
        
        return True








class Booking:




    booking_cntr = 1
    
    bookings_dict = {
        "January": {},
        "February": {},
        "March": {},
        "April": {},
        "May": {},
        "June": {},
        "July": {},
        "August": {},
        "September": {},
        "October": {},
        "November": {},
        "December": {}
    }








    for key in bookings_dict:
        if key in ["January", "March", "August", "July", "May", "October", "December"]:
            for days in range(1, 32):
                bookings_dict[key][days] = {}
                for working_hours in range(7,20):
                    bookings_dict[key][days][working_hours] = []
        if key in ["April", "June", "September", "November"]:
            for days in range(1, 31):
                bookings_dict[key][days] = {}
                for working_hours in range(7,20):
                    bookings_dict[key][days][working_hours] = []
        if key == "February":
            for days in range(1, 29):
                bookings_dict[key][days] = {}
                for working_hours in range(7,20):
                    bookings_dict[key][days][working_hours] = []
    
    def __init__(self, customer: str, staff: str, slot: int, date: datetime, services: list, notes: str):
        
        self.booking_id = self.booking_cntr
        
        self.customer = customer
        self.staff = staff
        self.slot = slot
        self.date = date
        self.services = services
        self.notes = notes
        
        Booking.booking_cntr += 1


## Windows ##
class Log_In_Window:

    def __init__(self):
        self.log_window_frame = None
        self.log_window_username_entry = None
        self.log_window_password_entry = None
        self.log_window_button = None
        self.username_var = StringVar()
        self.password_var = StringVar()

    ## Create Log In window ##
    def create_window(self):




        if self.log_window_frame: self.log_window_frame.destroy()
        
        self.log_window_frame = Frame(root, width = 1000, height = 600, bg = "light blue")
        self.log_window_frame.place(x = 0, y = 0)
        
        log_window_username_label = Label(self.log_window_frame, bg = "light blue", height = 2, width = 10, text = "Username:", font = ("Helvatica", 18))
        log_window_username_label.place(x = 220,y = 170)








        log_window_password_label = Label(self.log_window_frame, bg = "light blue", height = 2, width = 10, text = "Password:", font = ("Helvatica", 18))
        log_window_password_label.place(x = 220, y = 245)








        self.log_window_username_entry = Entry(self.log_window_frame, textvariable = self.username_var, font = ("Helvatica", 18))
        self.log_window_username_entry.place(x = 390, y = 185)








        self.log_window_password_entry = Entry(self.log_window_frame, textvariable = self.password_var, show = "*", font = ("Helvatica", 18))
        self.log_window_password_entry.place(x = 390, y = 260)






        self.log_window_button = Button(self.log_window_frame, text = "Log In", height = 2, width = 10, command = lambda: self.LogIn(), font = ("Helvatica", 18))
        self.log_window_button.place(x = 420, y = 330)

    # Check entries
    def LogIn(self):
        if self.username_var.get() == "" and self.password_var.get() == "":
            messagebox.showwarning("Log In Error", "Username and Entry fields are empty")
            return
           
        with open("user_data.pickle", "rb") as f: 
            staff = pickle.load(f)

        # Loop through staff accounts to check if an account with that username or password exists
        for account in staff:
            if self.username_var.get() == account.username and self.password_var.get() == account.staff_password:
                logged_user = account
                self.log_window_username_entry.delete(0, END)
                self.log_window_password_entry.delete(0, END)
               
                # If there is a match send the user to the main window
                if self.log_window_frame: self.log_window_frame.destroy()
                main_window.create_window(logged_user)
                return
        
        messagebox.showerror("Log In cridentials", "Username/Password entered is wrong")




class MainWindow:
   
    def __init__(self):




        self.main_window_frame = None
        self.Customer_Window_Button = None




    # Main Command Window for application
    def create_window(self, logged_user: object):
        if self.main_window_frame: self.main_window_frame.destroy()


        ## delete customer window ##
        if customer_window.customer_window_frame: customer_window.customer_window_frame.destroy()
        if customer_window.header_frame: customer_window.header_frame.destroy()


        ## delete staff frames ##
        if staff_window.staff_window_frame: staff_window.staff_window_frame.destroy()
        if staff_window.header_frame: staff_window.header_frame.destroy()


        ## delete view booking window ## 
        if view_booking_window.booking_window_frame: view_booking_window.booking_window_frame.destroy() 
        if view_booking_window.header_frame: view_booking_window.header_frame.destroy()








        ## delete booking window ## 
        if booking_window.customer_window_frame: booking_window.customer_window_frame.destroy()
        if booking_window.header_frame: booking_window.header_frame.destroy()








        self.main_window_frame = Frame(root, width = 1000, height = 600, bg = "light blue")
        self.main_window_frame.place(x = 0, y = 0)
       
        # Sends user to view customers
        self.Customer_Window_Button = Button(self.main_window_frame, text = "Customer", height = 2, width = 30, command = lambda: customer_window.create_window(logged_user), font = ("Helvatica", 18))
        self.Customer_Window_Button.place(x = 100, y = 75)








        # Staff Window appears only if logged user is an "Admin" or "Both"
        if logged_user.isAdmin == True:
            self.Staff_Window_Button = Button(self.main_window_frame, text = "Staff", height = 2, width = 30, command = lambda: staff_window.create_window(logged_user), font = ("Helvatica", 18))
            self.Staff_Window_Button.place(x = 100, y = 175)
       
        # Sends user to view bookings
        self.View_Bookings_Window_Button = Button(self.main_window_frame, text = "View Bookings", height = 2, width = 30, font = ("Helvatica", 18), command = lambda: view_booking_window.create_window(logged_user))
        self.View_Bookings_Window_Button.place(x = 100, y = 275)
       
        # Sends user to make a booking
        self.Make_Booking = Button(self.main_window_frame, text = "Make A Booking", height = 2, width = 30, font = ("Helvatica", 18), command = lambda: booking_window.create_window(logged_user))
        self.Make_Booking.place(x = 100, y = 375)
        
        Label(self.main_window_frame, text = f"Welcome \n{logged_user.firstname}", font = ("helvatica", 24), bg = "light blue").place(x = 650, y = 200)
       
        # Sends user to Log In window
        self.Log_out_Button = Button(self.main_window_frame, text = "Log Out", width = 7, height = 2, command = self.Log_out, font = ("Helvatica", 18))
        self.Log_out_Button.place(x = 850, y = 500)
       
    def Log_out(self):
        if self.main_window_frame: self.main_window_frame.destroy()
        log_in_window.create_window()




class CustomerWindow:
   
    def __init__(self):
        ## ----------- ##
        ## Main Frames ##
        ## ----------- ##




        self.customer_window_frame = None
        self.scroll_window_canvas = None
        self.scroll_window_frame = None
        self.scrollbar = None
        self.customer_window_frame2 = None
        self.customer_info_window = None
        self.header_frame = None








        ## -------------------------- ##
        ## Viewing Customer Variables ##
        ## -------------------------- ##




        self.firstname_var = StringVar()
        self.surname_var = StringVar()
        self.DoB_var = StringVar()
        self.phone_number_var = StringVar()
        self.email_var = StringVar()
        self.date_created_var = StringVar()
       
        ## ---------------------- ##
        ## Add Customer Variables ##
        ## ---------------------- ##
        
        self.add_customer_window = None
        
        self.firstname_cust_var = StringVar()
        self.surname_cust_var = StringVar()
        self.DoB_cust_var = StringVar()
        self.phone_number_cust_var = StringVar()
        self.email_cust_var = StringVar()
        self.c_email_cust_var = StringVar()
         
    def create_window(self, logged_user: object, add_customer_window: Frame = None):
        
        self.logged_user = logged_user
       
        if add_customer_window: add_customer_window.destroy()








        if main_window.main_window_frame: main_window.main_window_frame.destroy()








        ## Reset Customer Window ##
        if self.header_frame: self.header_frame.destroy()
        if self.customer_window_frame: self.customer_window_frame.destroy()








        ## Display Customers ##
        self.header_frame = Frame(root, height = 50, bg = "light blue")
        self.header_frame.pack(fill = X)








        back_button = Button(self.header_frame, text = "Go Back", command = lambda: main_window.create_window(logged_user), height = 2, width = 10)
        back_button.grid(column = 2, row = 0, padx = 20)








        create_customer_button = Button(self.header_frame, text = "Create Customer", command = lambda: self.create_customer(logged_user), height = 2, width = 15)
        create_customer_button.grid(column = 1, row = 0, padx = 300)








        Label(self.header_frame, bg =  "light blue", text = "Customer List", font = ("Helvatica", 18)).grid(column = 0, row = 0)








        ## Main Area ##
        self.customer_window_frame = Frame(root, bg = "light blue")
        self.customer_window_frame.pack(fill = BOTH, expand = TRUE)








        self.main_content = Frame(self.customer_window_frame, bg = "light blue")
        self.main_content.pack(fill = BOTH, expand = True)
        
        self.main_content.columnconfigure(0, weight = 1)
        self.main_content.columnconfigure(1, weight = 0)
        self.main_content.rowconfigure(0, weight = 1)
        
        ## Scroll Area ##
        self.canvas_container = Frame(self.main_content, bg = "light blue")
        self.canvas_container.grid(row = 0, column = 0, sticky = "nsew")
       
        self.scroll_window_canvas = Canvas(self.canvas_container, bg = "light blue")
        self.scroll_window_canvas.pack(side = LEFT, fill = BOTH, expand = True)








        self.scrollbar = ttk.Scrollbar(self.canvas_container, orient = VERTICAL, command = self.scroll_window_canvas.yview)
        self.scrollbar.pack(side = RIGHT, fill = Y)








        self.scroll_window_canvas.configure(yscrollcommand = self.scrollbar.set)
        self.scroll_window_canvas.bind("<Configure>", lambda e: self.scroll_window_canvas.configure(scrollregion = self.scroll_window_canvas.bbox("all")))








        self.customer_window_frame2 = Frame(self.scroll_window_canvas, bg = "light blue")
        self.canvas_window = self.scroll_window_canvas.create_window((0,0), window = self.customer_window_frame2, anchor = "nw")








        self.customer_window_frame2.bind("<Configure>", lambda e: self.scroll_window_canvas.configure(scrollregion = self.scroll_window_canvas.bbox("all")))
        self.scroll_window_canvas.bind("<Configure>", lambda e:self.scroll_window_canvas.itemconfig(self.canvas_window, width = e.width))








        ## Search Area ##
        self.search_panel = Frame(self.main_content, bg = "light blue", width = 120)
        self.search_panel.grid(row = 0, column = 1, sticky = "ns")
        self.search_panel.grid_propagate(False)
        
        Label(self.search_panel, text = "Search by name", bg = "light blue", font = underlined_font).pack(pady = 10)
        
        self.search_entry_name = Entry(self.search_panel)
        self.search_entry_name.pack(padx = 5, pady = 5)
        
        Label(self.search_panel, text = "Search by phone number", bg = "light blue", font = underlined_font).pack(pady = 10)
        
        self.search_entry_phone_number = Entry(self.search_panel)
        self.search_entry_phone_number.pack(padx = 5, pady = 5)
        
        Label(self.search_panel, text = "Search by DoB", bg = "light blue", font = underlined_font).pack(pady = 10)
        
        days  =[f"{x:02}" for x in range(1, 32)]
        months = [f"{x:02}" for x in range(1, 13)]
        year = [x for x in range(int(datetime.now().year) - 100, int(datetime.now().year) + 1)][::-1]
        
        self.cb_day_search = ttk.Combobox(self.search_panel, values = days, width = 8)
        self.cb_day_search.set("Day")
        self.cb_day_search.pack(pady = 5)
        
        self.cb_month_search = ttk.Combobox(self.search_panel, values = months, width = 8)
        self.cb_month_search.set("Month")
        self.cb_month_search.pack(pady = 5)
        
        self.cb_year_search = ttk.Combobox(self.search_panel, values = year, width = 8)
        self.cb_year_search.set("Year")
        self.cb_year_search.pack(pady = 5)
        
        
        Button(self.search_panel, text = "Search", font = ("Helvatica", 20), command = lambda: self.search_customers(name = self.search_entry_name.get(), phone_number = self.search_entry_phone_number.get(), dob_list = [self.cb_day_search.get(), self.cb_month_search.get(), self.cb_year_search.get()])).pack(pady = 5, side = "bottom")
        Button(self.search_panel, text = "Reset", font = ("Helvatica", 20), command = lambda: self.create_window(self.logged_user)).pack(pady = 5, side = "bottom")
    
        # Sort customers based on firstname and surname in descending order
        ordered_customer_list = []
        
        with open("customer_data.pickle", "rb") as f: 
            customers = pickle.load(f)




            ordered_customer_list = sorted(customers, key = lambda e: f"{e.firstname} {e.surname}")




        # Display each customer as a button
        y = 50
        for customer in ordered_customer_list:
            def create_button(customer):
                Button(self.customer_window_frame2, command = lambda: self.open_customer(customer, logged_user), text = f"{customer.firstname} {customer.surname}", width = 68, font = ("Helvatica", 18)).pack(padx = 10, pady = 5)
           
            create_button(customer)
            y += 50

    def open_customer(self, customer: object, logged_user: object):




        if self.customer_info_window: self.customer_info_window.destroy()
       
       
        self.customer_info_window = Toplevel(root, bg = "light blue")
        self.customer_info_window.geometry("400x525")








        # Customer attributes labels
        Label(self.customer_info_window, bg = "light blue", text = f"Customer ID: {customer.customer_id}", width = 15, height = 2).grid(row = 0, column = 0, columnspan = 2)
        Label(self.customer_info_window,bg = "light blue", text = "Firstname:*", width = 15, height = 2).grid(column = 0, row = 1, pady = 5, padx = 3)
        Label(self.customer_info_window,bg = "light blue", text = "Surname:", width = 15, height = 2).grid(column = 0, row = 2, pady = 5, padx = 3)
        Label(self.customer_info_window,bg = "light blue", text = "Date of Birth:", width = 15, height = 2).grid(column = 0, row = 3, pady = 5, padx = 3)
        Label(self.customer_info_window,bg = "light blue", text = "Phone Number:", width = 15, height = 2).grid(column = 0, row = 4, pady = 5, padx = 3)
        Label(self.customer_info_window,bg = "light blue", text = "Email:", width = 15, height = 2).grid(column = 0, row = 5, pady = 5, padx = 3)
        Label(self.customer_info_window,bg = "light blue", text = "Date Created:", width = 15, height = 2).grid(column = 0, row = 6, pady = 5, padx = 3)
        Label(self.customer_info_window,bg = "light blue", text = "Notes:", width = 15, height = 2).grid(column = 0, row = 7, pady = 5, padx = 3)








        # Firstname entry
        firstname_entry = Entry(self.customer_info_window,textvariable = self.firstname_var, width = 35)
        firstname_entry.grid(column = 1, row = 1, pady = 5, padx = 3)
        firstname_entry.delete(0,END)
        firstname_entry.insert(0, customer.firstname)








        # Surname entry
        surname_entry = Entry(self.customer_info_window,textvariable = self.surname_var, width = 35)
        surname_entry.grid(column = 1, row = 2, pady = 5, padx = 3)
        surname_entry.delete(0, END)
        surname_entry.insert(0, customer.surname)








        # Date of birth dropdowns
        days  =[f"{x:02}" for x in range(1, 32)]
        months = [f"{x:02}" for x in range(1, 13)]
        year = [x for x in range(int(datetime.now().year) - 100, int(datetime.now().year) + 1)][::-1]
        
        self.cb_day = ttk.Combobox(self.customer_info_window, values = days, width = 5)
        self.cb_day.set(customer.dob.strftime("%d,%m,%Y").split(",")[0])
        self.cb_day.grid(row = 3, column = 1, padx = (0, 160))
        
        self.cb_month = ttk.Combobox(self.customer_info_window, values = months, width = 10)
        self.cb_month.set(customer.dob.strftime("%d,%m,%Y").split(",")[1])
        self.cb_month.grid(row = 3, column = 1)
        
        self.cb_year = ttk.Combobox(self.customer_info_window, values = year, width = 5)
        self.cb_year.set(customer.dob.strftime("%d,%m,%Y").split(",")[2])
        self.cb_year.grid(row = 3, column = 1, padx = (160, 0))








        # Phone number entry
        phone_number_entry = Entry(self.customer_info_window,textvariable = self.phone_number_var, width = 35)
        phone_number_entry.grid(column = 1, row = 4, pady = 5, padx = 3)
        phone_number_entry.delete(0,END)
        phone_number_entry.insert(0, customer.phone_number)








        # Email entry
        email_entry = Entry(self.customer_info_window,textvariable = self.email_var, width = 35)
        email_entry.grid(column = 1, row = 5, pady = 5, padx = 3)
        email_entry.delete(0,END)
        email_entry.insert(0, customer.email)








        # Date created entry
        date_created_label = Label(self.customer_info_window, textvariable = self.date_created_var, width = 30, bg = "light blue")
        date_created_label.grid(column = 1, row = 6, pady = 5, padx = 3)
        self.date_created_var.set(customer.date_created[0:len(customer.date_created)-1])




        # notes
        words = customer.notes.split()
        notes_lines = []
        
        for i in range(0, len(words), 5):
            notes_lines.append(" ".join(words[i:i + 5]))
        notes_str = "\n".join(notes_lines)




        num_lines = max(1, len(notes_lines))








        # Notes
        notes_text = Text(self.customer_info_window, height = num_lines, width = 27)
        notes_text.insert("1.0", notes_str)
        notes_text.grid(column = 1, row = 7, pady = 5, padx = 3, columnspan = 3)








        change_customer_button = Button(self.customer_info_window, command = lambda: self.confirm_changes(C_customer = customer, notes = notes_text.get("1.0", "end-1c"),logged_user = logged_user, date = [self.cb_day.get(), self.cb_month.get(), self.cb_year.get()]), height = 3, width = 15, text = "Confirm Changes")
        change_customer_button.grid(column = 1, row = 8,padx = 10, pady = 10)








        # If logged user is admin allow them to delete customer
        if logged_user.isAdmin == True:
            delete_customer_button = Button(self.customer_info_window,command = lambda: self.delete_customer(customer, logged_user), text = "Delete Customer", height = 3, width = 15)
            delete_customer_button.grid(column = 0, row = 8, padx = 10, pady = 10)

    def delete_customer(self, D_customer: object, logged_user: object):
        customers_list = []




        if not messagebox.askyesno("Confirmation", "Delete Customer account?"):
            self.customer_info_window.lift()
            self.customer_info_window.focus_force()
            return




        with open("customer_data.pickle", "rb") as f:
            customers = pickle.load(f)




            for customer in customers:
                if customer.customer_id != D_customer.customer_id:
                    customers_list.append(customer)
           
        with open("customer_data.pickle", "wb") as f:
            pickle.dump(customers_list, f)




        # Remove bookings linked to customer
        with open("bookings.pickle", "rb") as f:
            bookings = pickle.load(f)




            for month in Booking.bookings_dict:
                for day in Booking.bookings_dict[month]:
                    for slot in Booking.bookings_dict[month][day]:
                        updated_slot_booking = []
                        for booking in Booking.bookings_dict[month][day][slot]:
                            if booking.customer.customer_id != D_customer.customer_id:
                                
                                updated_slot_booking.append(booking)
                                
                        Booking.bookings_dict[month][day][slot] = updated_slot_booking




        updated_bookings = [b for b in bookings if b.customer.customer_id != D_customer.customer_id]








        with open("bookings.pickle", "wb") as f:
            pickle.dump(updated_bookings, f)








        # Update staff bookings
        with open("user_data.pickle", "rb") as f:
            staffs = pickle.load(f)








        for staff in staffs:
            for month in staff.bookings:
                staff.bookings[month] = [b for b in staff.bookings[month]if b.customer.customer_id != D_customer.customer_id]




        with open("user_data.pickle", "wb") as f:
            pickle.dump(staffs, f)
           
        self.customer_info_window.destroy()
        customer_window.create_window(logged_user)
        messagebox.showinfo("Customer Database", "Customer has been successfully deleted")
        
    def confirm_changes(self, C_customer: object, notes: str, logged_user: object, date: list = []):
        
        with open("customer_data.pickle", "rb") as f:
            customers = pickle.load(f)




            for customer in customers:
                if customer.customer_id == C_customer.customer_id:




                    date_of_birth = {
                        "day": date[0],
                        "month": date[1],
                        "year": date[2]
                    }
                    
                    if Customer.validate_customer(firstname = self.firstname_var.get(), surname = self.surname_var.get(), dob = date_of_birth, phone_number = self.phone_number_var.get(), email = self.email_var.get(), c_email = self.email_var.get(), ID = C_customer.customer_id, window = self.customer_info_window):
                        customer.firstname = self.firstname_var.get()
                        customer.surname = self.surname_var.get()
                        customer.dob = datetime(int(date_of_birth["year"]), int(date_of_birth["month"]), int(date_of_birth["day"]))
                        customer.phone_number = self.phone_number_var.get()
                        customer.email = self.email_var.get()
                        customer.notes = notes








                        with open("customer_data.pickle", "wb") as f: pickle.dump(customers, f)








                        with open("bookings.pickle", "rb") as f:
                            bookings = pickle.load(f)




                            updated_bookings = []




                            for booking in bookings:
                                if booking.customer.customer_id == C_customer.customer_id:
                                    booking.customer = C_customer
                                
                                updated_bookings.append(booking)




                            with open("bookings.pickle", "wb") as f: pickle.dump(updated_bookings, f)








                        self.customer_info_window.destroy()
                        customer_window.create_window(logged_user)
                        messagebox.showinfo("Customer Database", "Customer details have been changed")

    def search_customers(self, name: str, phone_number: str, dob_list: list):
        
        name = name.strip()
        phone_number = phone_number.strip()




        if name != "" and not name.isalpha():
            messagebox.showerror("Search Error", "Only letters allowed in name")
            return




        if phone_number != "" and not phone_number.isdigit():
            messagebox.showerror("Search Error", "Only numbers allowed in phone")
            return




        with open("customer_data.pickle", "rb") as f:
            customers = pickle.load(f)




        results = []




        for customer in customers:
            match = True




            # Name Check
            if name != "":
                full_name = f"{customer.firstname} {customer.surname}".lower()
                if name.lower() not in full_name:
                    match = False








            # Phone Check 
            if phone_number != "":
                
                if phone_number not in customer.phone_number:
                    match = False








            # Dob Check
            if dob_list != ["Day", "Month", "Year"]:
                day, month, year = dob_list




                dob = customer.dob  








                if day != "Day" and int(day) != dob.day:
                    match = False
                if month != "Month" and int(month) != dob.month:
                    match = False
                if year != "Year" and int(year) != dob.year:
                    match = False








            # Final Check
            if match:
                results.append(customer)
        
        # destroy existing customer buttons
        for widget in self.customer_window_frame2.winfo_children(): widget.destroy()
        
        # create new customer buttons
        y = 50
        for customer in results:
            def create_button(customer):
                Button(self.customer_window_frame2, command = lambda: self.open_customer(customer, self.logged_user), text = f"{customer.firstname} {customer.surname}", width = 68, font = ("Helvatica", 18)).pack(padx = 10, pady = 5)
           
            create_button(customer)
            y += 50
        
        if not results: messagebox.showinfo("Search", "No matching customers found")
    
    def create_customer(self, logged_user: object):
       
        self.add_customer_window = Toplevel(root)
        self.add_customer_window.geometry("375x500")
        self.add_customer_window.configure(bg = "light blue")
        self.add_customer_window.title("Add Customer")








        # Customer attribute labels
        Label(self.add_customer_window, bg = "light blue", text = "Firstname:*", width = 15, height = 2).grid(column = 0, row = 0, pady = 5, padx = 3)
        Label(self.add_customer_window, bg = "light blue", text = "Surname:*", width = 15, height = 2).grid(column = 0, row = 1, pady = 5, padx = 3)
        Label(self.add_customer_window, bg = "light blue", text = "Date of Birth:*", width = 15, height = 2).grid(column = 0, row = 2, pady = 5, padx = 3)
        Label(self.add_customer_window, bg = "light blue", text = "Phone Number:*", width = 15, height = 2).grid(column = 0, row = 3, pady = 5, padx = 3)
        Label(self.add_customer_window, bg = "light blue", text = "Email:*", width = 15, height = 2).grid(column = 0, row = 4, pady = 5, padx = 3)
        Label(self.add_customer_window, bg = "light blue", text = "Confirm Email:*", width = 15, height = 2).grid(column = 0, row = 5, pady = 5, padx = 3)
        Label(self.add_customer_window, bg = "light blue", text = "Notes:", width = 15, height = 2).grid(column = 0, row = 6, pady = 5, padx = 3)
       
        # firstname entry
        firstname_entry = Entry(self.add_customer_window, textvariable = self.firstname_cust_var, width = 35)
        firstname_entry.grid(column = 1, row = 0, pady = 5, padx = 3)
        firstname_entry.delete(0,END)








        # surname entry
        surname_entry = Entry(self.add_customer_window, textvariable = self.surname_cust_var, width = 35)
        surname_entry.grid(column = 1, row = 1, pady = 5, padx = 3)
        surname_entry.delete(0, END)








        # date of birth dropdowns
        days  =[f"{x:02}" for x in range(1, 32)]
        months = [f"{x:02}" for x in range(1, 13)]
        year = [x for x in range(int(datetime.now().year) - 100, int(datetime.now().year) + 1)][::-1]
        
        self.cb_day = ttk.Combobox(self.add_customer_window, values = days, width = 5)
        self.cb_day.set("Day")
        self.cb_day.grid(row = 2, column = 1, padx = (0, 160))
        
        self.cb_month = ttk.Combobox(self.add_customer_window, values = months, width = 10)
        self.cb_month.set("Month")
        self.cb_month.grid(row = 2, column = 1)
        
        self.cb_year = ttk.Combobox(self.add_customer_window, values = year, width = 5)
        self.cb_year.set("Year")
        self.cb_year.grid(row = 2, column = 1, padx = (160, 0))




        # phone number entry
        phone_number_entry = Entry(self.add_customer_window,textvariable = self.phone_number_cust_var, width = 35)
        phone_number_entry.grid(column = 1, row = 3, pady = 5, padx = 3)
        phone_number_entry.delete(0,END)




        # email entry
        email_entry = Entry(self.add_customer_window,textvariable = self.email_cust_var, width = 35)
        email_entry.grid(column = 1, row = 4, pady = 5, padx = 3)
        email_entry.delete(0,END)
       
        #confirm email entry
        confirm_email_entry = Entry(self.add_customer_window,textvariable = self.c_email_cust_var, width = 35)
        confirm_email_entry.grid(column = 1, row = 5, pady = 5, padx = 3)
        confirm_email_entry.delete(0,END)




        # notes text
        notes_text = Text(self.add_customer_window, height = 8, width = 27)
        notes_text.grid(column = 1, row = 6, pady = 5, padx = 3)




        ## buttons ##
        # Add customer - triggers add_customer method
        add_customer_button = Button(self.add_customer_window, text = "Add Customer", command = lambda: self.add_customer(logged_user, notes_text.get("1.0", "end-1c"), self.add_customer_window), width = 13, height = 3)
        add_customer_button.grid(column = 1, row = 7, sticky = E)




        # Return - triggers create_window method
        return_button = Button(self.add_customer_window, text = "Go Back", command = lambda: self.create_window(logged_user, add_customer_window = self.add_customer_window), width = 10, height = 2)
        return_button.grid(column = 0, row = 7,padx = 15, sticky = E)
               
    def add_customer(self, logged_user: object, notes: str, add_customer_window: Frame):
        
        date = {
            "day": self.cb_day.get(),
            "month": self.cb_month.get(),
            "year": self.cb_year.get()
        }




        customer_details = {
            "firstname": self.firstname_cust_var.get(),
            "surname" : self.surname_cust_var.get(),
            "dob" : date,
            "phone_number": self.phone_number_cust_var.get(),
            "email": self.email_cust_var.get(),
            "c_email": self.c_email_cust_var.get(),
            "notes": notes
        }
        
        # if one of the dates is missing inform user
        if self.cb_day.get() == "Day": messagebox.showerror("Day", "Choose a Day for date of birth");add_customer_window.lift(); add_customer_window.focus_force(); return
        if self.cb_month.get() == "Month": messagebox.showerror("Month", "Choose a Month for date of birth");add_customer_window.lift(); add_customer_window.focus_force(); return
        if self.cb_year.get() == "Year": messagebox.showerror("Year", "Choose a Year for date of birth");add_customer_window.lift(); add_customer_window.focus_force(); return








        with open("customer_data.pickle", "rb") as f: customers = pickle.load(f)
       
        # validate data entered and if it is right then add customer
        if Customer.validate_customer(firstname = customer_details["firstname"], surname = customer_details["surname"], dob = customer_details["dob"], phone_number = customer_details["phone_number"],email = customer_details["email"], c_email = customer_details["c_email"], window = self.add_customer_window):
            new_customer = Customer(
                                firstname = customer_details["firstname"].strip(), 
                                surname = customer_details["surname"].strip(),
                                dob = [int(customer_details["dob"]["year"]), int(customer_details["dob"]["month"]), int(customer_details["dob"]["day"])], 
                                phone_number = customer_details["phone_number"].strip(),
                                email = customer_details["email"].strip(), 
                                c_email = customer_details["c_email"].strip(),
                                notes = customer_details["notes"].strip()
                            )








            if len(customers) != 0:
                new_customer.customer_id = customers[len(customers)-1].customer_id + 1
            
            customers.append(new_customer)




            with open("customer_data.pickle", "wb") as f: pickle.dump(customers, f)




            customer_window.create_window(logged_user, add_customer_window = add_customer_window)
            messagebox.showinfo("Customer Database", "Customer has been successfully added")



class StaffWindow:
   
    def __init__(self):
        ## ----------- ##
        ## Main Frames ##
        ## ----------- ##




        self.staff_window_frame = None
        self.scroll_window_canvas = None
        self.canvas_window = None
        self.scroll_window_frame = None
        self.canvas_container  = None
        self.main_content = None
        self.scrollbar = None
        self.staff_window_frame2 = None
        self.staff_info_window = None
        self.header_frame = None
       
        self.drop_down_entry = None




        ## ----------------------- ##
        ## Viewing Staff Variables ##
        ## ----------------------- ##
        
        self.last_user = None
        self.new_profile_window = True
        self.staff_role = None
        
        self.view_working_hours_window = None
        self.services_window = None
       
        self.firstname_var = StringVar()
        self.surname_var = StringVar()
        self.DoB_var = []
        self.phone_number_var = StringVar()
        self.email_var = StringVar()
        self.postcode_var = StringVar()
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.view_services = []
        self.date_created_var = StringVar()
        self.notes_var = ""
       








        ## ------------------- ##
        ## Add Staff Variables ##
        ## ------------------- ##




        ## personal_info_window variables ##
        self.firstname_staff_var = StringVar()
        self.surname_staff_var = StringVar()
        self.DoB_day_staff_var = StringVar()
        self.DoB_month_staff_var = StringVar()
        self.DoB_year_staff_var = StringVar()








        ## contact_info_window ##
        self.phone_number_staff_var = StringVar()
        self.email_staff_var = StringVar()
        self.c_email_staff_var = StringVar()
        self.postcode_staff_var = StringVar()








        ## account_info_window ##
        self.username_staff_var = StringVar()
        self.userPassword_staff_var = StringVar()
        self.role_staff_var = StringVar()








        ## work_hours_window ##
        self.monday_start = StringVar()
        self.monday_end = StringVar()
       
        self.tuesday_start = StringVar()
        self.tuesday_end = StringVar()
       
        self.wednesday_start = StringVar()
        self.wednesday_end = StringVar()
       
        self.thursday_start = StringVar()
        self.thursday_end = StringVar()
       
        self.friday_start = StringVar()
        self.friday_end = StringVar()
       
        self.saturday_start = StringVar()
        self.saturday_end = StringVar()
       
        self.work_hours_dict = {}
        
        ## work_services_window ##
        self.first_call = True
        self.staff_services = []
        
        self.notes_staff_var = StringVar()
       
    def create_window(self, logged_user, add_staff_window = None):
        if not self.new_profile_window: self.new_profile_window = True
        
        if add_staff_window: 
            add_staff_window.destroy()
            
        if main_window.main_window_frame: main_window.main_window_frame.destroy()
        
        self.reset_variables()
        
        ## Reset Staff Window ##
        if self.header_frame: self.header_frame.destroy()
        if self.staff_window_frame: self.staff_window_frame.destroy()








        ## Display Staffs ##
        self.header_frame = Frame(root, height = 50, bg = "light blue")
        self.header_frame.pack(fill = X)








        back_button = Button(self.header_frame, text = "Go Back", command = lambda: main_window.create_window(logged_user), height = 2, width = 10)
        back_button.grid(column = 2, row = 0, padx = 20, sticky = "e")








        create_staff_button = Button(self.header_frame, text = "Create Staff", command = lambda: self.personal_info_window(logged_user), height = 2, width = 15)
        create_staff_button.grid(column = 1, row = 0, padx = 300, )








        Label(self.header_frame, bg =  "light blue", text = "Staff List", font = ("Helvatica", 18)).grid(column = 0, row = 0)








        ## Main Area ##
        self.staff_window_frame = Frame(root, bg = "light blue")
        self.staff_window_frame.pack(fill = BOTH, expand = True)








        self.main_content  = Frame(self.staff_window_frame, bg = "light blue")
        self.main_content .pack(fill = BOTH, expand = True)
       
       
        self.main_content.columnconfigure(0, weight = 1)
        self.main_content.columnconfigure(1, weight = 0)
        self.main_content.rowconfigure(0, weight = 1)
       
       
        ## Scroll Area ##
        self.canvas_container = Frame(self.main_content, bg = "light blue")
        self.canvas_container.grid(row = 0, column = 0, sticky = "nsew")
        
        
        self.scroll_window_canvas = Canvas(self.canvas_container, bg = "light blue")
        self.scroll_window_canvas.pack(side = LEFT, fill = BOTH, expand = True)








        self.scrollbar = ttk.Scrollbar(self.canvas_container, orient = VERTICAL, command = self.scroll_window_canvas.yview)
        self.scrollbar.pack(side = RIGHT, fill = Y)








        self.scroll_window_canvas.configure(yscrollcommand = self.scrollbar.set)








        self.staff_window_frame2 = Frame(self.scroll_window_canvas, bg = "light blue")
        self.canvas_window = self.scroll_window_canvas.create_window((0,0), window = self.staff_window_frame2, anchor = "nw")
        
        
        self.staff_window_frame2.bind("<Configure>", lambda e: self.scroll_window_canvas.configure(scrollregion = self.scroll_window_canvas.bbox("all")))
        self.scroll_window_canvas.bind("<Configure>",lambda e: self.scroll_window_canvas.itemconfig(self.canvas_window, width = e.width))
        
        
        ## Search Area ##
        self.search_panel = Frame(self.main_content, bg = "light blue", width = 120)
        self.search_panel.grid(row = 0, column = 1, sticky = "ns")
        self.search_panel.grid_propagate(False)
        
        
        Label(self.search_panel, text = "Search by name", bg = "light blue", font = underlined_font).pack(pady = 10)
        
        
        self.search_entry_name = Entry(self.search_panel)
        self.search_entry_name.pack(padx = 5, pady = 5)
        
        
        Label(self.search_panel, text = "Search by phone number", bg = "light blue", font = underlined_font).pack(pady = 10)
        
        
        self.search_entry_phone_number = Entry(self.search_panel)
        self.search_entry_phone_number.pack(padx = 5, pady = 5)
        
        
        Label(self.search_panel, text = "Search by DoB", bg = "light blue", font = underlined_font).pack(pady = 10)
        
        
        days  =[f"{x:02}" for x in range(1, 32)]
        months = [f"{x:02}" for x in range(1, 13)]
        year = [x for x in range(int(datetime.now().year) - 100, int(datetime.now().year) + 1)][::-1]
        
        
        self.cb_day_search = ttk.Combobox(self.search_panel, values = days, width = 8)
        self.cb_day_search.set("Day")
        self.cb_day_search.pack(pady = 5)
        
        
        self.cb_month_search = ttk.Combobox(self.search_panel, values = months, width = 8)
        self.cb_month_search.set("Month")
        self.cb_month_search.pack(pady = 5)
        
        
        self.cb_year_search = ttk.Combobox(self.search_panel, values = year, width = 8)
        self.cb_year_search.set("Year")
        self.cb_year_search.pack(pady = 5)
        
        Button(self.search_panel, text = "Search", font = ("Helvatica", 20), command = lambda: self.search_staff(name = self.search_entry_name.get(), phone_number = self.search_entry_phone_number.get(), dob_list = [self.cb_day_search.get(), self.cb_month_search.get(), self.cb_year_search.get()], logged_user = logged_user)).pack(pady = 5, side = "bottom")
        Button(self.search_panel, text = "Reset", font = ("Helvatica", 20), command = lambda: self.create_window(logged_user)).pack(pady = 5, side = "bottom")








        ## Create an ordered list of staff users based on firstname and surname
        ordered_staff_list = []




        with open("user_data.pickle", "rb") as f:
            staffs = pickle.load(f)




            ordered_staff_list = sorted(staffs, key = lambda e: f"{e.firstname} {e.surname}")




        # Turn each staff into a button from the sorted list
        y = 50
        for staff in ordered_staff_list:
            def create_button(staff):
                Button(self.staff_window_frame2, command = lambda: self.open_staff(staff, logged_user), text = f"{staff.firstname} {staff.surname}", width = 67, font = ("Helvatica", 18)).pack(padx = 10, pady = 5)
           
            create_button(staff)
            y += 50

    def open_staff(self, user: object, logged_user: object, previous_window: Frame = None):
        if self.view_working_hours_window: self.view_working_hours_window.lower()
        if self.services_window: self.services_window.lower()
        
        self.reset_variables()
            
        ## DELETING PREVIOUS WINDOW ##
        
        if self.staff_info_window: self.staff_info_window.destroy()
        if previous_window: previous_window.destroy()
       
        ## CREATING CURRENT WINDOW ##
        
        self.staff_info_window = Toplevel(root, bg = "light blue")
        self.staff_info_window.geometry("400x825")








        ## LABES ##
        
        Label(self.staff_info_window, bg = "light blue", text = f"Staff ID: {user.staff_id}", width = 15, height = 2).grid(row = 0, column = 0, columnspan = 2)
        Label(self.staff_info_window, bg = "light blue", text = "Firstname:*", width = 15, height = 2).grid(column = 0, row = 1, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Surname:*", width = 15, height = 2).grid(column = 0, row = 2, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Date of Birth:*", width = 15, height = 2).grid(column = 0, row = 3, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Phone Number:*", width = 15, height = 2).grid(column = 0, row = 4, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Email:*", width = 15, height = 2).grid(column = 0, row = 5, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Postcode:*", width = 15, height = 2).grid(column = 0, row = 6, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Username:*", width = 15, height = 2).grid(column = 0, row = 7, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Password:*", width = 15, height = 2).grid(column = 0, row = 8, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Role:*", width = 15, height = 2).grid(column = 0, row = 9, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Working Hours:*", width = 15, height = 2).grid(column = 0, row = 10, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Services:*", width = 15, height = 2).grid(column = 0, row = 11, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Date Created:*", width = 15, height = 2).grid(column = 0, row = 12, pady = 5, padx = 3)
        Label(self.staff_info_window, bg = "light blue", text = "Notes:*", width = 15, height = 2).grid(column = 0, row = 13, pady = 5, padx = 3)








        ## ENTRIES ##
        
        # Firstname
        firstname_entry = Entry(self.staff_info_window,textvariable = self.firstname_var, width = 35)
        firstname_entry.grid(column = 1, row = 1, pady = 5, padx = 3, columnspan = 3)
        
        # Surname
        surname_entry = Entry(self.staff_info_window,textvariable = self.surname_var, width = 35)
        surname_entry.grid(column = 1, row = 2, pady = 5, padx = 3)








        # Date of Birth
        days  =[f"{x:02}" for x in range(1, 32)]
        months = [f"{x:02}" for x in range(1, 13)]
        year = [x for x in range(int(datetime.now().year) - 100, int(datetime.now().year) + 1)][::-1]
        
        self.cb_day = ttk.Combobox(self.staff_info_window, values = days, width = 5)
        self.cb_day.set(user.dob.strftime("%d,%m,%Y").split(",")[0])
        self.cb_day.grid(row = 3, column = 1, padx = (0, 160))
        
        self.cb_month = ttk.Combobox(self.staff_info_window, values = months, width = 10)
        self.cb_month.set(user.dob.strftime("%d,%m,%Y").split(",")[1])
        self.cb_month.grid(row = 3, column = 1)
        
        self.cb_year = ttk.Combobox(self.staff_info_window, values = year, width = 5)
        self.cb_year.set(user.dob.strftime("%d,%m,%Y").split(",")[2])
        self.cb_year.grid(row = 3, column = 1, padx = (160, 0))








        # Phone number
        phone_number_entry = Entry(self.staff_info_window,textvariable = self.phone_number_var, width = 35)
        phone_number_entry.grid(column = 1, row = 4, pady = 5, padx = 3, columnspan = 3)




        # Email
        email_entry = Entry(self.staff_info_window,textvariable = self.email_var, width = 35)
        email_entry.grid(column = 1, row = 5, pady = 5, padx = 3, columnspan = 3)
        
        # Postcode
        postcode_entry = Entry(self.staff_info_window,textvariable = self.postcode_var, width = 35)
        postcode_entry.grid(column = 1, row = 6, pady = 5, padx = 3, columnspan = 3)
        
        # Username
        username_entry = Entry(self.staff_info_window,textvariable = self.username_var, width = 35)
        username_entry.grid(column = 1, row = 7, pady = 5, padx = 3, columnspan = 3)








        # Password
        password_entry = Entry(self.staff_info_window,textvariable = self.password_var, width = 35)
        password_entry.grid(column = 1, row = 8, pady = 5, padx = 3, columnspan = 3)
        
        # Sets role based on staff attributes
        self.drop_down_entry = ttk.Combobox(self.staff_info_window, values = ["Admin", "Staff", "Both"], width = 30, textvariable = self.role_staff_var)
        self.drop_down_entry.grid(column = 1, row = 9, padx = 3)
        
        if not self.new_profile_window and self.staff_role:
            self.drop_down_entry.set(self.staff_role)
        
        if self.new_profile_window:
            self.new_profile_window = False
            if user.isAdmin and user.isStaff:
                self.drop_down_entry.set("Both")
            elif user.isAdmin == True and user.isStaff == False:
                self.drop_down_entry.set("Admin")
            else:
                self.drop_down_entry.set("Staff")








        # View staff working hours
        Button(self.staff_info_window, text = "View", width = 15, height = 2, command = lambda: self.view_working_hours()).grid(column = 1, row = 10, pady = 5, padx = 3, columnspan = 3)
        
        # View staff services
        Button(self.staff_info_window, text = "View", width = 15, height = 2, command = lambda: self.services(user)).grid(column = 1, row = 11, pady = 5, padx = 3, columnspan = 3)








        # Date created
        date_created_label = Label(self.staff_info_window, textvariable = self.date_created_var, width = 30, bg = "light blue")
        date_created_label.grid(column = 1, row = 12, pady = 5, padx = 3, columnspan = 3)




        
        # - notes -
        words = user.notes.split()
        notes_lines = []
        
        for i in range(0, len(words), 5):
            notes_lines.append(" ".join(words[i:i + 5]))
        notes_str = "\n".join(notes_lines)




        num_lines = max(1, len(notes_lines))








        # Notes
        notes_text = Text(self.staff_info_window, height = num_lines, width = 27)
        notes_text.insert("1.0", notes_str)
        notes_text.grid(column = 1, row = 13, pady = 5, padx = 3, columnspan = 3)








        # Confirm staff changes
        change_staff_button = Button(self.staff_info_window,command = lambda: self.confirm_changes(C_user = user, logged_user = logged_user, notes = notes_text.get("1.0", "end-1c")), height = 3, width = 15, text = "Confirm Changes")
        change_staff_button.grid(column = 1, row = 14,padx = 10, pady = 10, columnspan = 3)








        # if staff ID does not equal to 1 (Main Admin) add a "Delete Staff" button 
        if user.staff_id != 1:
            delete_customer_button = Button(self.staff_info_window,command = lambda: self.delete_staff(user, logged_user), text = "Delete Staff", height = 3, width = 15)
            delete_customer_button.grid(column = 0, row = 14, padx = 10, pady = 10)
        
        ## SETTING VARIABLES ## 
        
        # - firstname - 
        if self.firstname_var.get() == "": 
            self.firstname_var.set(user.firstname)
        else:
            self.firstname_var.set(self.firstname_var.get())
        
        # - surname - 
        if self.surname_var.get() == "": 
            self.surname_var.set(user.surname)
        else:
            self.surname_var.set(self.surname_var.get())








        # - phone number -
        if self.phone_number_var.get() == "": 
            self.phone_number_var.set(user.phone_number)
        else:
            self.phone_number_var.set(self.phone_number_var.get())




        # - email - 
        if self.email_var.get() == "": 
            self.email_var.set(user.email)
        else:
            self.email_var.set(self.email_var.get())
        
        # - email - 
        if self.postcode_var.get() == "": 
            self.postcode_var.set(user.postcode)
        else:
            self.postcode_var.set(self.postcode_var.get())
        
        # - username - 
        if self.username_var.get() == "": 
            self.username_var.set(user.username)
        else:
            self.username_var.set(self.username_var.get())




        # - password - 
        if self.password_var.get() == "": 
            self.password_var.set(user.staff_password)
        else:
            self.password_var.set(self.password_var.get())




        # - Monday hours - 
        if self.monday_start.get() or self.monday_end.get():
            pass
        elif len(user.working_hours["Monday"]) != 0:
            self.monday_start.set(user.working_hours["Monday"][0])
            self.monday_end.set(user.working_hours["Monday"][1])
        
        # - Tuesday hours - 
        if self.tuesday_start.get() or self.tuesday_end.get():
            pass    
        elif len(user.working_hours["Tuesday"]) != 0:
            self.tuesday_start.set(user.working_hours["Tuesday"][0])
            self.tuesday_end.set(user.working_hours["Tuesday"][1])
        
        # - Wednesday hours - 
        if self.wednesday_start.get() or self.wednesday_end.get():
            pass
        elif len(user.working_hours["Wednesday"]) != 0:
            self.wednesday_start.set(user.working_hours["Wednesday"][0])
            self.wednesday_end.set(user.working_hours["Wednesday"][1])
        
        # - Thursday hours - 
        if self.thursday_start.get() or self.thursday_end.get():
            pass
        elif len(user.working_hours["Thursday"]) != 0:
            self.thursday_start.set(user.working_hours["Thursday"][0])
            self.thursday_end.set(user.working_hours["Thursday"][1])
        
        # - Firday hours - 
        if self.friday_start.get() or self.friday_end.get():
            pass
        elif len(user.working_hours["Friday"]) != 0:
            self.friday_start.set(user.working_hours["Friday"][0])
            self.friday_end.set(user.working_hours["Friday"][1])
        
        # - Saturday hours - 
        if self.saturday_start.get() or self.saturday_end.get():
            pass
        elif len(user.working_hours["Saturday"]) != 0:
            self.saturday_start.set(user.working_hours["Saturday"][0])
            self.saturday_end.set(user.working_hours["Saturday"][1])
        
        # - services - 
        if self.first_call:
            self.view_services = user.services
            self.first_call = False
        else:
            self.view_services = self.view_services
        
        # - date created -
        if self.date_created_var.get() == "": 
            self.date_created_var.set(user.date_created[0:len(user.date_created)-1])
        else:
            self.date_created_var.set(self.date_created_var.get())

    def view_working_hours(self):
        
        # set up window
        if not self.view_working_hours_window:
            self.view_working_hours_window = Toplevel(root)
            self.view_working_hours_window.geometry("550x450")
            self.view_working_hours_window.title("Working Hours and Services")
            self.view_working_hours_window.configure(bg = "light blue")
        else:
            self.view_working_hours_window.lift()




        ## Labels
        Label(self.view_working_hours_window,bg = "light blue", text = "Work Information(24 hour clock)", width = 25, height = 2, font = ("Helvatica", 20)).grid(column = 0, row = 0, columnspan = 4)








        ## MONDAY ##
       
        # Labels
        Label(self.view_working_hours_window,bg = "light blue", text = "Monday", width = 15, height = 2, font = underlined_font).grid(column = 0, row = 1)
        Label(self.view_working_hours_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 0, row = 2)
        Label(self.view_working_hours_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 1, row = 2)








        # Entries
        monday_entry_start = Entry(self.view_working_hours_window, width = 10, textvariable = self.monday_start)
        monday_entry_start.grid(column = 0, row = 3)








        monday_entry_end = Entry(self.view_working_hours_window, width = 10, textvariable = self.monday_end)
        monday_entry_end.grid(column = 1, row = 3)
        
            
        ## TUESDAY ##




        # Labels
        Label(self.view_working_hours_window,bg = "light blue", text = "Tuesday", width = 15, height = 2, font = underlined_font).grid(column = 0, row = 4)
        Label(self.view_working_hours_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 0, row = 5)
        Label(self.view_working_hours_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 1, row = 5)
       
        # Entries
        tuesday_entry_start = Entry(self.view_working_hours_window, width = 10,textvariable = self.tuesday_start)
        tuesday_entry_start.grid(column = 0, row = 6)








        tuesday_entry_end = Entry(self.view_working_hours_window, width = 10, textvariable = self.tuesday_end)
        tuesday_entry_end.grid(column = 1, row = 6)








        ## WEDNESDAY ##




        # Labels
        Label(self.view_working_hours_window,bg = "light blue", text = "Wednesday", width = 15, height = 2, font = underlined_font).grid(column = 0, row = 7)
        Label(self.view_working_hours_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 0, row = 8)
        Label(self.view_working_hours_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 1, row = 8)
       
        # Entries
        wednesday_entry_start = Entry(self.view_working_hours_window, width = 10, textvariable = self.wednesday_start)
        wednesday_entry_start.grid(column = 0, row = 9)
        
        wednesday_entry_end = Entry(self.view_working_hours_window, width = 10, textvariable = self.wednesday_end)
        wednesday_entry_end.grid(column = 1, row = 9)








        ## THURSDAY ##




        # Labels
        Label(self.view_working_hours_window,bg = "light blue", text = "Thursday", width = 15, height = 2, font = underlined_font).grid(column = 3, row = 1)
        Label(self.view_working_hours_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 3, row = 2)
        Label(self.view_working_hours_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 4, row = 2)








        # Entries
        thursday_entry_start = Entry(self.view_working_hours_window, width = 10, textvariable = self.thursday_start)
        thursday_entry_start.grid(column = 3, row = 3)
        
        thursday_entry_end = Entry(self.view_working_hours_window, width = 10, textvariable = self.thursday_end)
        thursday_entry_end.grid(column = 4, row = 3)








        ## FRIDAY ##




        # Labels
        Label(self.view_working_hours_window,bg = "light blue", text = "Friday", width = 15, height = 2, font = underlined_font).grid(column = 3, row = 4)
        Label(self.view_working_hours_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 3, row = 5)
        Label(self.view_working_hours_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 4, row = 5)
       
        # Entries
        friday_entry_start = Entry(self.view_working_hours_window, width = 10, textvariable = self.friday_start)
        friday_entry_start.grid(column = 3, row = 6)
        
        friday_entry_end = Entry(self.view_working_hours_window, width = 10, textvariable = self.friday_end)
        friday_entry_end.grid(column = 4, row = 6)
        
        
        ## SATURDAY ##




        # Labels
        Label(self.view_working_hours_window,bg = "light blue", text = "Saturday", width = 15, height = 2, font = underlined_font).grid(column = 3, row = 7)
        Label(self.view_working_hours_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 3, row = 8)
        Label(self.view_working_hours_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 4, row = 8)
       
        # Entries
        saturday_entry_start = Entry(self.view_working_hours_window, width = 10, textvariable = self.saturday_start)
        saturday_entry_start.grid(column = 3, row = 9)
        
        
        saturday_entry_end = Entry(self.view_working_hours_window, width = 10, textvariable = self.saturday_end)
        saturday_entry_end.grid(column = 4, row = 9)
                
    def services(self, user):
        
        self.staff_role = self.role_staff_var.get()
        
        # set up services window
        if not self.services_window:
            self.services_window = Toplevel(root)
            self.services_window.title("Services for current staff")
            self.services_window.geometry("525x500")
            self.services_window.config(bg = "light blue")
        else:
            self.services_window.lift()








        core_hair_services = ["Haircut", "Hair trim", "Wash and blow-dry", "Restyle", "Fringe trim"]
        colouring_services = ["Full hair dye", "Root touch-up", "Highlights", "Balayage", "Toner application"]
        grooming_extra_services = ["Beard trim", "Beard shaping", "Beard colouring", "Hot towel shave"]
        treatment_services = ["Deep conditioning treatment", "Hair mask treatment", "Keratin treatment"]








        categories = [
            ("Core Hair Services",   core_hair_services),
            ("Colouring Services",   colouring_services),
            ("Grooming & Extras",    grooming_extra_services),
            ("Treatment Services",   treatment_services),
        ]
            
            
        Label(self.services_window, text = "Services", bg = "light blue", font = ("Helvatica", 24)).grid(row = 0, column = 0, columnspan = 2, pady = 10)








        # Loop through each category and if service exists in staff services list turn the check button on








        # CATEGORY 1 #
        for i, treatment in enumerate(categories[0][1]):
            
            Label(self.services_window, text = categories[0][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 1, column = 0, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):
                
                cat_1_cb = Checkbutton(self.services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment, user))
                cat_1_cb.grid(row = i + 2, column = 0, pady = (0, 5), padx = (30, 0), sticky = W)
                
                if treatment in self.view_services: cat_1_cb.select()
                
            create_checkbox(treatment)
            
        # CATEGORY 2 #
        for i, treatment in enumerate(categories[1][1]):
            
            Label(self.services_window, text = categories[1][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 1, column = 1, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):
                
                cat_2_cb = Checkbutton(self.services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment, user))
                cat_2_cb.grid(row = i + 2, column = 1, pady = (0, 5), padx = (30, 0), sticky = W)
            
                if treatment in self.view_services: cat_2_cb.select()
                
            create_checkbox(treatment)
            
        # CATEGORY 3 #
        for i, treatment in enumerate(categories[2][1]):
            
            Label(self.services_window, text = categories[2][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 7, column = 0, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):




                cat_3_cb = Checkbutton(self.services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment, user))
                cat_3_cb.grid(row = i + 9, column = 0, pady = (0, 5), padx = (30, 0), sticky = W)
            
                if treatment in self.view_services: cat_3_cb.select()
            
            create_checkbox(treatment)




        # CATEGORY 4 #
        for i, treatment in enumerate(categories[3][1]):
            
            Label(self.services_window, text = categories[3][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 7, column = 1, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):




                cat_4_cb = Checkbutton(self.services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment, user))
                cat_4_cb.grid(row = i + 9, column = 1, pady = (0, 5), padx = (30, 0), sticky = W)
                
                if treatment in self.view_services: cat_4_cb.select()
                
            create_checkbox(treatment)
         
        Button(self.services_window, text = "Confirm",font = ("Helvatica", 18), command = lambda: self.staff_info_window.lift()).grid(column = 1, row = 13)

    def delete_staff(self, D_staff, logged_user):
       
        if not messagebox.askyesno("Confirmation", "Delete Staff account?"):
            self.staff_info_window.lift()
            self.staff_info_window.focus_force()
            return




        staffs_list = []
        with open("user_data.pickle", "rb") as f:
            staffs = pickle.load(f)




            for staff in staffs:
                if staff.staff_id != D_staff.staff_id:
                    staffs_list.append(staff)




                
        with open("bookings.pickle","rb") as f:
            bookings = pickle.load(f)
            updated_bookings_list = []
            
            for booking in bookings:
                if booking.staff.staff_id != D_staff.staff_id:
                    updated_bookings_list.apend(booking)
            
            for month in Booking.bookings_dict:
                for day in Booking.bookings_dict[month]:
                    for slot in Booking.bookings_dict[month][day]:
                        updated_slot_booking = []
                        for booking in Booking.bookings_dict[month][day][slot]:
                            if booking.staff.staff_id != D_staff.staff_id:
                                
                                updated_slot_booking.append(booking)
                                
                        Booking.bookings_dict[month][day][slot] = updated_slot_booking
            
            with open("bookings.pickle", "wb") as f: pickle.dump(updated_bookings_list, f)
           
        with open("user_data.pickle", "wb") as f: pickle.dump(staffs_list, f)
       
        self.staff_info_window.destroy()
        messagebox.showinfo("Staff Database", "Staff has been successfully deleted")
        staff_window.create_window(logged_user)

    def confirm_changes(self, C_user: object, logged_user: object, notes: str):
        self.first_call = True
        
        if self.view_working_hours_window: 
            self.view_working_hours_window.destroy()
            self.view_working_hours_window = None
        if self.services_window: 
            self.services_window.destroy()
            self.services_window = None
        
        date = {
            "day": self.cb_day.get(),
            "month": self.cb_month.get(),
            "year": self.cb_year.get()
            }
        
        # check if data in firtsname, surname and date of birth entries is valid
        if not User.validate_personal_info(firstname = self.firstname_var.get(), surname = self.surname_var.get(), dob = date, window = self.staff_info_window, ID = C_user.staff_id):
            return
        
        # check if data in email, phone number and postcode entries is valid
        if not User.validate_contact_info(email = self.email_var.get(), c_email = self.email_var.get(), phone_number = self.phone_number_var.get(), postcode = self.postcode_var.get(), window = self.staff_info_window, ID = C_user.staff_id):
            return
        
        # check if username or password are empty
        if self.username_var.get() != "" and self.password_var.get() != "":
            # check if data in username and password entries is valid
            if not User.validate_account_info(username = self.username_var.get(), password = self.password_var.get(), role = self.drop_down_entry.get(), window = self.staff_info_window, exists = True):
                return
        elif self.username_var.get() == "" and self.password_var.get() == "":
            self.staff_info_window.lift()
            self.staff_info_window.focus_force()
            messagebox.showerror("Error", "Username or Password cannot be empty")
            return
        
    
        self.work_hours_dict = {
            "Monday": [self.monday_start.get(), self.monday_end.get()],
            "Tuesday": [self.tuesday_start.get(), self.tuesday_end.get()],
            "Wednesday": [self.wednesday_start.get(), self.wednesday_end.get()],
            "Thursday": [self.thursday_start.get(), self.thursday_end.get()],
            "Friday": [self.friday_start.get(), self.friday_end.get()],
            "Saturday": [self.saturday_start.get(), self.saturday_end.get()]
        }
        
        # check if work hours is valid  
        if not User.validate_work_hours(work_hours_dict = self.work_hours_dict, role = self.role_staff_var.get(), window = self.staff_info_window):
            return
        
        # check if number of services for the staff isvalid
        if not User.validate_work_services(services = self.view_services, role = self.role_staff_var.get(), window = self.staff_info_window):
            return








        # checks notes for staff
        if not User.validate_notes_info(notes = notes, window = self.staff_info_window):
            return




        with open("user_data.pickle", "rb") as f:
            users = pickle.load(f)




            for user in users:
                if user.staff_id == C_user.staff_id:
                    user.firstname = self.firstname_var.get().strip()
                    user.surname = self.surname_var.get().strip()
                    user.dob = datetime(int(date["year"]), int(date["month"]), int(date["day"]))
                    user.phone_number = self.phone_number_var.get().strip()
                    user.email = self.email_var.get().strip()
                    user.postcode = self.postcode_var.get().strip()
                    user.username = self.username_var.get().strip()
                    user.staff_password = self.password_var.get().strip()
                    user.working_hours = self.work_hours_dict
                    user.services = self.view_services
                    user.notes = notes
                    
                    if self.role_staff_var.get() == "Both":
                        user.isStaff = True
                        user.isAdmin = True
                    elif self.role_staff_var.get() == "Admin":
                        user.isStaff = False
                        user.isAdmin = True
                    elif self.role_staff_var.get() == "Staff":
                        user.isStaff = True
                        user.isAdmin = False
       
        with open("user_data.pickle", "wb") as f: pickle.dump(users, f)








        self.staff_info_window.destroy()
        self.reset_variables()
        staff_window.create_window(logged_user)
        messagebox.showinfo("Staff Database", "Staff account has been successfully updated")

    def search_staff(self, name: str, phone_number: str, dob_list: list, logged_user):
        
        name = name.strip()
        phone_number = phone_number.strip()
        
        if name != "" and not name.isalpha():
            if not name.isalpha():
                messagebox.showerror("Search Error", "Only letters allowed in name")
                return
            
        if phone_number!= "" and not phone_number.isdigit():
            messagebox.showerror("Search Error", "Only numbers allowed in phone")
            return
        
        with open("user_data.pickle", "rb") as f:
            users = pickle.load(f)




        results = []




        for user in users:
            match = True








            # Name Check
            if name != "":
                full_name = f"{user.firstname} {user.surname}".lower()
                if name.lower() not in full_name:
                    match = False




            # Phone Check
            if phone_number != "":
                if phone_number not in user.phone_number:
                    match = False




            # Dob Check
            if dob_list != ["Day", "Month", "Year"]:
                day, month, year = dob_list




                dob = user.dob




                if day != "Day" and int(day) != dob.day:
                    match = False
                if month != "Month" and int(month) != dob.month:
                    match = False
                if year != "Year" and int(year) != dob.year:
                    match = False




            # Final Check
            if match:
                results.append(user)
        
        # destroy existing staff buttons
        for widget in self.staff_window_frame2.winfo_children(): widget.destroy()
        
        # create new staff buttons
        y = 50
        for user in results:
            def create_button(user):
                Button(self.staff_window_frame2, command = lambda: self.open_staff(user, logged_user), text = f"{user.firstname} {user.surname}", width = 68, font = ("Helvatica", 18)).pack(padx = 10, pady = 5)
           
            create_button(user)
            y += 50
        
        # if nothing found return
        if not results: messagebox.showinfo("Search", "No matching users found")

    def personal_info_window(self, logged_user, previous_window = None, date = ["Day", "Month", "Year"]):
       
        if previous_window: previous_window.destroy()




        # set up window
        personal_staff_window = Toplevel(root)
        personal_staff_window.geometry("415x275")
        personal_staff_window.title("Personal Information")
        personal_staff_window.configure(bg = "light blue")
        
        ## Labels ##
        Label(personal_staff_window,bg = "light blue", text = "Personal Information", width = 20, height = 2, font = ("Helvatica", 20)).grid(column = 0, row = 0, columnspan = 4)








        Label(personal_staff_window,bg = "light blue", text = "Firstname:*", width = 15, height = 2).grid(column = 0, row = 1, pady = 5, padx = 3)
        Label(personal_staff_window,bg = "light blue", text = "Surname:*", width = 15, height = 2).grid(column = 0, row = 2, pady = 5, padx = 3)
        Label(personal_staff_window,bg = "light blue", text = "Date of Birth (DD/MM/YYYY):*", width = 25, height = 2).grid(column = 0, row = 3, pady = 5, padx = 3)








        # firstname
        firstname_entry = Entry(personal_staff_window, textvariable = self.firstname_staff_var, width = 35)
        firstname_entry.grid(column = 1, row = 1, pady = 5, padx = 3, columnspan = 3)
        firstname_entry_value = firstname_entry.get()
        firstname_entry.delete(0, END)
        firstname_entry.insert(0, firstname_entry_value)
        
        # surname
        surname_entry = Entry(personal_staff_window, textvariable = self.surname_staff_var, width = 35)
        surname_entry.grid(column = 1, row = 2, pady = 5, padx = 3, columnspan = 3)
        surname_entry_value = surname_entry.get()
        surname_entry.delete(0, END)
        surname_entry.insert(0, surname_entry_value)








        # date of birth
        days  =[f"{x:02}" for x in range(1, 32)]
        months = [f"{x:02}" for x in range(1, 13)]
        year = [x for x in range(int(datetime.now().year) - 100, int(datetime.now().year) + 1)][::-1]
        
        self.cb_day = ttk.Combobox(personal_staff_window, values = days, width = 5)
        self.cb_day.set(date[0])
        self.cb_day.grid(row = 3, column = 1, padx = (0, 160))
        
        self.cb_month = ttk.Combobox(personal_staff_window, values = months, width = 10)
        self.cb_month.set(date[1])
        self.cb_month.grid(row = 3, column = 1)
        
        self.cb_year = ttk.Combobox(personal_staff_window, values = year, width = 5)
        self.cb_year.set(date[2])
        self.cb_year.grid(row = 3, column = 1, padx = (160, 0))








        ## Buttons 
        next_section_button = Button(personal_staff_window, text = "Next Section", command = lambda: self.contact_info_window(previous_window = personal_staff_window, logged = logged_user), height = 2, width = 10)
        next_section_button.grid(column = 1, row = 4, padx = 15, sticky = E)
       
        return_button = Button(personal_staff_window, text = "Go Back", command = lambda: self.create_window(logged_user = logged_user, add_staff_window = personal_staff_window), width = 10, height = 2)
        return_button.grid(column = 0, row = 4, padx = 15, sticky = E)
       
    def contact_info_window(self, previous_window, logged):
        
        self.date = {
            "day": self.cb_day.get(),
            "month": self.cb_month.get(),
            "year": self.cb_year.get()
            }




        # checks if previous data is correct(firstname, surname, date of birth)
        if not User.validate_personal_info(firstname = self.firstname_staff_var.get(), surname = self.surname_staff_var.get(), dob = self.date, window = previous_window):
            return
        else:
            # set up window
            if previous_window: previous_window.destroy()
            contact_staff_window = Toplevel(root)
            contact_staff_window.geometry("375x315")
            contact_staff_window.title("Contact Information")
            contact_staff_window.configure(bg = "light blue")




        ## Labels ##
        Label(contact_staff_window,bg = "light blue", text = "Contact Information", width = 15, height = 2, font = ("Helvatica", 20)).grid(column = 0, row = 0, columnspan = 2)








        Label(contact_staff_window,bg = "light blue", text = "Email:*", width = 15, height = 2).grid(column = 0, row = 1, pady = 5, padx = 3)
        Label(contact_staff_window,bg = "light blue", text = "Confirm Email:*", width = 15, height = 2).grid(column = 0, row = 2, pady = 5, padx = 3)
        Label(contact_staff_window,bg = "light blue", text = "Phone Number:*", width = 15, height = 2).grid(column = 0, row = 3, pady = 5, padx = 3)
        Label(contact_staff_window,bg = "light blue", text = "Postcode:*", width = 15, height = 2).grid(column = 0, row = 4, pady = 5, padx = 3)








        ## Entries ##




        # email
        email_entry = Entry(contact_staff_window, textvariable = self.email_staff_var, width = 35)
        email_entry.grid(column = 1, row = 1, pady = 5, padx = 3)
        email_entry_value = email_entry.get()
        email_entry.delete(0, END)
        email_entry.insert(0, email_entry_value)




        # c_email
        c_email_entry = Entry(contact_staff_window, textvariable = self.c_email_staff_var, width = 35)
        c_email_entry.grid(column = 1, row = 2, pady = 5, padx = 3)
        c_email_entry_value = c_email_entry.get()
        c_email_entry.delete(0, END)
        c_email_entry.insert(0, c_email_entry_value)




        # phone number
        phone_number_entry = Entry(contact_staff_window, textvariable = self.phone_number_staff_var, width = 35)
        phone_number_entry.grid(column = 1, row = 3, pady = 5, padx = 3)
        phone_number_entry_value = phone_number_entry.get()
        phone_number_entry.delete(0, END)
        phone_number_entry.insert(0, phone_number_entry_value)




        # postcode
        postcode_entry = Entry(contact_staff_window, textvariable = self.postcode_staff_var, width = 35)
        postcode_entry.grid(column = 1, row = 4, pady = 5, padx = 3)
        postcode_entry_value = postcode_entry.get()
        postcode_entry.delete(0, END)
        postcode_entry.insert(0, postcode_entry_value)




        # Buttons
        next_section_button = Button(contact_staff_window, text = "Next Section", command = lambda: self.account_info_window(contact_staff_window, logged), height = 2, width = 10)
        next_section_button.grid(column = 1, row = 5, padx = 15, sticky = E)
       
    
        return_button = Button(contact_staff_window, text = "Go Back", command = lambda: self.personal_info_window(logged, previous_window = contact_staff_window, date = [self.date["day"], self.date["month"], self.date["year"]]), width = 10, height = 2)
        return_button.grid(column = 0, row = 5, padx = 15, sticky = E)

    def account_info_window(self, previous_window, logged):
        
        # check previous data is correct( email, phone number, postcode)
        if not User.validate_contact_info(email = self.email_staff_var.get(), c_email = self.c_email_staff_var.get(), phone_number = self.phone_number_staff_var.get(), postcode = self.postcode_staff_var.get(), window = previous_window):
            return
        else:
            # set uo window
            if previous_window: previous_window.destroy()
            account_staff_window = Toplevel(root)
            account_staff_window.geometry("375x275")
            account_staff_window.title("Account Information")
            account_staff_window.configure(bg = "light blue")
            
        ## Labels
        Label(account_staff_window,bg = "light blue", text = "Account Information", width = 20, height = 2, font = ("Helvatica", 20)).grid(column = 0, row = 0, columnspan = 2)








        Label(account_staff_window,bg = "light blue", text = "Username:*", width = 15, height = 2).grid(column = 0, row = 1, pady = 5, padx = 3)
        Label(account_staff_window,bg = "light blue", text = "Password:*", width = 15, height = 2).grid(column = 0, row = 2, pady = 5, padx = 3)
        Label(account_staff_window,bg = "light blue", text = "Account Level:*", width = 15, height = 2).grid(column = 0, row = 3, pady = 5, padx = 3)








        ## Entries ##
        
        # Username
        username_entry = Entry(account_staff_window, textvariable = self.username_staff_var, width = 35)
        username_entry.grid(column = 1, row = 1, pady = 5, padx = 3)
        username_entry_value = username_entry.get()
        username_entry.delete(0, END)
        username_entry.insert(0, username_entry_value)




        # Password
        password_entry = Entry(account_staff_window, textvariable = self.userPassword_staff_var, width = 35)
        password_entry.grid(column = 1, row = 2, pady = 5, padx = 3)
        password_entry_value = password_entry.get()
        password_entry.delete(0, END)
        password_entry.insert(0, password_entry_value)
        
        # Role
        self.drop_down_entry = ttk.Combobox(account_staff_window, values = ["Admin", "Staff", "Both"], width = 30, textvariable = self.role_staff_var)
        self.drop_down_entry.set("Choose role")
        self.drop_down_entry.grid(column = 1, row = 3, padx = 3)




        # Buttons
        next_section_button = Button(account_staff_window, text = "Next Section", command = lambda: self.work_hours_window(previous_window = account_staff_window, logged = logged), height = 2, width = 10)
        next_section_button.grid(column = 1, row = 4, padx = 15, sticky = E)
       
       
        return_button = Button(account_staff_window, text = "Go Back", command = lambda: self.contact_info_window(logged = logged, previous_window = account_staff_window), width = 10, height = 2)
        return_button.grid(column = 0, row = 4, padx = 15, sticky = E)
   
    def work_hours_window(self, previous_window, logged):
        
        # check previous data(username, password, role)
        if not User.validate_account_info(username = self.username_staff_var.get(), password = self.userPassword_staff_var.get(), role = self.drop_down_entry.get(), window = previous_window):
            return
        else:
            if previous_window: previous_window.destroy()
            work_info_window = Toplevel(root)
            work_info_window.geometry("560x450")
            work_info_window.title("Working Hours")
            work_info_window.configure(bg = "light blue")




        ## Labels
        Label(work_info_window,bg = "light blue", text = "Work Information(24 hour clock)", width = 25, height = 2, font = ("Helvatica", 20)).grid(column = 0, row = 0, columnspan = 4, padx = (50, 0))
        
        
        ## MONDAY ##
        
        # Labels
        Label(work_info_window,bg = "light blue", text = "Monday", width = 15, height = 2, font = underlined_font).grid(column = 0, row = 1)
        Label(work_info_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 0, row = 2)
        Label(work_info_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 1, row = 2)




        # Entries
        monday_entry_start = Entry(work_info_window, width = 10, textvariable = self.monday_start)
        monday_entry_start.grid(column = 0, row = 3)
        monday_entry_start_value = monday_entry_start.get()
        monday_entry_start.delete(0, END)
        monday_entry_start.insert(0, monday_entry_start_value)




        monday_entry_end = Entry(work_info_window, width = 10, textvariable = self.monday_end)
        monday_entry_end.grid(column = 1, row = 3)
        monday_entry_end_value = monday_entry_end.get()
        monday_entry_end.delete(0, END)
        monday_entry_end.insert(0, monday_entry_end_value)








        ## TUESDAY ##




        # Labels
        Label(work_info_window,bg = "light blue", text = "Tuesday", width = 15, height = 2, font = underlined_font).grid(column = 0, row = 4)
        Label(work_info_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 0, row = 5)
        Label(work_info_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 1, row = 5)
       
        # Entries
        tuesday_entry_start = Entry(work_info_window, width = 10,textvariable = self.tuesday_start)
        tuesday_entry_start.grid(column = 0, row = 6)
        tuesday_entry_start_value = tuesday_entry_start.get()
        tuesday_entry_start.delete(0, END)
        tuesday_entry_start.insert(0, tuesday_entry_start_value)








        tuesday_entry_end = Entry(work_info_window, width = 10, textvariable = self.tuesday_end)
        tuesday_entry_end.grid(column = 1, row = 6)
        tuesday_entry_end_value = tuesday_entry_end.get()
        tuesday_entry_start.delete(0, END)
        tuesday_entry_start.insert(0, tuesday_entry_end_value)








        ## WEDNESDAY ##




        # Labels
        Label(work_info_window,bg = "light blue", text = "Wednesday", width = 15, height = 2, font = underlined_font).grid(column = 0, row = 7)
        Label(work_info_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 0, row = 8)
        Label(work_info_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 1, row = 8)
       
        # Entries
        wednesday_entry_start = Entry(work_info_window, width = 10, textvariable = self.wednesday_start)
        wednesday_entry_start.grid(column = 0, row = 9)
        wednesday_entry_start_value = wednesday_entry_start.get()
        wednesday_entry_start.delete(0, END)
        wednesday_entry_start.insert(0, wednesday_entry_start_value)




        wednesday_entry_end = Entry(work_info_window, width = 10, textvariable = self.wednesday_end)
        wednesday_entry_end.grid(column = 1, row = 9)
        wednesday_entry_end_value = wednesday_entry_end.get()
        wednesday_entry_start.delete(0, END)
        wednesday_entry_start.insert(0, wednesday_entry_end_value)








        ## THURSDAY ##




        # Labels
        Label(work_info_window,bg = "light blue", text = "Thursday", width = 15, height = 2, font = underlined_font).grid(column = 3, row = 1)
        Label(work_info_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 3, row = 2)
        Label(work_info_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 4, row = 2)
       
        # Entries
        thursday_entry_start = Entry(work_info_window, width = 10, textvariable = self.thursday_start)
        thursday_entry_start.grid(column = 3, row = 3)
        thursday_entry_start_value = thursday_entry_start.get()
        thursday_entry_start.delete(0, END)
        thursday_entry_start.insert(0, thursday_entry_start_value)




        thursday_entry_end = Entry(work_info_window, width = 10, textvariable = self.thursday_end)
        thursday_entry_end.grid(column = 4, row = 3)
        thursday_entry_end_value = thursday_entry_end.get()
        thursday_entry_end.delete(0, END)
        thursday_entry_end.insert(0, thursday_entry_end_value)








        ## FRIDAY ##




        # Labels
        Label(work_info_window,bg = "light blue", text = "Friday", width = 15, height = 2, font = underlined_font).grid(column = 3, row = 4)
        Label(work_info_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 3, row = 5)
        Label(work_info_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 4, row = 5)
       
        # Entries
        friday_entry_start = Entry(work_info_window, width = 10, textvariable = self.friday_start)
        friday_entry_start.grid(column = 3, row = 6)
        friday_entry_start_value = friday_entry_start.get()
        friday_entry_start.delete(0, END)
        friday_entry_start.insert(0, friday_entry_start_value)




        friday_entry_end = Entry(work_info_window, width = 10, textvariable = self.friday_end)
        friday_entry_end.grid(column = 4, row = 6)
        friday_entry_end_value = friday_entry_end.get()
        friday_entry_end.delete(0, END)
        friday_entry_end.insert(0, friday_entry_end_value)








        ## SATURDAY ##




        # Labels
        Label(work_info_window,bg = "light blue", text = "Saturday", width = 15, height = 2, font = underlined_font).grid(column = 3, row = 7)
        Label(work_info_window,bg = "light blue", text = "Start", width = 15, height = 2).grid(column = 3, row = 8)
        Label(work_info_window,bg = "light blue", text = "End", width = 15, height = 2).grid(column = 4, row = 8)
       
        # Entries
        saturday_entry_start = Entry(work_info_window, width = 10, textvariable = self.saturday_start)
        saturday_entry_start.grid(column = 3, row = 9)
        saturday_entry_start_value = saturday_entry_start.get()
        saturday_entry_start.delete(0, END)
        saturday_entry_start.insert(0, saturday_entry_start_value)




        saturday_entry_end = Entry(work_info_window, width = 10, textvariable = self.saturday_end)
        saturday_entry_end.grid(column = 4, row = 9)
        saturday_entry_end_value = saturday_entry_end.get()
        saturday_entry_start.delete(0, END)
        saturday_entry_start.insert(0, saturday_entry_end_value)




        # Buttons
        next_section_button = Button(work_info_window, text = "Next Section", command = lambda: self.work_services_window(work_info_window, logged), height = 2, width = 10)
        next_section_button.grid(column = 4, row = 14, padx = 15, pady = 10, sticky = E)
       
        return_button = Button(work_info_window, text = "Go Back", command = lambda: self.account_info_window(logged = logged, previous_window = work_info_window), width = 10, height = 2)
        return_button.grid(column = 0, row = 14, padx = 15, pady = 10, sticky = E)
     
    def change_services(self, treatment: str, user: object = None):
        if user:
            if treatment in self.view_services:
                self.view_services.remove(treatment)
            else:
                self.view_services.append(treatment)
            return
        
        if treatment in self.staff_services:
            self.staff_services.remove(treatment)
        else:
            self.staff_services.append(treatment)
            
    def work_services_window(self, prev_wndw, logged):
        
        self.work_hours_dict = {
            "Monday": [self.monday_start.get(), self.monday_end.get()],
            "Tuesday": [self.tuesday_start.get(), self.tuesday_end.get()],
            "Wednesday": [self.wednesday_start.get(), self.wednesday_end.get()],
            "Thursday": [self.thursday_start.get(), self.thursday_end.get()],
            "Friday": [self.friday_start.get(), self.friday_end.get()],
            "Saturday": [self.saturday_start.get(), self.saturday_end.get()]
        }
        
        # checks previous data is correct( work hours )
        if not User.validate_work_hours(work_hours_dict = self.work_hours_dict, role = self.role_staff_var.get(), window = prev_wndw):
            return
        else:
            # sets up new window
            if prev_wndw: prev_wndw.destroy()
            work_services_window = Toplevel(root)
            work_services_window.geometry("525x500")
            work_services_window.title("Services")
            work_services_window.configure(bg = "light blue")
        
        core_hair_services = ["Haircut", "Hair trim", "Wash and blow-dry", "Restyle", "Fringe trim"]
        colouring_services = ["Full hair dye", "Root touch-up", "Highlights", "Balayage", "Toner application"]
        grooming_extra_services = ["Beard trim", "Beard shaping", "Beard colouring", "Hot towel shave"]
        treatment_services = ["Deep conditioning treatment", "Hair mask treatment", "Keratin treatment"]




        categories = [
            ("Core Hair Services",   core_hair_services),
            ("Colouring Services",   colouring_services),
            ("Grooming & Extras",    grooming_extra_services),
            ("Treatment Services",   treatment_services),
        ]
            
            
        Label(work_services_window, text = "Services", bg = "light blue", font = ("Helvatica", 24)).grid(row = 0, column = 0, columnspan = 2, pady = 10)








        # Loops through each category and creates a checkbutton
        # If button was previously selected it keeps its memory




        # CATEGORY 1 #
        for i, treatment in enumerate(categories[0][1]):
            
            Label(work_services_window, text = categories[0][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 1, column = 0, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):
                
                cat_1_cb = Checkbutton(work_services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment))
                cat_1_cb.grid(row = i + 2, column = 0, pady = (0, 5), padx = (30, 0), sticky = W)
                
                if treatment in self.staff_services: cat_1_cb.select()
                
            create_checkbox(treatment)
            
        # CATEGORY 2 # 
        for i, treatment in enumerate(categories[1][1]):
            
            Label(work_services_window, text = categories[1][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 1, column = 1, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):




                cat_2_cb = Checkbutton(work_services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment))
                cat_2_cb.grid(row = i + 2, column = 1, pady = (0, 5), padx = (30, 0), sticky = W)
            
                if treatment in self.staff_services: cat_2_cb.select()
                
            create_checkbox(treatment)
            
        # CATEGORY 3 #
        for i, treatment in enumerate(categories[2][1]):
            
            Label(work_services_window, text = categories[2][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 7, column = 0, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):




                cat_3_cb = Checkbutton(work_services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment))
                cat_3_cb.grid(row = i + 9, column = 0, pady = (0, 5), padx = (30, 0), sticky = W)
            
                if treatment in self.staff_services: cat_3_cb.select()




            create_checkbox(treatment)








        # CATEGORY 4 #
        for i, treatment in enumerate(categories[3][1]):
            
            Label(work_services_window, text = categories[3][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 7, column = 1, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):
                
                cat_4_cb = Checkbutton(work_services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment))
                cat_4_cb.grid(row = i + 9, column = 1, pady = (0, 5), padx = (30, 0), sticky = W)
                
                if treatment in self.staff_services: cat_4_cb.select()
                
            create_checkbox(treatment)




        # Buttons
        Button(work_services_window, text = "Go back", font = ("Helvatica", 18), command = lambda: self.work_hours_window(work_services_window, logged)).grid(row = 13, column = 0, sticky = W, padx = (20, 0))
        Button(work_services_window, text = "Next Section", font = ("Helvatica", 18), command = lambda: self.notes_info_window(work_services_window, logged)).grid(row = 13, column = 1, sticky = W, padx = (20, 0))

    def notes_info_window(self, previous_window, logged):




        # checks previous data is correct( services )
        if not User.validate_work_services(services = self.staff_services, role = self.role_staff_var.get(), window = previous_window):
            return
        else:
            # sets up new window
            if previous_window: previous_window.destroy()
            notes_window = Toplevel(root)
            notes_window.geometry("375x225")
            notes_window.title("Notes")
            notes_window.configure(bg = "light blue")
       
        Label(notes_window, text = "Additional notes:", bg = "light blue").grid(column = 0, row = 0)
       
        notes_text = Text(notes_window, height = 8, width = 27)
        notes_text.grid(column = 1, row = 0, pady = 5, padx = 3)
       
        next_section_button = Button(
            notes_window, text = "Add Staff",
            command = lambda: self.add_staff(logged_user = logged, notes = notes_text.get("1.0", "end-1c"), add_staff_window = notes_window),
            height = 2, width = 10
            )
       
        next_section_button.grid(column = 1, row = 14, padx = 15, pady = 10, sticky = E)
       
        return_button = Button(notes_window, text = "Go Back", command = lambda: self.work_services_window(logged = logged, previous_window = notes_window), width = 10, height = 2)
        return_button.grid(column = 0, row = 14, padx = 15, pady = 10, sticky = E)

    def add_staff(self, logged_user, notes, add_staff_window):
        
        #checks previous data is correct( notes )
        if not User.validate_notes_info(notes = notes, window = add_staff_window):
            self.notes_info_window(previous_window = None, logged = logged_user)
            return
            
        
        staff_details = {
            "firstname": self.firstname_staff_var.get().strip(),
            "surname" : self.surname_staff_var.get().strip(),
            "dob" : [int(self.date["year"]), int(self.date["month"]), int(self.date["day"])],
            "phone_number": self.phone_number_staff_var.get().strip(),
            "email": self.email_staff_var.get().strip(),
            "c_email": self.c_email_staff_var.get().strip(),
            "postcode": self.postcode_staff_var.get().strip(),
            "username": self.username_staff_var.get().strip(),
            "password": self.userPassword_staff_var.get().strip(),
            "role": self.role_staff_var.get().strip(),
            "working_hours": self.work_hours_dict,
            "services": self.staff_services,
            "notes": notes.strip()
        }




        with open("user_data.pickle", "rb") as f: staffs = pickle.load(f)




        match staff_details["role"]:
            case "Admin":
                new_staff = Admin(
                        staff_details["firstname"],
                        staff_details["surname"],
                        staff_details["dob"],
                        staff_details["phone_number"],
                        staff_details["email"],
                        staff_details["postcode"],
                        staff_details["username"],
                        staff_details["password"],
                        {
                            "Monday": [],
                            "Tuesday": [],
                            "Wednesday": [],
                            "Thursday": [],
                            "Friday": [],
                            "Saturday": []
                        }
                            ,
                        [],
                        staff_details["notes"],
                        isAdmin = True
                        )




                # correctly update id
                new_staff.staff_id = staffs[len(staffs) - 1].staff_id + 1




                staffs.append(new_staff)
            case "Both":
                new_staff = Admin(
                    staff_details["firstname"],
                    staff_details["surname"],
                    staff_details["dob"],
                    staff_details["phone_number"],
                    staff_details["email"],
                    staff_details["postcode"],
                    staff_details["username"],
                    staff_details["password"],
                    staff_details["working_hours"],
                    staff_details["services"],
                    staff_details["notes"],
                    isAdmin = True,
                    isStaff = True
                    )




                # correctly update id
                new_staff.staff_id = staffs[len(staffs) - 1].staff_id + 1








                staffs.append(new_staff)
            case "Staff":
                new_staff = Staff(
                        staff_details["firstname"],
                        staff_details["surname"],
                        staff_details["dob"],
                        staff_details["phone_number"],
                        staff_details["email"],
                        staff_details["postcode"],
                        staff_details["username"],
                        staff_details["password"],
                        staff_details["working_hours"],
                        staff_details["services"],
                        staff_details["notes"],
                        isStaff = True
                        )




                # correctly update id
                new_staff.staff_id = staffs[len(staffs) - 1].staff_id + 1








                staffs.append(new_staff)








        with open("user_data.pickle", "wb") as f: pickle.dump(staffs, f)
       
        staff_window.create_window(logged_user, add_staff_window = add_staff_window)
        messagebox.showinfo("Staff", "Staff successfully added")

    def reset_variables(self):
        # reset all entries to nothing( empty )
        for var_name, value in staff_window.__dict__.items():
            if var_name == "work_hours_dict":
                self.work_hours_dict = {}
            elif isinstance(value, StringVar):
                value.set("")
            elif isinstance(value, list):
                setattr(self, var_name, []) 


class MakeBooking:
    
    def __init__(self):
        ## ----------- ##
        ## Main Frames ##
        ## ----------- ##
        
        self.header_frame = None
        self.customer_window_frame = None
        self.canvas_container = None
        self.scroll_window_canvas = None
        self.scrollbar = None
        self.customer_window_frame2 = None
        
        self.logged_user = None
        self.trace_id = None
        
        
        ## --------------- ##
        ## Booking Windows ##
        ## --------------- ##




        self.staff_wndw = None
        self.services_window = None
        self.months_window = None
        self.cal = None
        
        
        ## ----------------- ##
        ## Booking Variables ##
        ## ----------------- ##




        self.making_booking = False
        self.services_list = []
        self.staff_var = StringVar()
        self.selected_staff = None
        self.timeslots_list = []
         
    def create_window(self, logged_user: object, prev_window: Frame = None):




        if prev_window: prev_window.destroy()
        self.reset_variables()
        
        self.logged_user = logged_user








        if main_window.main_window_frame: main_window.main_window_frame.destroy()








        ## reset customer window ##
        if self.header_frame: self.header_frame.destroy()
        if self.customer_window_frame: self.customer_window_frame.destroy()








        ## display customers ##
        self.header_frame = Frame(root, height = 50, bg = "light blue")
        self.header_frame.pack(fill = X)








        back_button = Button(self.header_frame, text = "Go Back", command = lambda: main_window.create_window(self.logged_user), height = 2, width = 10)
        back_button.grid(column = 2, row = 0, padx = 650, sticky = E)








        customer_list_label = Label(self.header_frame, bg =  "light blue", text = "Choose a customer", font = ("Helvatica", 18))
        customer_list_label.grid(column = 0, row = 0)








        self.customer_window_frame = Frame(root, bg = "light blue")
        self.customer_window_frame.pack(fill = BOTH, expand = 1)








        self.canvas_container = Frame(self.customer_window_frame, bg = "light blue")
        self.canvas_container.pack(fill = BOTH, expand = True)
       
    
        self.scroll_window_canvas = Canvas(self.canvas_container, bg = "light blue")
        self.scroll_window_canvas.pack(side = LEFT, fill = BOTH, expand = True)








        self.scrollbar = ttk.Scrollbar(self.canvas_container, orient = VERTICAL, command = self.scroll_window_canvas.yview)
        self.scrollbar.pack(side = RIGHT, fill = Y)








        self.scroll_window_canvas.configure(yscrollcommand = self.scrollbar.set)
        self.scroll_window_canvas.bind("<Configure>", lambda e: self.scroll_window_canvas.configure(scrollregion = self.scroll_window_canvas.bbox("all")))








        self.customer_window_frame2 = Frame(self.scroll_window_canvas, bg = "light blue", name = "customer holder")








        self.scroll_window_canvas.create_window((0,0), window = self.customer_window_frame2, anchor = "nw")








        # Sort customers based on firstname and surname in descending order
        ordered_customer_list = []
        
        with open("customer_data.pickle", "rb") as f: 
            customers = pickle.load(f)




            ordered_customer_list = sorted(customers, key = lambda e: f"{e.firstname} {e.surname}")








        # Display each customer as a button
        y = 50
        for i, customer in enumerate(ordered_customer_list):
            def create_button(customer):
                Button(self.customer_window_frame2, command = lambda: self.services(customer, self.logged_user, reset_variables = True), text = f"{customer.firstname} {customer.surname}", width = 68, font = ("Helvatica", 18)).grid(row = i, column = 0, padx = 10, pady = 5)
           
            create_button(customer)
            y += 50
            
    def services(self, customer: object, logged_user: object, prev_window: Frame = None, reset_variables = False):
        
        if reset_variables:
            self.reset_variables()


        if prev_window: 
            prev_window.destroy()




        self.customer = customer
        
        self.services_window = Toplevel(root)
        self.services_window.title("Services for current staff")
        self.services_window.geometry("525x500")
        self.services_window.config(bg = "light blue")








        core_hair_services = ["Haircut", "Hair trim", "Wash and blow-dry", "Restyle", "Fringe trim"]
        colouring_services = ["Full hair dye", "Root touch-up", "Highlights", "Balayage", "Toner application"]
        grooming_extra_services = ["Beard trim", "Beard shaping", "Beard colouring", "Hot towel shave"]
        treatment_services = ["Deep conditioning treatment", "Hair mask treatment", "Keratin treatment"]








        categories = [
            ("Core Hair Services",   core_hair_services),
            ("Colouring Services",   colouring_services),
            ("Grooming & Extras",    grooming_extra_services),
            ("Treatment Services",   treatment_services),
        ]
            
            
        Label(self.services_window, text = "Choose services for booking", bg = "light blue", font = ("Helvatica", 24)).grid(row = 0, column = 0, columnspan = 2, pady = 10)








        # CATEGORY 1 #
        for i, treatment in enumerate(categories[0][1]):
            
            Label(self.services_window, text = categories[0][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 1, column = 0, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):
                
                cat_1_cb = Checkbutton(self.services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment))
                cat_1_cb.grid(row = i + 2, column = 0, pady = (0, 5), padx = (30, 0), sticky = W)
                
                if treatment in self.services_list: cat_1_cb.select()
                
            create_checkbox(treatment)
            
        # CATEGORY 2 #
        for i, treatment in enumerate(categories[1][1]):
            
            Label(self.services_window, text = categories[1][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 1, column = 1, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):




                cat_2_cb = Checkbutton(self.services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment))
                cat_2_cb.grid(row = i + 2, column = 1, pady = (0, 5), padx = (30, 0), sticky = W)
            
                if treatment in self.services_list: cat_2_cb.select()
                
            create_checkbox(treatment)
            
        # CATEGORY 3 #  
        for i, treatment in enumerate(categories[2][1]):
            
            Label(self.services_window, text = categories[2][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 7, column = 0, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):




                cat_3_cb = Checkbutton(self.services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment))
                cat_3_cb.grid(row = i + 9, column = 0, pady = (0, 5), padx = (30, 0), sticky = W)
            
                if treatment in self.services_list: cat_3_cb.select()




            create_checkbox(treatment)




        # CATEGORY 4 #
        for i, treatment in enumerate(categories[3][1]):
            
            Label(self.services_window, text = categories[3][0], bg = "light blue", font = ("Helvatica", 18)).grid(row = 7, column = 1, padx = 10, pady = (0, 5))




            def create_checkbox(treatment):




                cat_4_cb = Checkbutton(self.services_window, text = treatment, bg = "light blue", command = lambda: self.change_services(treatment, ))
                cat_4_cb.grid(row = i + 9, column = 1, pady = (0, 5), padx = (30, 0), sticky = W)
                
                if treatment in self.services_list: cat_4_cb.select()
                
            create_checkbox(treatment)
        
        # Buttons
        Button(self.services_window, text = "Go back", command = lambda: self.create_window(logged_user, self.services_window), height = 2, width = 10).grid(column = 0, row = 13, pady = 10)
        Button(self.services_window, text = "Next Section", height = 2, width = 10, command = lambda: self.choose_staff(logged_user, self.services_window)).grid(column = 1, row = 13, pady = 10)
  
    def change_services(self, treatment: str):
        
        if treatment in self.services_list:
            self.services_list.remove(treatment)
        else:
            self.services_list.append(treatment)
      
    def choose_staff(self, logged_user: object, prev_window: Frame = None):
        
        if prev_window: prev_window.destroy()
        
        allowed_services = [
            "Haircut", "Hair trim", "Wash and blow-dry", 
            "Restyle", "Fringe trim", "Full hair dye","Root touch-up", 
            "Highlights", "Balayage", "Toner application", "Beard trim", 
            "Beard shaping", "Beard colouring","Hot towel shave", 
            "Deep conditioning treatment", "Hair mask treatment", "Keratin treatment"
            ]
        
        for service in self.services_list:
            if service not in allowed_services:
                self.services(customer = self.customer, logged_user = logged_user)
                messagebox.showerror("Error", "One of the services entered is not in the database")
                self.services_window.lift()
                self.services_window.focus_force()
                return
  
        staff_wndw = Toplevel(root)
        x = 60
        staff_wndw.geometry(f"100x{x}")
        staff_wndw.config(bg = "light blue")
        
        # if no services have been chosen stop and inform user
        # reload previous window ( services )
        if len(self.services_list) == 0:
            self. services(customer = self.customer, logged_user = logged_user, prev_window = staff_wndw)
            messagebox.showwarning("Services", "No services have been chosen")
            self.services_window.lift()
            self.services_window.focus_force()
            return
        
        with open("user_data.pickle", "rb") as f: users = pickle.load(f)
        
        available_staff_list = []
        
        # loops through all the users that can work (isStaff == True ) and appends them to a list
        for user in users:
            if user.isStaff:
                if all(service in user.services for service in self.services_list):
                    if user not in available_staff_list:
                        available_staff_list.append(user)
        
        Label(staff_wndw, text = "Pick a Staff Member", bg = "light blue", height = 2, width = 20).grid(column = 0, row = 0, columnspan = 2)
        Entry(staff_wndw, textvariable = self.staff_var, width = 20).grid(column = 0, row = 1, columnspan = 2)
        
        if len(available_staff_list) == 0:
            self.services(customer = self.customer, logged_user = logged_user, prev_window = staff_wndw)
            messagebox.showwarning("Services", "No staff do those services")
            self.services_window.lift()
            self.services_window.focus_force()
            return




        # Creates buttons with the staff's name that can do those services one under another
        text = ""
        for i in range(len(available_staff_list)):
            text = f"{available_staff_list[i].firstname[:]} {available_staff_list[i].surname[:]}"
            print(text)
            Button(staff_wndw, text = text, font = ("Helvatica", 16), width = 15, command = lambda t = text : self.staff_var.set(t)).grid(column = 0, row = i + 2, columnspan = 2, pady = 5)
            x += 45
            staff_wndw.geometry(f"345x{x}")
            
        x += 90
        staff_wndw.geometry(f"345x{x}")
        
        Button(staff_wndw, text = "Go Back", font = ("Helvatica", 20), command = lambda: self. services(customer = self.customer, logged_user = logged_user, prev_window = staff_wndw)).grid(column = 0, row = len(available_staff_list) + 3, pady = 5, padx = 10)
        Button(staff_wndw, text = "Next Section", font = ("Helvatica", 20), command = lambda: self.choose_date( prev_window = staff_wndw)).grid(column = 1, row = len(available_staff_list) + 3, pady = 5, padx = 10)
        
    def choose_date(self, prev_window: Frame = None):




        if self.staff_var.get() == "":
            messagebox.showerror("Staff", "No staff have been picked for booking")
            prev_window.lift()
            prev_window.focus_force()
            return




        if prev_window: prev_window.destroy()




        self.months_window = Toplevel(root)
        self.months_window.geometry("600x700")
        self.months_window.title("Booking Date")
        self.months_window.config(bg = "light blue")








        ## CALENDAR ##
        
        self.cal = Calendar(self.months_window, selectmode = "day", showweeknumbers = False, borderwidth = 3)
        self.cal.grid(row = 0, column = 0)
        
        # when a data is clicked create the time slots for that hour
        self.trace_id = self.cal.bind("<<CalendarSelected>>", self.timeslot_creation)
        
        ## TIME SLOTS ##
        
        Button(self.months_window, text = "Go Back", command = lambda: self.choose_staff(logged_user = self.logged_user, prev_window = self.months_window), font = ("Helvatica", 18)).grid(row = 1, column = 0, pady = 10)
        
        Label(self.months_window, text = "Time Slots for that Day", font = ("Helvatica", 18), bg = "light blue").grid(row = 0, column = 1)
        
    def timeslot_creation(self, *args):
        
        # Ensure a calendar widget exists before proceeding
        if self.cal:

            # Convert selected date from calendar (string) into datetime object for comparisons
            self.date = datetime.strptime(self.cal.get_date(), "%m/%d/%y")
            
            # Compare selected date with today's date
            if self.date < datetime.strptime(f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year}", "%d/%m/%Y"):
                Label(self.months_window, text = "Cannot choose a day in the past", font = ("Helvatica", 14), fg = "Red", bg = "light blue").grid(column = 0, row = 2)
                for label in self.timeslots_list:
                    label.destroy()
                    self.timeslots_list = []
                return
            
            # checks if the date is on Sunday
            if self.date.strftime("%A") == "Sunday":
                Label(self.months_window, text = "Salon is closed on Sunday", font = ("Helvatica", 14), fg = "Red", bg = "light blue", width = 25).grid(column = 0, row = 2)
                for timeslot in self.timeslots_list:
                    timeslot.destroy()
                return
            else: 
                Label(self.months_window, font = ("Helvatica", 14), bg = "light blue", width = 24).grid(column = 0, row = 2)

            with open("user_data.pickle", "rb") as f: 
                staff = pickle.load(f)

            # Match staff based on selected ID
            for user in staff:
                if f"{user.firstname} {user.surname}" in self.staff_var.get():
                    self.selected_staff = user
            
            # destroy existing time slots
            for label in self.timeslots_list:
                label.destroy()

            self.timeslots_list = []
            
            # check if staff works on selected day
            if self.selected_staff.working_hours[self.date.strftime("%A")][0] != "" and self.selected_staff.working_hours[self.date.strftime("%A")][1] != "":

                # get working hours
                start = int(self.selected_staff.working_hours[self.date.strftime("%A")][0])
                end = int(self.selected_staff.working_hours[self.date.strftime("%A")][1])

                # Loop through each possible hour slot
                for hour in range(start, end):
                    
                    # prevents user from bookings timeslots which on the day and in the past hours
                    if self.date.month == datetime.now().month and self.date.day == datetime.now().day and self.date.year == datetime.now().year:
                        if hour <= int(datetime.now().strftime("%H")):
                            continue
                    
                    booking_exists = True

                    # check if timeslot is already booked
                    for booking in self.selected_staff.bookings[self.date.strftime("%B")]:

                        # compare full date + hours with existing bookings
                        # if a booking exists on that day and slot do not add it to the window
                        if (int(self.date.day) == int(booking.date.day)) and (int(self.date.month) == int(booking.date.month)) and (int(self.date.year) == int(booking.date.year)) and ((int(hour)) == int(booking.slot)):
                            booking_exists = False

                    # skip slot if already booked
                    if not booking_exists: continue
                
                    # create available timeslot button
                    label = Button(self.months_window, font = ("Helvatica", 18), width = 15, text = f"{hour}:00 - {hour + 1}:00", command = lambda h = hour: self.additional_notes(h, self.months_window))
                    
                    # store button for later management
                    self.timeslots_list.append(label)
                
                # display time slots
                row = 1
                for label in self.timeslots_list:
                    label.grid(column = 1, row = row, pady = 2)
                    row += 1
            else:
                # if staff does not work that day inform user
                Label(self.months_window, text = "Staff not available this day", font = ("Helvatica", 14), bg= "light blue").grid(column = 1, row = 1)
    
    def additional_notes(self, hour: int, prev_window: Frame):
        
        if prev_window: prev_window.destroy()
        
        notes_wndw = Toplevel(root)
        notes_wndw.title("Additional Notes")
        notes_wndw.config(bg = "light blue")
        notes_wndw.geometry("230x200")
        
        Label(notes_wndw, text = "Additional notes:", bg = "light blue").grid(column = 0, row = 0,  columnspan = 2, padx = 10)
       
        notes_text = Text(notes_wndw, height = 8, width = 27)
        notes_text.grid(column = 0, row = 1, pady = 5, padx = 3, columnspan = 2)
        
        Button(notes_wndw, text = "Go Back", command = lambda: self.choose_date(prev_window = notes_wndw), width = 10).grid(row = 2, column = 0)
        
        Button(notes_wndw, text = "Continue", command = lambda: self.complete_booking(hour, notes_text.get("1.0", "end-1c"), notes_wndw), width = 10).grid(row = 2, column = 1)
                     
    def complete_booking(self, hour: int, notes: str, prev_window: Frame = None):
        
        if prev_window: prev_window.destroy()
        
        booking_dict = {
            "Customer": self.customer,
            "Staff": self.selected_staff,
            "Slot": hour,
            "Date": self.date,
            "Services": self.services_list,
            "Notes": notes
        }
        
        booking_details_window = Toplevel(root)
        booking_details_window.title("Complete Booking")
        booking_details_window.config(bg = "light blue")
        booking_details_window.geometry("375x450")
        
        Label(booking_details_window, text = "Booking Details", font = underlined_font, bg = "light blue").grid(row = 0, column = 0, columnspan = 3, pady = 10)
        
        # Display new booking details for final check by user
        for key in booking_dict:
            match key:
                case "Customer":
                    Label(booking_details_window, text = "Customer", width = 15, font = ("Helvatica", 14), relief = SOLID,borderwidth = 1, bg = "light blue").grid(row = 1, column = 0, padx = 10, pady = 5, sticky = W)
                    Label(booking_details_window, text = f"{booking_dict[key].firstname} {booking_dict[key].surname}", width = 15, font = ("Helvatica", 14), relief = SOLID,borderwidth = 1, bg = "light blue").grid(row = 1, column = 1)
                case "Staff":
                    Label(booking_details_window, text = "Staff", width = 15, font = ("Helvatica", 14), relief = SOLID,borderwidth = 1, bg = "light blue").grid(row = 2, column = 0, padx = 10, pady = 5, sticky = W)
                    Label(booking_details_window, text = f"{booking_dict[key].firstname} {booking_dict[key].surname}", width = 15, font = ("Helvatica", 14), relief = SOLID,borderwidth = 1, bg = "light blue").grid(row = 2, column = 1)
                case "Slot":
                    Label(booking_details_window, text = "Slot", width = 15, font = ("Helvatica", 14), relief = SOLID,borderwidth = 1, bg = "light blue").grid(row = 3, column = 0, padx = 10, pady = 5, sticky = W)
                    Label(booking_details_window, text = f"{booking_dict[key]}:00 - {booking_dict[key] + 1}:00", width = 15, font = ("Helvatica", 14), relief = SOLID,borderwidth = 1, bg = "light blue").grid(row = 3, column = 1)
                case "Date":
                    Label(booking_details_window, text = "Date", width = 15, font = ("Helvatica", 14), relief = SOLID,borderwidth = 1, bg = "light blue").grid(row = 4, column = 0, padx = 10, pady = 5, sticky = W)
                    Label(booking_details_window, text = booking_dict[key].strftime("%d/%m/%Y"), width = 15, font = ("Helvatica", 14), relief = SOLID,borderwidth = 1, bg = "light blue").grid(row = 4, column = 1)
                case "Services":
                    
                    services_lines = []
                    for i in range(0, len(booking_dict[key]), 5):
                        services_lines.append(", ".join(booking_dict[key][i:i+5]))
                    services_str = "\n".join(services_lines)

                    num_lines = max(1, len(services_lines))  # at least 1 row tall

                    Label(booking_details_window, text = "Services:", width = 15, relief = SOLID, font = ("Helvatica", 14), borderwidth = 1, bg = "light blue").grid(row = 5, column = 0, padx = 5, pady = 5)
                    services_text = Text(booking_details_window, height = num_lines, width = 22, relief = SOLID, bg = "light blue")
                    services_text.insert("1.0", services_str)
                    services_text.config(state = DISABLED)
                    services_text.grid(row = 5, column = 1)
                    
                case "Notes":
                    Label(booking_details_window, text = "Notes", width = 15, font = ("Helvatica", 14), relief = SOLID, borderwidth = 1, bg = "light blue").grid(row = 6, column = 0, padx = 10, pady = 5, sticky = W)
                    Label(booking_details_window, text = booking_dict[key], width = 15, font = ("Helvatica", 14), relief = SOLID,borderwidth = 1, bg = "light blue").grid(row = 6, column = 1)
        
        Button(booking_details_window, text = "Cancel Booking", width = 15, command = lambda: self.create_window(self.logged_user, booking_details_window)).grid(row = 7, column = 0, pady = 5)
        Button(booking_details_window, text = "Go Back", width = 15, command = lambda: self.additional_notes(hour, booking_details_window)).grid(row = 7, column = 1, pady = 5)
        Button(booking_details_window, text = "Confirm Booking", width = 15, font = ("Helvatica", 14), command = lambda: self.save_booking(booking_dict, booking_details_window)).grid(row = 8, column = 0, columnspan = 2, pady = 5)

    def reset_variables(self):
        
        self.services_list = []
        self.selected_staff = ""
        self.staff_var.set("")
    
    def save_booking(self, new_booking_dict: dict, prev_wndw: Frame):
        
        # load all users and bookings
        with open("user_data.pickle", "rb") as f: users = pickle.load(f)
        with open("bookings.pickle", "rb") as f: bookings = pickle.load(f)

        working_staff = []


        # Loop through all users to determine which staff are working at the selected day and time
        for user in users:
            if len(user.working_hours[self.date.strftime("%A")]) == 0: continue

            if user.working_hours[self.date.strftime("%A")][0] != "" and user.working_hours[self.date.strftime("%A")][1] != "":

                # Check if selected booking slot falls within staff working hours
                # chosen time slot is bigger than start of working day
                # chosen time slot is smaller than end of working day
                if int(new_booking_dict["Slot"]) >= int(user.working_hours[self.date.strftime("%A")][0]) and int(new_booking_dict["Slot"]) <= int(user.working_hours[self.date.strftime("%A")][1]):
                    working_staff.append(user)
                    
        print(working_staff)
        
        # fill dictionary with existing bookings for quick lookup
        for booking in bookings:
            if booking.date == new_booking_dict["Date"] and booking.slot == new_booking_dict["Slot"] and booking.customer.customer_id == new_booking_dict["Customer"].customer_id:
                messagebox.showerror("Booking Error", "A customer already has a booking on that day and time slot")
                prev_wndw.lift()
                prev_wndw.focus_force()
                return
            
            Booking.bookings_dict[booking.date.strftime("%B")][booking.date.day][booking.slot].append(booking)


        # Check if number of bookings in selected slot is less than available staff
        # This prevents overbooking beyond staff capacity
        if len(Booking.bookings_dict[new_booking_dict["Date"].strftime("%B")][new_booking_dict["Date"].day][new_booking_dict["Slot"]]) < len(working_staff):
            
            # create new booking object
            new_booking = Booking(
                customer = new_booking_dict["Customer"],
                staff = new_booking_dict["Staff"],
                slot = new_booking_dict["Slot"],
                date = new_booking_dict["Date"],
                services = new_booking_dict["Services"],
                notes = new_booking_dict["Notes"]
            )


            if len(bookings) != 0:
                new_booking.booking_id = bookings[len(bookings) - 1].booking_id + 1
            
            # add booking to dictionary for fast access
            Booking.bookings_dict[new_booking.date.strftime("%B")][new_booking.date.day][new_booking.slot].append(new_booking)
            
            # add booking to main bookings list
            bookings.append(new_booking)


            # save updated bookings list to file
            with open("bookings.pickle", "wb") as f:
                pickle.dump(bookings, f)
        else:
            # if slot is full, notify user and stop process
            messagebox.showinfo("Booking notice", "Day is full" )
            self.choose_date(prev_window = prev_wndw)
            return


        # add new booking to selected staff member's personal booking list
        new_booking_dict["Staff"].bookings[new_booking_dict["Date"].strftime("%B")].append(new_booking)


        # reload users and update the correct staff member's bookings
        with open("user_data.pickle", "rb") as f: 
            users = pickle.load(f)
            for user in users:
                if user.staff_id == new_booking_dict["Staff"].staff_id:
                    user.bookings = new_booking_dict["Staff"].bookings

            # save updated user data back to file
            with open("user_data.pickle", "wb") as f:
                pickle.dump(users, f)


        # close calendar/booking window after successful booking
        if self.months_window and self.months_window.winfo_exists(): 
            self.months_window.destroy()
          
        self.months_window = None
        self.cal = None


        messagebox.showinfo("Booking", "Booking was succesfully added")
        self.create_window(self.logged_user, prev_wndw)


class ViewBooking:
    
    def __init__(self):
        ## ----------- ##
        ## Main Frames ##
        ## ----------- ##
        
        self.header_frame = None
        self.booking_window_frame = None
        self.main_content = None
        self.canvas_container = None
        self.scroll_window_canvas = None
        self.scrollbar = None
        self.booking_window_frame2 = None
        




        self.load_booking_window = None
        self.logged_user = None

    def create_window(self, logged_user: object, prev_wndw: Frame = None):




        if prev_wndw: prev_wndw.destroy()








        self.logged_user = logged_user
       
        if main_window.main_window_frame: main_window.main_window_frame.destroy()








        ## reset customer window ##
        if self.header_frame: self.header_frame.destroy()
        if self.booking_window_frame: self.booking_window_frame.destroy()








        ## display customers ##
        self.header_frame = Frame(root, height = 50, bg = "light blue")
        self.header_frame.pack(fill = X)








        back_button = Button(self.header_frame, text = "Go Back", command = lambda: main_window.create_window(self.logged_user), height = 2, width = 10)
        back_button.grid(column = 2, row = 0, padx = 650, sticky = E)








        Label(self.header_frame, bg =  "light blue", text = "Choose a Booking", font = ("Helvatica", 18)).grid(column = 0, row = 0)








        ## Main Area ##
        self.booking_window_frame = Frame(root, bg = "light blue")
        self.booking_window_frame.pack(fill = BOTH, expand = True)
        
        self.main_content = Frame(self.booking_window_frame, bg = "light blue")
        self.main_content.pack(fill = BOTH, expand = True)








        self.main_content.columnconfigure(0, weight = 1)
        self.main_content.columnconfigure(1, weight = 0)
        self.main_content.rowconfigure(0, weight = 1)
        
        
        ## Scroll Area ##
        self.canvas_container = Frame(self.main_content, bg = "light blue")
        self.canvas_container.grid(row = 0, column = 0, sticky = "nsew")
       
    
        self.scroll_window_canvas = Canvas(self.canvas_container, bg = "light blue")
        self.scroll_window_canvas.pack(side = LEFT, fill = BOTH, expand = True)








        self.scrollbar = ttk.Scrollbar(self.canvas_container, orient = VERTICAL, command = self.scroll_window_canvas.yview)
        self.scrollbar.pack(side = RIGHT, fill = Y)








        self.scroll_window_canvas.configure(yscrollcommand = self.scrollbar.set)








        self.booking_window_frame2 = Frame(self.scroll_window_canvas, bg = "light blue")
        self.canvas_window = self.scroll_window_canvas.create_window((0,0), window = self.booking_window_frame2, anchor = "nw")








        self.booking_window_frame2.bind("<Configure>", lambda e: self.scroll_window_canvas.configure(scrollregion = self.scroll_window_canvas.bbox("all")))
        self.scroll_window_canvas.bind("<Configure>", lambda e: self.scroll_window_canvas.itemconfigure(self.canvas_window, width = e.width))
        
        ## Search Area ##
        self.search_panel = Frame(self.main_content, bg = "light blue", width = 120)
        self.search_panel.grid(row = 0, column = 1, sticky = "ns")
        self.search_panel.grid_propagate(False)








        Label(self.search_panel, text = "Search by name", bg = "light blue", font = underlined_font).pack(pady = 10)
        
        self.search_entry_name = Entry(self.search_panel)
        self.search_entry_name.pack(padx = 5, pady = 5)
        
        Label(self.search_panel, text = "Search by phone number", bg = "light blue", font = underlined_font).pack(pady = 10)
        
        self.search_entry_phone_number = Entry(self.search_panel)
        self.search_entry_phone_number.pack(padx = 5, pady = 5)
        
        Label(self.search_panel, text = "Search by DoB", bg = "light blue", font = underlined_font).pack(pady = 10)
        
        days  =[f"{x:02}" for x in range(1, 32)]
        months = [f"{x:02}" for x in range(1, 13)]
        year = [x for x in range(int(datetime.now().year) - 100, int(datetime.now().year) + 1)][::-1]
        
        
        self.cb_day_search = ttk.Combobox(self.search_panel, values = days, width = 8)
        self.cb_day_search.set("Day")
        self.cb_day_search.pack(pady = 5)
        
        
        self.cb_month_search = ttk.Combobox(self.search_panel, values = months, width = 8)
        self.cb_month_search.set("Month")
        self.cb_month_search.pack(pady = 5)
        
        
        self.cb_year_search = ttk.Combobox(self.search_panel, values = year, width = 8)
        self.cb_year_search.set("Year")
        self.cb_year_search.pack(pady = 5)
        
        style = ttk.Style()
        style.configure("Custom.TRadiobutton", background = "light blue", foreground = "black", font = ("arial", 12))
        style.map("Custom.TRadiobutton", background = [("active", "light blue"), ("selected", "light blue")])
        
        self.view_past_bookings_bool = IntVar()
        ttk.Radiobutton(self.search_panel, text = "Display old bookings", value = 1, variable = self.view_past_bookings_bool, style = "Custom.TRadiobutton").pack(pady = 5)
        




        Button(self.search_panel, text = "Search", font = ("Helvatica", 20), command = lambda: self.search_bookings(name = self.search_entry_name.get(), phone_number = self.search_entry_phone_number.get(), date = [self.cb_day_search.get(), self.cb_month_search.get(), self.cb_year_search.get()], show_all = self.view_past_bookings_bool.get())).pack(pady = 5, side = "bottom")
        Button(self.search_panel, text = "Reset", font = ("Helvatica", 20), command = lambda: self.create_window(self.logged_user)).pack(pady = 5, side = "bottom")




        with open("bookings.pickle", "rb") as f: bookings = pickle.load(f)




        temp_dict = {
            "January": [],
            "February": [],
            "March": [],
            "April": [],
            "May": [],
            "June": [],
            "July": [],
            "August": [],
            "September": [],
            "October": [],
            "November": [],
            "December": []
        }




        today = datetime.now().date()




        # append bookings to each month and those which are in the future
        for booking in bookings:

            booking_date = booking.date.date()
            
            # Past date
            if booking_date < today:
                self.delete_booking(booking_to_delete = booking, prev_wndw = None)
            
            # Today
            elif booking_date == today:
                if booking.slot < datetime.now().hour:
                    self.delete_booking(booking_to_delete = booking, prev_wndw = None)
            
            temp_dict[booking.date.strftime("%B")].append(booking)
        
        # sort bookings based on date and hour
        for month in temp_dict:
            temp_dict[month] = sorted(temp_dict[month], key = lambda e: (e.date, e.slot))




        for month in temp_dict:
            Label(self.booking_window_frame2, bg = "light blue", text = f"{month}", font = ("Helvatica", 26), width = 20, relief = RAISED).pack(padx = 10, pady = 5)




            for booking in temp_dict[month]:
                def create_button(booking):
                    Button(self.booking_window_frame2, command = lambda: self.load_booking(booking), text = f"{booking.customer.firstname} {booking.customer.surname}, {booking.date.strftime("%d/%m/%Y")}", width = 68, font = ("Helvatica", 18)).pack(padx = 10, pady = 5)
            
                create_button(booking)

    def search_bookings(self, name: str, phone_number: str, date: list, show_all: int): 
        
        name = name.strip()
        phone_number = phone_number.strip()
        
        with open("bookings.pickle", "rb") as f:
            bookings = pickle.load(f)
        
        today = datetime.now().date()
        if show_all != 1:
            for booking in bookings:
                booking_date = booking.date.date()
            
                # Past date
                if booking_date < today:
                    self.delete_booking(booking_to_delete = booking, prev_wndw = None)
            
                # Today
                elif booking_date == today:
                    if booking.slot < datetime.now().hour:
                        self.delete_booking(booking_to_delete = booking, prev_wndw = None)
                 
        results = []




        for booking in bookings:
            match = True




            # Name check
            if name != "":
                if not name.isalpha():
                    messagebox.showerror("Search Error", "Only letters allowed in name")
                    return
                
                full_name = f"{booking.customer.firstname} {booking.customer.surname}".lower()
                if name.lower() not in full_name:
                    match = False




            # Phone check 
            if phone_number != "":
                if not phone_number.isdigit():
                    messagebox.showerror("Search Error", "Only numbers allowed in phone")
                    return
                
                if phone_number not in booking.customer.phone_number:
                    match = False




            # Date check
            if date != ["Day", "Month", "Year"]:
                day, month, year = date




                booking_date = booking.date 




                if day != "Day" and int(day) != booking_date.day:
                    match = False
                if month != "Month" and int(month) != booking_date.month:
                    match = False
                if year != "Year" and int(year) != booking_date.year:
                    match = False








            # Final check
            if match: results.append(booking)
        
        # Destroy existing booking buttons
        for widget in self.booking_window_frame2.winfo_children(): widget.destroy()
        
        temp_dict = {
            "January": [],
            "February": [],
            "March": [],
            "April": [],
            "May": [],
            "June": [],
            "July": [],
            "August": [],
            "September": [],
            "October": [],
            "November": [],
            "December": []
        }
        
        # sort results
        results = sorted(results, key = lambda b: (b.date, b.slot))
        
        for booking in results:
            temp_dict[booking.date.strftime("%B")].append(booking)
        
        # load bookings that fit search criteria
        for month in temp_dict:
            Label(self.booking_window_frame2, bg = "light blue", text = f"{month}", font = ("Helvatica", 26), width = 20, relief = RAISED).pack(padx = 10, pady = 5)




            for booking in temp_dict[month]:
                def create_button(booking):
                    Button(self.booking_window_frame2, command = lambda: self.load_booking(booking), text = f"{booking.customer.firstname} {booking.customer.surname}, {booking.date.strftime("%d/%m/%Y")}", width = 68, font = ("Helvatica", 18)).pack(padx = 10, pady = 5)
            
                create_button(booking)
        
        if not results: 
            messagebox.showinfo("Search", "No matching bookings found")
            self.create_window(self.logged_user)
            
    def load_booking(self, booking: object):
        
        self.load_booking_window = Toplevel(root)
        self.load_booking_window.geometry("420x400")
        self.load_booking_window.title("Viewing Booking")
        self.load_booking_window.config(bg = "light blue")


        Label(self.load_booking_window, bg = "light blue", font = ("Helvatica", 30), text = f"Booking ID: {booking.booking_id}").grid(column = 0, row = 0, columnspan = 2, padx = 10, pady = 10)



        Label(self.load_booking_window, text = "Customer:", width = 10, relief = RAISED, font = ("Helvatica", 16)).grid(row = 1, column = 0, padx = 10, pady = 5)
        Label(self.load_booking_window, text = f"{booking.customer.firstname} {booking.customer.surname}", bg = "light blue", relief = SOLID, width = 25).grid(row = 1, column = 1)


        Label(self.load_booking_window, text = "Staff:", width = 10, relief = RAISED, font = ("Helvatica", 16)).grid(row = 2, column = 0, padx = 10, pady = 5)
        Label(self.load_booking_window, text = f"{booking.staff.firstname} {booking.staff.surname}", bg = "light blue", relief = SOLID, width = 25).grid(row = 2, column = 1)


        Label(self.load_booking_window, text = "Slot:", width = 10, relief = RAISED, font = ("Helvatica", 16)).grid(row = 3, column = 0, padx = 10, pady = 5)
        Label(self.load_booking_window, text = f"{booking.slot}:00 - {booking.slot + 1}:00", bg = "light blue", relief = SOLID, width = 25).grid(row = 3, column = 1)


        Label(self.load_booking_window, text = "Date:", width = 10, relief = RAISED, font = ("Helvatica", 16)).grid(row = 4, column = 0, padx = 10, pady = 5)
        Label(self.load_booking_window, text = f"{booking.date.strftime("%d/%m/%Y")}", bg = "light blue", relief = SOLID, width = 25).grid(row = 4, column = 1)


        services_lines = []
        for i in range(0, len(booking.services), 5):
            services_lines.append(", ".join(booking.services[i:i+5]))
        services_str = "\n".join(services_lines)


        num_lines = max(1, len(services_lines))  # at least 1 row tall


        Label(self.load_booking_window, text = "Services:", width = 10, relief = RAISED, font = ("Helvatica", 16)).grid(row = 5, column = 0, padx = 5, pady = 5)
        services_text = Text(self.load_booking_window, height = num_lines, width = 22, relief = SOLID, bg = "light blue")
        services_text.insert("1.0", services_str)
        services_text.config(state = DISABLED)
        services_text.grid(row = 5, column = 1)


        Label(self.load_booking_window, text = "Notes:", width = 10, relief = RAISED, font = ("Helvatica", 16)).grid(row = 6, column = 0, padx = 10, pady = 5)
        Label(self.load_booking_window, text = f"{booking.notes}", bg = "light blue", relief = SOLID, width = 25).grid(row = 6, column = 1)


        Button(self.load_booking_window, text = "Go Back", width = 10, font = ("Helvatica", 16), command = lambda: self.create_window(logged_user = self.logged_user, prev_wndw = self.load_booking_window)).grid(row = 7, column = 1, pady = 20, padx = 10)
        Button(self.load_booking_window, text = "Delete Booking", width = 15, font = ("Helvatica", 16), command = lambda: self.delete_booking(booking, self.load_booking_window)).grid(row = 7, column = 0, padx = 10, pady = 20)

    def delete_booking(self, booking_to_delete: object, prev_wndw: Frame): 
        
        if not messagebox.askyesno("Confirmation", "Delete Booking?"):
            self.load_booking_window.lift()
            self.load_booking_window.focus_force()
            return
        
        # load bookings
        with open("bookings.pickle", "rb") as f: 
            bookings = pickle.load(f)
            
        updated_bookings = []




        for booking in bookings:
            if booking.booking_id != booking_to_delete.booking_id:
                updated_bookings.append(booking)

            for month in Booking.bookings_dict:
                for day in Booking.bookings_dict[month]:
                    for slot in Booking.bookings_dict[month][day]:
                        
                        updated_slot_booking = []
                        
                        for booking in Booking.bookings_dict[month][day][slot]:
                            if booking.booking_id != booking_to_delete.booking_id:
                                
                                booking.append(updated_slot_booking)
                                
                        Booking.bookings_dict[month][day][slot] = updated_slot_booking




        # save updated bookings list
        with open("bookings.pickle", "wb") as f:
            pickle.dump(updated_bookings, f)


        updated_staff_bookings = []




        # delete booking from staff
        for booking in booking_to_delete.staff.bookings[booking_to_delete.date.strftime("%B")]:
            if booking.booking_id != booking_to_delete.booking_id:
                updated_staff_bookings.append(booking)

        # update user data
        with open("user_data.pickle","rb") as f:
            users = pickle.load(f)

            for user in users:
                
                # find correct staff member
                if user.staff_id == booking_to_delete.staff.staff_id:

                    # update their bookings for that month
                    user.bookings[booking_to_delete.date.strftime("%B")] = updated_staff_bookings


        # save updated user data
        with open("user_data.pickle", "wb") as f: pickle.dump(users, f)


        # Remove booking from dictionary structure if used elsewhere
        try:
            Booking.bookings_dict[booking_to_delete.date.strftime("%B")][booking_to_delete.date.day][booking_to_delete.slot].remove(booking_to_delete)
        except:
            pass  # Prevent crash if not found
        
        # return to main window
        self.create_window(self.logged_user, prev_wndw)
        messagebox.showinfo("Booking File", "Booking was succesfully deleted")



if __name__ == "__main__":
   
    work_hours_dict_a = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": []
        }
    
    work_hours_dict_b = {
            "Monday": [8, 18],
            "Tuesday": [8, 18],
            "Wednesday": [8, 18],
            "Thursday": [8, 18],
            "Friday": [8, 18],
            "Saturday": [8, 18]
        }

    admin = Admin(
            firstname = "Kristiyan", 
            surname = "Pehlivanski", 
            dob = [2007, 1, 1], 
            phone_number = "07123456789",
            email = "kris@email.com", 
            postcode = "LL138EJ", 
            username = "1",
            staff_password = "1", 
            working_hours = work_hours_dict_a, 
            services = [], 
            notes = "", 
            isAdmin = True
                )
    
    staff = Staff(
        firstname = "John", 
        surname = "Johny", 
        dob = [2008, 1, 16], 
        phone_number = "07123456701", 
        email = "john@email.com", 
        postcode = "LL139EX", 
        username = "john", 
        staff_password = "Johny6", 
        working_hours = work_hours_dict_b, 
        services = ["Restyle"], 
        notes = "", 
        isStaff = True
    )


    users = [admin, staff]
    
    with open("user_data.pickle", "rb") as f: 
        try:
            staff = pickle.load(f)
            if len(staff) == 0:
                with open("user_data.pickle", "wb") as f:
                    pickle.dump(users, f)
        except EOFError:
            with open("user_data.pickle", "wb") as f:
                pickle.dump(users, f)
   
    log_in_window = Log_In_Window()
    log_in_window.create_window()


    main_window = MainWindow()
   
   
    customer_window = CustomerWindow()


    staff_window = StaffWindow()



    booking_window = MakeBooking()


    view_booking_window = ViewBooking()



root.mainloop()
