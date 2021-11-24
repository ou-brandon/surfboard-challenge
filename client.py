# import all the required modules
import socket
import threading
from tkinter import *
# from tkinter import font
# from tkinter import ttk
import sys

# import all functions /
# everything from chat.py file
# from chat import *

PORT = 5000
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):

        # chat window which is currently hidden
        self.Window = Tk()
        def on_closing():
            client.close()
            sys.exit(0)
        self.Window.protocol("WM_DELETE_WINDOW", on_closing)
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # create a Label
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        # set the focus of the cursor
        self.entryName.focus()

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.55)
        
        # self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self, name):

        self.name = name + "@" + str(socket.gethostbyname(socket.gethostname()))
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=True,
                              height=True)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text="Meeting Agenda",
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        # add agenda box
        self.agenda = Text(self.Window,
                             width=20,
                             height=5,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5) 

        self.agenda.place(relheight=0.3,
                            relwidth=1,
                            rely=0.1)        

        self.agendaScrollbar = Scrollbar(self.agenda)
        
        # place the scroll bar
        # into the gui window
        self.agendaScrollbar.place(relheight=1,
                        relx=0.974)

        self.agendaScrollbar.config(command=self.agenda.yview)
        self.agenda.config(yscrollcommand=self.agendaScrollbar.set)                            
        # end agenda
        
        # Begin agenda update button
        
        self.labelTop = Label(self.Window,
                                 bg="#ABB2B0",
                                 height= 10)

        self.labelTop.place(relwidth=1,
                               rely=0.4)

        self.updateButtonMsg = Button(self.labelTop,
                                text="Update Agenda",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B0",
                                command=lambda: self.updateButton(self.agenda.get('1.0',END)))

        self.updateButtonMsg.place(relx=0.77,
                             rely=.01,
                             relheight=0.2,
                             relwidth=0.22)

        # End agenda update button
        
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.45,
                            relwidth=1,
                            rely=0.47)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=60)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.agendaMsg = Entry(self.agenda,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        self.scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        self.scrollbar.place(relheight=1,
                        relx=0.974)

        self.scrollbar.config(command=self.textCons.yview)
        self.textCons.config(yscrollcommand=self.scrollbar.set)
        self.textCons.config(state=DISABLED)
        
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    # function to implement the update agenda button
    def updateButton(self, msg):
        # self.agenda.config(state=DISABLED)
        self.agendaMsg = msg
        snd = threading.Thread(target=self.updateAgenda)
        snd.start()
        

    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)

                # if the messages from the server is NAME send the client's name
                if message == "":
                    message = "Lost Communication to Server"
                    self.textCons.insert(END, message)
                    client.close()
                    break
                elif message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                elif message.startswith("***AGENDA***"):
                    self.agenda.delete('1.0', END)
                    message = message.replace("***AGENDA***", "")
                    self.agenda.insert(END, message)
                else:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message + "\n\n")

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                m = "Lost Communication to Server"
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, m)
                client.close()
                break

    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            try:
                client.send(message.encode(FORMAT))
            except:
                message = "Lost Communication to Server"
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, message)
                client.close()
                break
            break

    # function to update agenda

    def updateAgenda(self):
        while True:
            message = (f"{self.agendaMsg}")
            message = "***AGENDA***" + message
            try:
                client.send(message.encode(FORMAT))
            except:
                message = "Lost Communication to Server"
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, message)
                client.close()
                break
            break

 
# create a GUI class object
g = GUI()
g.Window.mainloop()
