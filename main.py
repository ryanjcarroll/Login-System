from tkinter import *
import json

TITLE_FONT = ("Helvitica", 18)

# Main Tkinter Tk object which contains all frames
class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.frames = {}
        self.frame = None
        for F in (LoginWindow, RegisterWindow, ApplicationWindow, ChangePasswordWindow):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginWindow)
        self.geometry("300x200")
        self.resizable(False, False)

    def show_frame(self, type):
        frame = self.frames[type]
        frame.tkraise()
        frame.set_active()
        self.frame = frame

# Login Page
class LoginWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master

        self.output = Label(self)
        self.login_result = Label(self)

        self.run()

    # builds all widgets and adds them to the window
    def build(self):
        # title
        self.title = Message(self, text="Login Screen", width=400, font=TITLE_FONT, justify=CENTER)

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

    # called whenever this frame is set as the active frame
    def set_active(self):
        self.master.title("Login Page")

    def clear(self):
        self.username.delete(0,'end')
        self.password.delete(0,'end')

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
            self.clear()
            self.master.frames[ApplicationWindow].set_user(u_input)
            self.master.show_frame(ApplicationWindow)
        else:
            self.login_result = Label(self, text="Login invalid", fg="red")
            self.login_result.grid(row=5, column=1, sticky=W)

    def register(self):
        self.master.show_frame(RegisterWindow)

    def pack(self):
        self.title.grid(row=0, column=0, pady=(20, 10), columnspan=3)
        self.username_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 5))
        self.username.grid(row=1, column=1, pady=(0, 5))
        self.password_label.grid(row=2, column=0, padx=(20, 0))
        self.password.grid(row=2, column=1)
        self.login.grid(row=3, column=1, sticky=E)
        self.register.grid(row=4, column=1, sticky=E)

    # called to build the window and control the main loop
    def run(self):
        self.build()
        self.pack()

# Register New User Page
class RegisterWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master
        self.output = Label(self)
        self.register_result = Label(self)

        self.run()

    def build(self):
        # title
        self.title = Message(self, text="Register User", width=400, font=TITLE_FONT, justify=CENTER)

        # username input
        self.username_label = Label(self, text="Username")
        self.username = Entry(self)

        # password input
        self.password_label = Label(self, text="Password")
        self.password = Entry(self, show="\u2022")

        # password input
        self.password2_label = Label(self, text="Retype password")
        self.password2 = Entry(self, show="\u2022")

        # back button
        self.back = Button(self, text="Back", command=self.back)

        # register button
        self.register = Button(self, text="Register", command=self.register)

    # called whenever this frame is set as the active frame
    def set_active(self):
        self.master.title("Register new user")

    def back(self):
        self.clear()
        self.master.show_frame(LoginWindow)

    def clear(self):
        self.username.delete(0,'end')
        self.password.delete(0,'end')
        self.password2.delete(0, 'end')

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
            self.clear()
            new_user = {'username': u_input, 'password': p_input}
            with open('database.json') as file:
                data = json.load(file)
                data["login_info"].append(new_user)
            with open('database.json', 'w') as file:
                json.dump(data, file, indent=2)

        self.register_result.grid(row=5, column=0, columnspan=2)

    def pack(self):
        self.title.grid(row=0, column=0, pady=(20, 10), columnspan=3)
        self.username_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 5))
        self.username.grid(row=1, column=1, pady=(0, 5))
        self.password_label.grid(row=2, column=0, padx=(20, 0))
        self.password.grid(row=2, column=1)
        self.password2_label.grid(row=3, column=0, padx=(20, 0))
        self.password2.grid(row=3, column=1)
        self.back.grid(row=4, column=1, sticky=W)
        self.register.grid(row=4, column=1, sticky=E)

    def run(self):
        self.build()
        self.pack()

# Main Application Page (After Login Success)
class ApplicationWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master
        self.output = Label(self)
        self.register_result = Label(self)
        self.user = None

        self.username = Label(self)
        self.run()

    def build(self):
        # title
        self.title = Message(self, text="Main Application", width=400, font=TITLE_FONT, justify=CENTER)

        # buttons
        self.logout = Button(self, text="Logout", command=self.logout)
        self.change_password = Button(self, text="Change Password", command=self.change_password)

        # called whenever this frame is set as the active frame

    def set_active(self):
        self.master.title("Main Application")

    # called when user clicks Logout button
    def logout(self):
        self.master.show_frame(LoginWindow)

    # called when user clicks Change Password button
    def change_password(self):
        self.master.frames[ChangePasswordWindow].set_user(self.user)
        self.master.show_frame(ChangePasswordWindow)

    # called upon successful login from the login page
    def set_user(self, user):
        self.user = user
        self.username.destroy()
        self.username = Label(self, text="Welcome, " + self.user + "!")
        self.username.grid(row=1, column=0, pady =(0, 20))

    def pack(self):
        self.title.grid(row=0,column=0, padx = 50)
        self.logout.grid(row=2,column=0)
        self.change_password.grid(row=3,column=0)

    def run(self):
        self.build()
        self.pack()

class ChangePasswordWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master
        self.user = None
        self.result = Label(self)
        self.run()

    def build(self):
        # title
        self.title = Message(self, text="Change Password", width=400, font=TITLE_FONT, justify=CENTER)

        # confirm old password input
        self.confirm_label = Label(self, text="Confirm Old Password")
        self.confirm = Entry(self, show="\u2022")

        # password input
        self.password_label = Label(self, text="New Password")
        self.password = Entry(self, show="\u2022")

        # password input
        self.password2_label = Label(self, text="Retype password")
        self.password2 = Entry(self, show="\u2022")

        # back button
        self.back = Button(self, text="Back", command=self.back)

        # update button
        self.update = Button(self, text="Update", command=self.update)

    def set_active(self):
        self.master.title("Change Password")

    def set_user(self, user):
        self.user = user

    def update(self):
        old_input = self.confirm.get()
        p_input = self.password.get()
        p2_input = self.password2.get()
        valid_old_pass = False

        with open("database.json", "r") as file:
            data = json.loads(file.read())
        for profile in data["login_info"]:
            if self.user == profile['username']:
                if old_input == profile['password']:
                    valid_old_pass = True

        # display result message and update the JSON if valid
        self.result.destroy()
        if not valid_old_pass:
            self.result = Label(self, text="Old password incorrect", fg="red")
        elif p_input != p2_input:
            self.result = Label(self, text="Passwords do not match", fg="red")
        elif len(p_input) < 6:
            self.result = Label(self, text="Password must be 6+ characters", fg="red")
        else:
            self.result = Label(self, text="Password changed successfully", fg="green")
            self.clear()
            with open('database.json') as file:
                data = json.load(file)
                for profile in data['login_info']:
                    if self.user == profile['username']:
                        profile['password'] = p_input
            with open('database.json', 'w') as file:
                json.dump(data, file, indent=2)

        self.result.grid(row=5, column=0, columnspan=2, sticky=E)

    def back(self):
        self.clear()
        self.master.show_frame(ApplicationWindow)

    def clear(self):
        self.confirm.delete(0, 'end')
        self.password.delete(0, 'end')
        self.password2.delete(0, 'end')

    def pack(self):
        self.title.grid(row=0, column=0, pady=(20, 10), columnspan=3)
        self.confirm_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 5))
        self.confirm.grid(row=1, column=1, pady=(0, 5))
        self.password_label.grid(row=2, column=0, padx=(20, 0))
        self.password.grid(row=2, column=1)
        self.password2_label.grid(row=3, column=0, padx=(20, 0))
        self.password2.grid(row=3, column=1)
        self.back.grid(row=4, column=1, sticky=W)
        self.update.grid(row=4, column=1, sticky=E)

    def run(self):
        self.build()
        self.pack()

m=App()
m.mainloop()