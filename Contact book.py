from tkinter import *
from tkinter import messagebox

root = Tk()
root.geometry('750x500')
root.title("Contact Book")
root.config(bg="#cce7ff")  # soft blue background

# Sample contact list
contacts = [
    ["Arpit", "8976543233"],
    ["Bhuvan", "9876134122"],
    ["chetan", "9988765243"]
]

# Input variables
name_var = StringVar()
number_var = StringVar()

# ---------- Functions ----------
def refresh_listbox():
    contact_listbox.delete(0, END)
    for c in contacts:
        contact_listbox.insert(END, c[0])  # Show only name

def reset_fields():
    name_var.set("")
    number_var.set("")

def get_selected_index():
    selected = contact_listbox.curselection()
    return selected[0] if selected else None

def add_contact():
    name, number = name_var.get().strip(), number_var.get().strip()
    if name and number:
        contacts.append([name, number])
        refresh_listbox()
        reset_fields()
    else:
        messagebox.showwarning("Input Error", "Please enter both name and number.")

def view_contact():
    idx = get_selected_index()
    if idx is not None:
        name_var.set(contacts[idx][0])
        number_var.set(contacts[idx][1])

def update_contact():
    idx = get_selected_index()
    if idx is not None:
        name, number = name_var.get().strip(), number_var.get().strip()
        if name and number:
            contacts[idx] = [name, number]
            refresh_listbox()
            reset_fields()
        else:
            messagebox.showwarning("Input Error", "Both fields must be filled to update.")

def delete_contact():
    idx = get_selected_index()
    if idx is not None:
        del contacts[idx]
        refresh_listbox()
        reset_fields()

# ---------- Layout ----------
title_label = Label(root, text="Contact Book", bg="#cce7ff", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

form_frame = Frame(root, bg="#cce7ff")
form_frame.pack(pady=10)

Label(form_frame, text="Name:", bg="#cce7ff", font=("Helvetica", 14)).grid(row=0, column=0, sticky=W, padx=10, pady=5)
Entry(form_frame, textvariable=name_var, font=("Helvetica", 14), width=30).grid(row=0, column=1, padx=10, pady=5)

Label(form_frame, text="Phone Number:", bg="#cce7ff", font=("Helvetica", 14)).grid(row=1, column=0, sticky=W, padx=10, pady=5)
Entry(form_frame, textvariable=number_var, font=("Helvetica", 14), width=30).grid(row=1, column=1, padx=10, pady=5)

button_frame = Frame(root, bg="#cce7ff")
button_frame.pack(pady=10)

Button(button_frame, text="Add", width=12, command=add_contact).grid(row=0, column=0, padx=5, pady=5)
Button(button_frame, text="View", width=12, command=view_contact).grid(row=0, column=1, padx=5, pady=5)
Button(button_frame, text="Update", width=12, command=update_contact).grid(row=0, column=2, padx=5, pady=5)
Button(button_frame, text="Delete", width=12, command=delete_contact).grid(row=0, column=3, padx=5, pady=5)
Button(button_frame, text="Clear", width=12, command=reset_fields).grid(row=0, column=4, padx=5, pady=5)

list_frame = Frame(root)
list_frame.pack(pady=10)

scrollbar = Scrollbar(list_frame, orient=VERTICAL)
contact_listbox = Listbox(list_frame, font=("Helvetica", 14), width=50, yscrollcommand=scrollbar.set, height=10)
scrollbar.config(command=contact_listbox.yview)

scrollbar.pack(side=RIGHT, fill=Y)
contact_listbox.pack(side=LEFT, fill=BOTH, expand=True)

refresh_listbox()

root.mainloop()

