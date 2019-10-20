import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.geometry('500x500')
root.title('File Counter')
color = 'gray77'
root.configure(bg = color)

#%%

# text = 'metal metal metal rock rock in consert'
# text.count('metal') ---> 3

count_result = dict()

def count_text(file):
    file_open = open(str(file), 'r')
    full_text = file_open.readlines()
    file_open.close()
    
    for word in word_list.get().split(', '):
        for text in full_text:
            if word in count_result:
                count_result[word] = count_result[word] + text.count(word) 
            else:
                count_result[word] = text.count(word)
    print(count_result)

def open_file():
    root.filename = filedialog.askopenfilename()

def clear_text():
    word_list.delete(0, tk.END)     # to delete something from Entry write 0, which indicates the first word
    answer.delete('1.0', tk.END)    # to delete something from Text write '1.0', which indicates the first line

#%%
word_list = tk.Entry(root, width = 70)
word_list.place(x = 0, y = 0)

file = tk.Button(root, text = 'select file', width = 65, bg = color,
                 command = lambda: open_file() )
file.place(x = 0, y = 30)

count = tk.Button(root, text = 'Count words', width = 65, bg = color,
                  command = lambda: count_text(root.filename) )
count.place(x = 0, y = 60)

clear = tk.Button(root, text = 'Clear text', width = 65, bg = color,
                  command = lambda: clear_text() )
clear.place(x = 0, y = 90)

answer = tk.Text(root, height = 30, width = 100, bg = color)
answer.place(x = 0, y = 120)



root.mainloop()