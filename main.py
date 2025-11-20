from tkinter import *
from tkinter import ttk
from random import choice
from string import digits, punctuation

pw = ''
words = open("words.txt", "r").readlines()
# Remove newline characters from each word
words = [word.strip() for word in words]

def new_pass():
    global pw
    pw = ""
    for i in range(3):
        word = choice(words).capitalize()
        pw += word
    random_number = choice(digits)
    random_symbol = choice(punctuation)
    pw += random_number
    pw += random_symbol
    pass_label.config(text='Your new password: ' + pw)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(pw)
    root.update() 
    copy_label.config(text='Copied to Clipboard!')

def pass_gen():
    global pass_label
    global copy_label
    global root
    root = Tk()
    root.title('LockSmith')
    root.geometry('300x150')

    ttk.Label(root, text="Password Generator", font=("Arial", 16)).pack()
    ttk.Button(root, text="Generate Password", command=new_pass).pack()
    pass_label = ttk.Label(root, text="")
    pass_label.pack()
    ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack()
    copy_label = ttk.Label(root, text="")
    copy_label.pack()
    ttk.Label(root, text='Test Ctrl+V:').pack(side=LEFT)
    ttk.Entry(root, width=30).pack(side=LEFT)
    root.mainloop()
pass_gen()

