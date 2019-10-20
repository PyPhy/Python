#!/usr/bin/env python3

import tkinter as tk

root = tk.Tk()
root.title('Food price')
root.geometry('300x200')
root.resizable( width = False, height = False)
root.configure( bg = 'gray77')                   # color of background

v = tk.IntVar()
res = tk.IntVar()

def Cal_price():
    value = int(v.get() )
    
    if value == 0:
        res.set(int(entry_2.get())* 5)
    elif value == 1:
        res.set(int(entry_2.get())* 6)
    elif value == 2:
        res.set(int(entry_2.get())* 7)
    elif value == 3:
        res.set(int(entry_2.get())* 8)
    elif value == 4:
        res.set(int(entry_2.get())* 9)
    elif value == 5:
        res.set(int(entry_2.get())* 10)


label = tk.Label(root, text = 'Choose An Item', bg = 'gray77')
label.place(x = 100, y = 5)

#%% Radio buttons
r_btn = tk.Radiobutton(root, text = 'Banana', bg = 'gray77', variable = v, value = 0)
r_btn.place(x = 5, y = 30)

r_btn_2 = tk.Radiobutton(root, text = 'Apple', bg = 'gray77', variable = v, value = 1)
r_btn_2.place(x = 5, y = 60)

r_btn_3 = tk.Radiobutton(root, text = 'Orange', bg = 'gray77', variable = v, value = 2)
r_btn_3.place(x = 5, y = 90)

r_btn_4 = tk.Radiobutton(root, text = 'Rise', bg = 'gray77', variable = v, value = 3)
r_btn_4.place(x = 150, y = 30)

r_btn_5 = tk.Radiobutton(root, text = 'Mango', bg = 'gray77', variable = v, value = 4)
r_btn_5.place(x = 150, y = 60)

r_btn_6 = tk.Radiobutton(root, text = 'kivi', bg = 'gray77', variable = v, value = 5)
r_btn_6.place(x = 150, y = 90)


#%% Display the result
entry = tk.Entry(root, width = 25, textvariable = res)
entry.place(x = 80, y = 130)

label_res = tk.Label(root, text = 'Price', bg = 'gray77')
label_res.place(x = 5, y = 130)


#%%
entry_2 = tk.Entry(root, width = 25)
entry_2.place(x = 80, y = 160)

btn = tk.Button(root, text = 'Cal', highlightbackground = 'gray77', command = lambda: Cal_price() )
btn.place(x = 5, y = 160)


root.mainloop()
