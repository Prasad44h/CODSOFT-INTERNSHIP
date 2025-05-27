import tkinter as tk
from tkinter import messagebox

def perform_operation(op):
    try:
        num1=float(entry1.get())
        num2=float(entry2.get())

        if op =='+':
            result = num1+num2
        elif op =='-':
             result = num1-num2
        elif op =='*':
             result = num1*num2
        elif op =='/':
            if num2 ==0:
                messagebox.showerror("Error","Division by zero is not allowed.")
                return
            result=num1/num2
        else:
            messagebox.showerror("error","invalid operation.")
            return
        
        result_label.config(text=f"result:{result}")
    except ValueError:
        messagebox.showerror("error","please enter valid numeric values.")

#GUI setup
window=tk.Tk()
window.title("simple calculator")
window.geometry("300x300")
window.resizable(False,False)
window.config(bg="white")


tk.Label(window,text="enter first number:",bg="white",fg="black").pack(pady=5)
entry1=tk.Entry(window,font=("Arial",14),bg="white",fg="black",bd=2,relief=tk.SOLID)
entry1.pack()

tk.Label(window,text="enter second number:",bg="white",fg="black").pack(pady=5)
entry2=tk.Entry(window,font=("Arial",14),bg="white",fg="black",bd=2,relief=tk.SOLID)
entry2.pack()


frame=tk.Frame(window,bg="white")
frame.pack(pady=10)


for symbol in ['+','-','*','/']:
    btn=tk.Button(frame,text=symbol,width=5,height=2,font=("Arail",14),bg="blue",fg="white",activebackground="#00008B",activeforeground="white",
                  command=lambda op=symbol:perform_operation(op))
    btn.pack(side=tk.LEFT,padx=5) 



result_label=tk.Label(window,text="result:",font=("arial",14),bg="white",fg="black")
result_label.pack(pady=20)

window.mainloop()
