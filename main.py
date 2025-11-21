from tkinter import *
from tkinter import ttk, messagebox
from random import choice
from string import digits, punctuation
import pandas as pd

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
    while True:
        random_symbol = choice(punctuation)
        if random_symbol in {',', '(', ')', '[', ']', '{', '}'}:
            continue
        break
    pw += random_number
    pw += random_symbol
    pass_label.config(text='Your new password: ' + pw)

def copy_to_clipboard():
    passgen.clipboard_clear()
    passgen.clipboard_append(pw)
    passgen.update()
    messagebox.showinfo('Copy to Clipboard','Password copied!')

def pass_gen():
    global pass_label
    global passgen
    passgen = Tk()
    passgen.title('LockSmith PassGen')
    passgen.geometry('350x175')
    passgen.resizable(False, False)

    ttk.Label(passgen, text="Password Generator", font=("Arial", 16)).pack()
    ttk.Button(passgen, text="Generate Password", command=new_pass).pack()
    pass_label = ttk.Label(passgen, text="")
    pass_label.pack()
    ttk.Button(passgen, text="Copy to Clipboard", command=copy_to_clipboard).pack()
    ttk.Label(passgen, text='Test Ctrl+V:').pack()
    ttk.Entry(passgen, width=50).pack()
    ttk.Button(passgen, text="Exit", command=passgen.destroy).pack()

    passgen.mainloop()
pass_gen()
