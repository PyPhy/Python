import tkinter as tk

# This is tkinter window
root = tk.Tk()

# This is the name of title
root.title('Mo')

#%% To add a text in tkinter app use Label
# this will tell tkinter that where to put the text (or stuff)
# x ---> how far from left
# y ---> how down from top
# x and y are the value of pixels

label = tk.Label(root, text = 'M')
label.place(x = 0, y = 0)

label2 = tk.Label(root, text = 'M')
label2.place(x = 50, y = 40)


root.mainloop()