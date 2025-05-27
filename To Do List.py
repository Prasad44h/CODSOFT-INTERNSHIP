from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
from datetime import datetime

def add_task():  
    task_string = task_field.get().strip()
    due_time = time_field.get().strip()
    
    if not task_string or not due_time:
        messagebox.showinfo('Error', 'Please enter both task and time.')
        return

    try:
        datetime.strptime(due_time, "%H:%M")
    except ValueError:
        messagebox.showinfo('Error', 'Time must be in HH:MM format.')
        return

    try:
        the_cursor.execute('INSERT INTO tasks (title, due_time) VALUES (?, ?)', (task_string, due_time))
        the_connection.commit()
        tasks.append((task_string, due_time))   
        list_update()    
        task_field.delete(0, 'end')
        time_field.delete(0, 'end')
    except sql.IntegrityError:
        messagebox.showinfo('Error', 'Task already exists.')

def list_update():    
    clear_list()
    tasks.sort(key=lambda x: x[1])
    for task, due in tasks:    
        task_listbox.insert('end', f"{task}  —  [Due: {due}]")
  
def delete_task():  
    try:  
        selected_index = task_listbox.curselection()[0]
        task_title = tasks[selected_index][0]
        tasks.pop(selected_index)
        the_cursor.execute('DELETE FROM tasks WHERE title = ?', (task_title,))
        the_connection.commit()
        list_update()
    except IndexError:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')        
  
def delete_all_tasks():  
    if messagebox.askyesno('Delete All', 'Are you sure?'):    
        tasks.clear()
        the_cursor.execute('DELETE FROM tasks')   
        the_connection.commit()
        list_update()
   
def clear_list():   
    task_listbox.delete(0, 'end')  
  
def close():    
    the_connection.commit()
    the_cursor.close()
    the_connection.close()
    guiWindow.destroy()
    
def retrieve_database():    
    tasks.clear()
    try:
        for row in the_cursor.execute('SELECT title, due_time FROM tasks'):
            tasks.append((row[0], row[1]))
    except sql.OperationalError:
        messagebox.showinfo('Database Error', 'Could not read from table. Recreating table...')
        the_cursor.execute('DROP TABLE IF EXISTS tasks')
        the_cursor.execute('CREATE TABLE tasks (title TEXT UNIQUE, due_time TEXT)')
        the_connection.commit()

if __name__ == "__main__":   
    guiWindow = Tk()   
    guiWindow.title("🗓️ To-Do List with Due Time")  
    guiWindow.geometry("800x550")   
    guiWindow.configure(bg="#EAF2F8")  

    the_connection = sql.connect('listOfTasks.db')   
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT UNIQUE, due_time TEXT)')
    the_connection.commit()

    tasks = []  

    # Header
    header = Label(guiWindow, text="📝 My To-Do List", font=("Segoe UI", 20, "bold"), bg="#EAF2F8", fg="#154360")
    header.pack(pady=20)

    # Main container
    container = Frame(guiWindow, bg="white", bd=2, relief=SOLID, padx=20, pady=20)
    container.pack(padx=20, pady=10, fill=BOTH, expand=True)

    # Input section
    Label(container, text="Task:", font=("Segoe UI", 12), bg="white").grid(row=0, column=0, sticky=W, pady=5)
    task_field = Entry(container, font=("Segoe UI", 12), width=40)
    task_field.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

    Label(container, text="Due Time (HH:MM):", font=("Segoe UI", 12), bg="white").grid(row=1, column=0, sticky=W, pady=5)
    time_field = Entry(container, font=("Segoe UI", 12), width=20)
    time_field.grid(row=1, column=1, sticky=W, pady=5)

    add_button = Button(container, text="➕ Add Task", bg='#1ABC9C', fg="white",
                        font=("Segoe UI", 11, "bold"), command=add_task)
    add_button.grid(row=1, column=2, padx=10, sticky=E)

    # Task list section
    task_listbox = Listbox(container, font=("Segoe UI", 11), width=65, height=10,
                           selectbackground="#AED6F1", selectforeground="black", bg="#FBFCFC")
    task_listbox.grid(row=2, column=0, columnspan=3, pady=20)

    scrollbar = Scrollbar(container)
    scrollbar.grid(row=2, column=3, sticky='ns', padx=(0, 10))
    task_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=task_listbox.yview)

    # Buttons
    del_button = Button(container, text="🗑 Delete Task", bg='#E74C3C', fg="white",
                        font=("Segoe UI", 11, "bold"), command=delete_task)
    del_button.grid(row=3, column=0, pady=10)

    del_all_button = Button(container, text="🧹 Clear All", bg='#5DADE2', fg="white",
                            font=("Segoe UI", 11, "bold"), command=delete_all_tasks)
    del_all_button.grid(row=3, column=1, pady=10)

    exit_button = Button(container, text="🚪 Exit", bg='#7D3C98', fg="white",
                         font=("Segoe UI", 11, "bold"), command=close)
    exit_button.grid(row=3, column=2, pady=10)

    retrieve_database()
    list_update()
    guiWindow.mainloop()

