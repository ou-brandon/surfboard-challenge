# surfboard-challenge

This project should allow clients to communicate in an environment with a group chat and a shared agenda. 

To run this code:
1. Run server.py on one machine to establish an IP address for the server. Enter a port in the terminal to set a terminal.
2. Run client.py on a separate machine.
3. If you are a presenter, check the "Are you presenting?" box. Fill out all the fields (name, server ip address, server port number) properly, then click "Continue."
4. To add agenda items, fill out every field and click "add."
5. To edit/remove items, make sure the name of the task you want to remove matches the text in the "title" field. Afterward, click edit/remove.


Code was used from the following site:
    https://www.geeksforgeeks.org/gui-chat-application-using-tkinter-in-python/

Because of the duration of this project, some features could not be implemented. Some improvements for later include:
- User customization (background pictures, font sizes, etc.)
- Shared Agenda among presenters (For now, presenters have unique task lists)
