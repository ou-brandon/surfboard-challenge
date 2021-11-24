
#!/usr/bin/env python3
# https://github.com/joeVenner/Python-Chat-Gui-App
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq
# 172.28.99.184

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tk.END, msg)
        except OSError:  
            break


def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


#
# https://cppsecrets.com/users/218111411511410110199104971141051161049764103109971051084699111109/Python-Tkinter-To-do-List.php

#root = tk.Tk()
#root.title('To-Do List')
#root.geometry("400x250+500+300")

conn = sq.connect('todo.db')
cur = conn.cursor()
cur.execute('create table if not exists tasks (title text)')

task = []
def addTask():
    word = e1.get()
    if len(word) == 0:
        messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        task.append(word)
        cur.execute('insert into tasks values (?)', (word,))
        listUpdate()
        e1.delete(0, 'end')


def listUpdate():
    clearList()
    for i in task:
        t.insert('end', i)


def delOne():
    try:
        val = t.get(t.curselection())
        if val in task:
            task.remove(val)
            listUpdate()
            cur.execute('delete from tasks where title = ?', (val,))
    except:
        messagebox.showinfo('Cannot Delete', 'No Task Item Selected')


def deleteAll():
    mb = messagebox.askyesno('Delete All', 'Are you sure?')
    if mb == True:
        while (len(task) != 0):
            task.pop()
        cur.execute('delete from tasks')
        listUpdate()


def clearList():
    t.delete(0, 'end')


def bye():
    print(task)
    top.destroy()


def retrieveDB():
    while (len(task) != 0):
        task.pop()
    for row in cur.execute('select title from tasks'):
        task.append(row[0])


# ------------------------------- Functions--------------------------------
top = tk.Tk()
top.title("Meeting")

messages_frame = tk.Frame(top)
my_msg = tk.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tk.Scrollbar(messages_frame)  # To see through previous messages.
# this will contain the messages.
msg_list = tk.Listbox(messages_frame, height=20, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# msg_list.pack(side=tk.RIGHT, fill=tk.Y)
#msg_list.place(relx=.7, rely=.2)
msg_list.pack()
messages_frame.pack()

l1 = ttk.Label(top, text='To-Do List')
l2 = ttk.Label(top, text='Enter task title: ')
e1 = ttk.Entry(top, width=21)
t = tk.Listbox(top, height=11, selectmode='SINGLE')
b1 = ttk.Button(top, text='Add task', width=20, command=addTask)
b2 = ttk.Button(top, text='Delete', width=20, command=delOne)
b3 = ttk.Button(top, text='Delete all', width=20, command=deleteAll)
b4 = ttk.Button(top, text='Exit', width=20, command=bye)

retrieveDB()
listUpdate()

# Place geometry
l2.place(x=50, y=50)
e1.place(x=50, y=80)
b1.place(x=50, y=110)
b2.place(x=50, y=140)
b3.place(x=50, y=170)
b4.place(x=50, y=200)
l1.place(x=50, y=10)
t.place(x=220, y=50)
# top.mainloop()

conn.commit()
cur.close()
#

entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#Socket part
#HOST = input('Enter host: ') # Enter host of the server without inverted commas
HOST = "192.168.1.155"
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()  # for start of GUI  Interface