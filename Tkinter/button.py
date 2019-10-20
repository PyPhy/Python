import tkinter as tk

root = tk.Tk()
root.title('Mo')
# size of window
root.geometry('300x300')
# stop the resizing
root.resizable( width = False, height = False)

#%%
name = tk.StringVar()

def print_name():
    name.set('Mo')

Btn = tk.Button(root, text = 'Click me!', command = lambda: print_name() )
Btn.place(x = 0, y = 0)

label = tk.Label(root, textvariable = name)
label.place(x = 100, y = 100)

#%%
Hello = tk.StringVar()

def print_Hello():
    Hello.set('Hello world')

Btn2 = tk.Button(root, text = 'Click me!', command = lambda: print_Hello() )
Btn2.place(x = 200, y = 0)

label2 = tk.Label(root, textvariable = Hello)
label2.place(x = 100, y = 200)


root.mainloop()