from tkinter import *
import json

# UI class
class LoginWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("240x200")
        self.resizable(False, False)
        self.output = Label(self)
        self.login_result = Label(self)
        self.title("Password Generator")

    # builds all widgets and adds them to the window
    def build(self):
        # title
        self.title = Message(self, text="Login Screen", width=400, font=("Helvitica", 20), justify=CENTER)

        # username input
        self.username_label = Label(self, text="Username")
        self.username = Entry(self)

        # password input
        self.password_label = Label(self, text="Password")
        self.password = Entry(self, show="\u2022")

        # login button
        self.login = Button(self, text="Login", command=self.login)

        # register button
        self.register = Button(self, text="Register", command=self.register)

    def pack(self):
        self.title.grid(row=0, column=0, pady=(20, 10), columnspan=3)
        self.username_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 5))
        self.username.grid(row=1, column=1, pady=(0, 5))
        self.password_label.grid(row=2, column=0, padx=(20, 0))
        self.password.grid(row=2, column=1)
        self.login.grid(row=3, column=1, sticky=E)
        self.register.grid(row=4, column=1, sticky=E)

    # called when the login button is pressed
    def login(self):
        valid_login = False
        u_input = self.username.get()
        p_input = self.password.get()

        # read database and check if login is valid
        with open("database.json", "r") as file:
            data= json.loads(file.read())
        for profile in data["login_info"]:
            if u_input == profile['username']:
                if p_input == profile['password']:
                    valid_login = True
                    break
            valid_login = False

        # display message result
        self.login_result.destroy()
        if(valid_login):
            a = ApplicationWindow()
            self.destroy()
        else:
            self.login_result = Label(self, text="Login invalid", fg="red")
            self.login_result.grid(row=5, column=1, sticky=W)

    def register(self):
        r = RegisterWindow()

    # called to build the window and control the main loop
    def run(self):
        self.build()
        self.pack()
        self.mainloop()

class RegisterWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("270x200")
        self.resizable(False, False)
        self.output = Label(self)
        self.register_result = Label(self)
        self.title("Register new user")

        self.run()

    def build(self):
        # title
        self.title = Message(self, text="Register User", width=400, font=("Helvitica", 20), justify=CENTER)

        # username input
        self.username_label = Label(self, text="Username")
        self.username = Entry(self)

        # password input
        self.password_label = Label(self, text="Password")
        self.password = Entry(self, show="\u2022")

        # password input
        self.password2_label = Label(self, text="Retype password")
        self.password2 = Entry(self, show="\u2022")

        # register button
        self.register = Button(self, text="Register", command=self.register)

    def pack(self):
        self.title.grid(row=0, column=0, pady=(20, 10), columnspan=3)
        self.username_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 5))
        self.username.grid(row=1, column=1, pady=(0, 5))
        self.password_label.grid(row=2, column=0, padx=(20, 0))
        self.password.grid(row=2, column=1)
        self.password2_label.grid(row=3, column=0, padx=(20, 0))
        self.password2.grid(row=3, column=1)
        self.register.grid(row=4, column=1, sticky=E)

    def register(self):
        u_input = self.username.get()
        p_input = self.password.get()
        p2_input = self.password2.get()

        # check if username already exists
        nameTaken = False
        with open("database.json", "r") as file:
            data = json.loads(file.read())
        for profile in data["login_info"]:
            if u_input == profile['username']:
                nameTaken = True
                break

        # display error messages, if any
        self.register_result.destroy()
        if len(u_input) < 6:
            self.register_result = Label(self, text="Username must be 6+ characters", fg="red")
        elif nameTaken:
            self.register_result = Label(self, text="Username taken", fg="red")
        elif p_input != p2_input:
            self.register_result = Label(self, text="Passwords do not match", fg="red")
        elif len(p_input) < 6:
            self.register_result = Label(self, text="Password must be 6+ characters", fg="red")
        else:
            self.register_result = Label(self, text="Registered successfully", fg="green")
            new_user = {'username': u_input, 'password': p_input}
            with open('database.json') as file:
                data = json.load(file)
                data["login_info"].append(new_user)
            with open('database.json', 'w') as file:
                json.dump(data, file)

        self.register_result.grid(row=5, column=0, columnspan=2)

    def run(self):
        self.build()
        self.pack()

class ApplicationWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("270x200")
        self.resizable(False, False)
        self.output = Label(self)
        self.register_result = Label(self)
        self.title("Main Application")

        self.run()
    def run(self):
        pass
    
win = LoginWindow()
win.run()