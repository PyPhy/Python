from tkinter import *

root = Tk()
root.title('Add it')
root.geometry('264x226+428+161')
root.resizable( width = False, height = False)

#===============================================================================

num1 = IntVar()
num2 = IntVar()
res_value = IntVar()

#===============================================================================

def plus():
    try:
        value = float(num1.get()) + float(num2.get())
        res_value.set(value)
    except:
        messagebox.showerror('error')

#===============================================================================

Add = Button(root, text = '+', command = lambda: plus())
Add.place(relx=0.42, rely=0.49, height=36, width=37)
Add.configure(activebackground="#d9d9d9")

Entry_1 = Entry(root, textvariable = num1)
Entry_1.place(relx=0.08, rely=0.18,height=47, relwidth=0.36)
Entry_1.configure(background="white")
Entry_1.configure(font="TkFixedFont")
Entry_1.configure(width=96)

Entry_2 = Entry(root, textvariable = num2)
Entry_2.place(relx=0.53, rely=0.18,height=47, relwidth=0.36)
Entry_2.configure(background="white")
Entry_2.configure(font="TkFixedFont")
Entry_2.configure(selectbackground="#c4c4c4")

disp_result = Entry(root, textvariable = res_value)
disp_result.place(relx=0.3, rely=0.71,height=47, relwidth=0.36)
disp_result.configure(background="white")
disp_result.configure(font="TkFixedFont")
disp_result.configure(selectbackground="#c4c4c4")

root.mainloop()
