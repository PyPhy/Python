import tkinter as tk

root = tk.Tk()
root.title('Mo')
root.geometry('300x300')
root.resizable( width = False, height = False)

entry = tk.Entry(root)
entry.place(x = 50, y = 0)

# .get() will get the information from entry
# .insert() will add information to entry
def get_name():
    print(entry.get())
    entry.insert(0, 'My name is: ')

label = tk.Label(root, text = 'Name: ')
label.place(x = 0, y = 0)

btn = tk.Button(root, text = 'get Name', command = lambda: get_name() )
btn.place(x = 100, y = 100)

root.mainloop()