from tkinter import *

#UI class
class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("500x500")
        self.resizable(False, False)
        self.output = Label(self)
        self.title("Password Generator")

    #builds all widgets and adds them to the window
    def build(self):
        #title
        self.title = Message(self, text="Login Screen", width=400, font=("Helvitica", 20), justify=CENTER)

        #username input
        self.username_label = Label(self, text="Username")
        self.username = Entry(self)

        #password input
        self.password_label = Label(self, text="Password")
        self.password = Entry(self)

        #login button
        self.login = Button(self, text="Login", command=self.login)

    def pack(self):
        self.title.grid(row=0, column=0, pady=(20, 10), columnspan=3)
        self.username_label.grid(row=1,column=0, padx=(20,0), pady=(0,5))
        self.username.grid(row=1,column=1, pady=(0,5))
        self.password_label.grid(row=2, column=0, padx=(20, 0))
        self.password.grid(row=2, column=1)
        self.login.grid(row=3,column=1, sticky=E)

    def login(self):
        print("login attempted")
        print("u: " + self.username.get())
        print("p: " + self.password.get())

    #called to build the window and control the main loop
    def run(self):
        self.build()
        self.pack()
        self.mainloop()

win = Window()
win.run()