import tkinter as tk

root = tk.Tk()
root.geometry('800x500')
root.title('Run Python Code')
color = 'gray'
root.configure(bg = color)
root.resizable(width = False, height = False)

top = tk.Frame(root, width = 800, height = 50, bg = 'black')
top.pack(side = tk.TOP)

bottom = tk.Frame(root, width = 800, height = 500, bg = 'red')
bottom.pack(side = tk.BOTTOM)



root.mainloop()