import tkinter as tk

root = tk.Tk()
root.title("My First App")
root.geometry("300x500")

label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

root.mainloop()
