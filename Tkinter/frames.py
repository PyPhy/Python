import tkinter as tk

root = tk.Tk()
root.geometry('500x500')

frame1 = tk.Frame(root, width = 250, height = 500, bg = 'red')
frame1.pack(side = tk.LEFT)

frame2 = tk.Frame(root, width = 250, height = 500, bg = 'blue')
frame2.pack(side = tk.RIGHT)


root.mainloop()