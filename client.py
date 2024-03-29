# import all the required  modules
import socket
import threading
from tkinter import *
import sys

# Information needed for connections

# Will add functionality to ask for the port and IP address of the server

FORMAT = "utf-8"

# Initialize client -> this will be formally set during the constructor
client = 0

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
        
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()

        # deafult user type
        self.presenter = False

        # topics dictionary
        self.topics = {} # Maps topic title to a "title - description - estimate time" string
        
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False,
                             height = False)
        self.login.configure(width = 400,
                             height = 500)

        # create check button for checking if someone is presenting
        self.checkVar = IntVar()
        self.checkButton = Checkbutton(self.login, 
                             text = "Are you presenting?",
                             font = "Helvetica 12 bold",
                             variable = self.checkVar, 
                             onvalue = 1, 
                             offvalue = 0, 
                             height = 5,
                             width = 20)
         
        self.checkButton.place(relheight = 0.2,
                             relx = 0.1,
                             rely = 0.08)  

        # create a Label for the login prompt
        self.pls = Label(self.login,
                       text = "Please login to continue",
                       justify = LEFT,
                       font = "Helvetica 12 bold")
         
        self.pls.place(relheight = 0.15,
                       relx = 0.1,
                       rely = 0.25)

         
        # create a entry box for
        # typing the message      
        # create a label for the name entry
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 10")
         
        self.labelName.place(relheight = 0.1,
                             relx = 0.15,
                             rely = 0.4)
         
        # create a entry box for typing the message
        self.entryName = Entry(self.login,
                             font = "Helvetica 10")
         
        self.entryName.place(relwidth = 0.2,
                             relheight = 0.1,
                             relx = 0.35,
                             rely = 0.4)
        # Begin IP Field Creation
        self.ipLabel = Label(self.login,
                               text = "Server\nIP Address: ",
                               font = "Helvetica 10")
         
        self.ipLabel.place(relheight = 0.1,
                             relx = 0.1,
                             rely = 0.54)
         
        # create a entry box for typing the message
        self.ipEntry = Entry(self.login,
                             font = "Helvetica 10")
         
        self.ipEntry.place(relwidth = 0.2,
                             relheight = 0.07,
                             relx = 0.35,
                             rely = 0.55)
        # End IP Field Creation
        # Begin Port Field Creation
        self.portLabel = Label(self.login,
                               text = "Server\nPort Number: ",
                               font = "Helvetica 10")
         
        self.portLabel.place(relheight = 0.1,
                             relx = 0.1,
                             rely = 0.65)
         
        # create a entry box for typing the message
        self.portEntry = Entry(self.login,
                             font = "Helvetica 10")
         
        self.portEntry.place(relwidth = 0.2,
                             relheight = 0.07,
                             relx = 0.35,
                             rely = 0.68)

        # End Port Field Creation
        # set the focus of the cursor
        self.entryName.focus()
        
        # create a continue button to proceed to the main screen
        self.go = Button(self.login,
                         text = "Continue",
                         font = "Helvetica 10 bold",
                         command = lambda: self.goAhead(self.entryName.get(), self.checkVar.get()))
        
        self.go.place(relx = 0.1,
                      rely = 0.8)
        self.Window.mainloop()

    # Checks if the user is presenting
    # If they are a presenter, they will receive two (1, 2) windows
    # 1 is for the group chat box and a shared agenda
    # 2 is only for presenters and allows them to edit the agenda and send the updated agenda to all users
    def goAhead(self, name, acheckvar):
        
        # Checks if the user is a presenter
        if acheckvar == 1:
            self.presenter = True
        
        # Connect to the server
        global client
        SERVER = self.ipEntry.get()
        PORT = int(self.portEntry.get())
        ADDRESS = (SERVER, PORT)
        try:
            client = socket.socket(socket.AF_INET,
                        socket.SOCK_STREAM)
            client.connect(ADDRESS)
        except:
            print("An error occurred")
            sys.exit(0)

        # Remove login screen
        self.login.destroy()

        # Invokes a method that generates the agenda-creating window
        if self.presenter:
            self.topic()

        self.layout(name)
         
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()
    
    # Generates the agenda-creating window
    def topic (self):
        self.topic = Toplevel()
        # set the title
        self.topic.title("Topic Work Window")

        self.topic.resizable(width = True,
                             height = True)
        self.topic.configure(width = 400,
                             height = 400)
        # create title
        
        self.topic_title_label = Label(self.topic,
                       text = "Task Title",
                       justify = LEFT,
                       font = "Helvetica 12 bold")
         

        self.topic_title_label.place(relheight = 0.1,
                       relx = 0.1,
                       rely = 0.1)

        # create a entry box for typing the message
        self.topic_title_entry = Entry(self.topic,
                             font = "Helvetica 12",
                             width = 10)
         
        self.topic_title_entry.place(relwidth = 0.4,
                             relheight = 0.1,
                             relx = 0.5,
                             rely = 0.1)

        # Begin Description label
        self.topic_description_label = Label(self.topic,
                       text = "Task \n Description",
                       justify = LEFT,
                       font = "Helvetica 12 bold")
         

        self.topic_description_label.place(relheight = 0.1,
                       relx = 0.1,
                       rely = 0.3)

        # End Description Label
        # Begin Description Entry
        self.topic_description_entry = Entry(self.topic,
                             font = "Helvetica 12",
                             width = 10)
         
        self.topic_description_entry.place(relwidth = 0.4,
                             relheight = 0.15,
                             relx = 0.5,
                             rely = 0.3)
        # End Description Entry 
        # create estimated time label and entry widgets
        # Label for estimated time
        self.topic_time_label = Label(self.topic,
                       text = "Estimated Time",
                       justify = LEFT,
                       font = "Helvetica 12 bold")
         

        self.topic_time_label.place(relheight = 0.1,
                       relx = 0.1,
                       rely = 0.55)
        
        # create a entry box for typing the message
        self.topic_time_entry = Entry(self.topic,
                             font = "Helvetica 12",
                             width=10)
         
        self.topic_time_entry.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.5,
                             rely = 0.55)
        # end estimated time creation

        # create the Add, Edit, and Delete Buttons
        # These modify the agenda
        # The Add the Edit buttons invoke the same method to update the agenda
        self.add = Button(self.topic,
                         text = "Add",
                         font = "Helvetica 12 bold",
                         command = lambda: self.goAdd_Edit(self.topic_title_entry.get(), self.topic_description_entry.get(), self.topic_time_entry.get()))
         
        self.add.place(relx = 0.1,
                      rely = 0.75) 
        
        self.edit = Button(self.topic,
                         text = "Edit",
                         font = "Helvetica 12 bold",
                         command = lambda: self.goAdd_Edit(self.topic_title_entry.get(), self.topic_description_entry.get(), self.topic_time_entry.get()))
          
        self.edit.place(relx = 0.3,
                      rely = 0.75)

        self.delete = Button(self.topic,
                         text = "Delete",
                         font = "Helvetica 12 bold",
                         command = lambda: self.goDelete(self.topic_title_entry.get()))
          
        self.delete.place(relx = 0.5, rely = 0.75)

        # Resend button lets the presenter resend the agenda to new members joining the meeting
        # or if they do not have the updated agenda
        self.resend = Button(self.topic,
                         text = "Resend",
                         font = "Helvetica 12 bold",
                         command = lambda: self.updateAgenda())
          
        self.resend.place(relx = 0.75,
                      rely = 0.75)

    # Updates the agenda for everyone
    def updateAgenda(self):
        message = ""
        
        # Loops through all the current topics in the agenda
        for k, task in self.topics.items():
            #print(sub_dict)
            message += ("Title: " + task[0] + "\nDescription: " + task[1] + "\nEst. Time: " + task[2] + "\n------------------------\n")   
        
        # Adding ***AGENDA*** allows one to figure out if the message should be added to the agenda or chat box
        self.msg="***AGENDA***" + message + "***AGENDA***"
        snd= threading.Thread(target = self.sendMessage)
        snd.start()

    # Adds/Edits the topic with title, which is what the variable title is
    def goAdd_Edit(self, title, description, time):
        self.topics[title] = [title, description, time]
        self.updateAgenda()

    # Deletes the topic with the same title as atitle
    def goDelete(self, atitle):
        self.topics.pop(atitle)
        self.updateAgenda()

    # end of topic

    # The main layout of the chat
    def layout(self,name):
       
        self.name = name
        # handle window closing
        def on_closing():
            client.close()
            sys.exit()

        self.Window.protocol("WM_DELETE_WINDOW", on_closing) 
        # to show chat window
        self.Window.deiconify()
        self.Window.title("Chat Room")
        self.Window.resizable(width = True, height = True)
        self.Window.configure(width = 470, height = 550, bg = "#17202A")
        self.labelHead = Label(self.Window, bg = "#17202A", fg = "#EAECEE",  text = "Meeting Agenda" , font = "Helvetica 13 bold", pady = 5)
         
        self.labelHead.place(relwidth = 1, relheight=0.1)
        self.line = Label(self.Window, width = 450, bg = "#ABB2B9")
         
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)
        # Agenda Text box
        self.textAgenda = Text(self.Window,
                             width = 30,
                             height = 5,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
        
        self.textAgenda.place(relheight = 0.3,
                            relwidth = 1,
                            rely = 0.08)
        
        # Labels the chat box
        self.labelBottomA = Label(self.Window,
                                 bg = "#17202A",
                                 fg = "#EAECEE",
                                 height = 3,
                                 font = "Helvetica 13 bold",
                                 text = "Chat Box")
         
        self.labelBottomA.place(relwidth = 1,
                               rely = 0.41)
        # Extra line for aesthetic purpoess
        self.line2 = Label(self.Window, width = 450, bg = "#ABB2B9")
        self.line2.place(relwidth = 1, rely = 0.49, relheight = 0.012)
        # create a Update Button

        # create a scroll bar for the agenda
        # place the scroll bar into the gui window
        self.agendaScrollbar = Scrollbar(self.textAgenda)
         

        self.agendaScrollbar.place(relheight = 1,
                        relx = 0.974)
        
        self.agendaScrollbar.config(command = self.textAgenda.yview)
        self.textAgenda.config(yscrollcommand=self.agendaScrollbar.set)

        self.textAgenda.config(state = DISABLED)    
        
        # Text console for all users
        self.textCons = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
         
        self.textCons.place(relheight = 0.4,
                            relwidth = 1,
                            rely = 0.5)
        
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
         
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
        
        # Allows users to input chat messages
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
         
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
         
        self.entryMsg.focus()
         
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
        
        self.buttonMsg.place(relx = 0.7,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)
         
        self.textCons.config(cursor = "arrow")
         
        # create a scroll bar
        self.chatScrollbar = Scrollbar(self.textCons)
         
        # place the scroll bar
        # into the gui window
        self.chatScrollbar.place(relheight = .8,
                        relx = 0.974)
        
        self.chatScrollbar.config(command = self.textCons.yview)
        
        self.textCons.config(yscrollcommand=self.chatScrollbar.set)
        self.textCons.config(state = DISABLED)
 
    # Function for the send button
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd= threading.Thread(target = self.sendMessage)
        snd.start()
 


    # Function to receive messages
    # Handles several possible errors such as disconnecting from the server
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == "": # server is down
                    client.close()
                    break

                 
                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                elif message.find("***AGENDA***") > 0:
                    message = message.replace("***AGENDA***","")
                    #remove send name
                    if message.find(":") > 0:
                        message = message[message.find(":") + 1:]
                    message = message.strip()
                    self.textAgenda.config(state = NORMAL)
                    # remove old text
                    self.textAgenda.delete('1.0', END)
                    # insert new adgenda
                    self.textAgenda.insert(END, message+"\n\n")
                    self.textAgenda.config(state = DISABLED)
                else:
                    # insert messages to text box
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")
                     
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                client.close()
                break
         
    # Function to send messages
    def sendMessage(self):
        # self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))   
            break   
 
# create a GUI class object
g = GUI()