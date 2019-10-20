import tkinter as tk
import tkinter.messagebox
from io import StringIO
import sys

root = tk.Tk()
root.geometry('800x500')
root.title('Run Python Code')
color = 'gray'
root.configure(bg = color)
root.resizable(width = False, height = False)
#%%
def run():
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    exec(python_code.get('1.0', tk.END))
    sys.stdout = old_stdout
    tkinter.messagebox.showinfo('Result', redirected_output.getvalue() )

def clear_python():
    python_code.delete('1.0', tk.END)

#%%
top = tk.Frame(root, width = 800, height = 100, bg = color)
top.pack(side = tk.TOP)

bottom = tk.Frame(root, width = 800, height = 450, bg = color)
bottom.pack(side = tk.BOTTOM)

btn_clear = tk.Button(top, text = 'Clear', bg = color,
                      font = ('arial', 15, 'bold'), command = lambda: clear_python() )
btn_clear.pack(side = tk.TOP)

btn_run = tk.Button(top, text = 'Run', bg = color, 
                    font = ('arial', 15, 'bold'), command =  lambda: run() )
btn_run.pack(side = tk.TOP)

python_code = tk.Text(bottom, font = ('arial', 15, 'bold'), bg = 'gray88')
python_code.pack(side = tk.TOP)


root.mainloop()