import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.geometry('400x150')
root.title('Calculator')
color = 'gray88'
root.configure(bg = color)
root.resizable(width = False, height = False)

#==================================variable=======================================
num1 = tk.IntVar()
num2 = tk.IntVar()
res_value = tk.IntVar()

#==================================Frames=======================================
top_first = tk.Frame(root, width = 800, height = 40, bg = color)
top_first.pack(side = tk.TOP)

top_second = tk.Frame(root, width = 800, height = 40, bg = color)
top_second.pack(side = tk.TOP)

top_third = tk.Frame(root, width = 800, height = 40, bg = color)
top_third.pack(side = tk.TOP)

top_fourth = tk.Frame(root, width = 800, height = 40, bg = color)
top_fourth.pack(side = tk.TOP)

#==================================functions=======================================

def plus():
    try:
        value = float(num1.get()) + float(num2.get())
        res_value.set(value)
    except:
        messagebox.showerror('error')
        
def minus():
    try:
        value = float(num1.get()) - float(num2.get())
        res_value.set(value)
    except:
        messagebox.showerror('error')
        
def mul():
    try:
        value = float(num1.get()) * float(num2.get())
        res_value.set(value)
    except:
        messagebox.showerror('error')
        
def div():
    if num2.get() == '0':
        messagebox.showerror('divisionerror')
    
    try:
        value = float(num1.get()) / float(num2.get())
        res_value.set(value)
    except:
        messagebox.showerror('error')


#==================================Buttons=======================================

btn_plus = tk.Button(top_third, text = '+', width = 8,
                     bg = color, command = lambda: plus() )
btn_plus.pack(side = tk.LEFT, padx = 5, pady = 5)

btn_minus = tk.Button(top_third, text = '-', width = 8, 
                      bg = color, command = lambda: minus())
btn_minus.pack(side = tk.LEFT, padx = 5, pady = 5)

btn_mul = tk.Button(top_third, text = '*', width = 8,
                    bg = color, command = lambda: mul())
btn_mul.pack(side = tk.LEFT, padx = 5, pady = 5)

btn_div = tk.Button(top_third, text = '/', width = 8, 
                    bg = color, command = lambda: div())
btn_div.pack(side = tk.LEFT, padx = 5, pady = 5)


#==================================Entry+Labels=======================================

label_first_num = tk.Label(top_first, text = 'Input Number 1:', bg = color)
label_first_num.pack(side = tk.LEFT, padx = 5, pady = 5)

first_num = tk.Entry(top_first, bg = color, textvariable = num1)
first_num.pack(side = tk.LEFT, padx = 5, pady = 5)

label_second_num = tk.Label(top_second, text = 'Input Number 2:', bg = color)
label_second_num.pack(side = tk.LEFT, padx = 5, pady = 5)

second_num = tk.Entry(top_second, bg = color, textvariable = num2)
second_num.pack(side = tk.LEFT, padx = 5, pady = 5)


res = tk.Label(top_fourth, text = 'Result:', bg = color)
res.pack(side = tk.LEFT, padx = 5, pady = 5)

res_num = tk.Entry(top_fourth, bg = color, textvariable = res_value)
res_num.pack(side = tk.LEFT, padx = 5, pady = 5)







root.mainloop()