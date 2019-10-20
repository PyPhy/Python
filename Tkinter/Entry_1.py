import tkinter as tk

root = tk.Tk()
root.title('App')
root.geometry('300x300')
root.resizable( width = False, height = False)

entry = tk.Entry(root)
entry.place(x = 50, y = 0)

name = tk.StringVar()

def get_name():
    name.set(entry.get())

label = tk.Label(root, text = 'Name: ')
label.place(x = 0, y = 0)

btn = tk.Button(root, text = 'get Name', command = lambda: get_name() )
btn.place(x = 100, y = 100)

label2 = tk.Label(root, textvariable = name)
label2.place(x = 100, y = 200)

root.mainloop()