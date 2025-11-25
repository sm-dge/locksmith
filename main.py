from tkinter import *
from tkinter import ttk, messagebox
from random import choice
from string import digits, punctuation
import pandas as pd
from pathlib import Path

pw = ''
words_list = Path(__file__).with_name('words.txt')
saved_list = Path(__file__).with_name('saved.csv')
readme = Path(__file__).with_name('README.txt')
words = open(words_list, "r").readlines()
# Remove newline characters from each word
words = [word.strip() for word in words]

try:
    open(saved_list, 'r')
except:
    with open(saved_list, 'w') as f:
        f.write('application,password')

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
    passgen = Toplevel(root)
    passgen.title('LockSmith PassGen')
    passgen.geometry('350x150')
    passgen.resizable(False, False)

    ttk.Label(passgen, text="Password Generator", font=("Arial", 16)).pack()
    ttk.Button(passgen, text="Generate Password", command=new_pass).pack()
    pass_label = ttk.Label(passgen, text="")
    pass_label.pack()
    ttk.Button(passgen, text="Copy to Clipboard", command=copy_to_clipboard).pack()
    ttk.Button(passgen, text="Back", command= passgen.destroy).pack()

    passgen.mainloop()

def save_pass():
    df = pd.read_csv(saved_list)
    application = app_entry.get()
    password = pass_entry.get()
    if application == '' or password == '':
        messagebox.showerror('Error', 'An application name and password is required before saving!')
    
    elif application in df['application'].values:
        overwrite = messagebox.askyesno("Overwrite?", f"Password for '{application}' already exists! Would you like to overwrite this password?")
        if overwrite:
            confirm = messagebox.askyesno("Overwrite?",f"Are you sure you wish to overwrite the password for '{application}'?")
            if confirm:
                df.loc[df['application'] == application, 'password'] = password
                df.to_csv(saved_list, index=False)
                messagebox.showinfo("Overwrite Successful", f"Password for '{application}' overwritten.")
            else:
                messagebox.showinfo("Overwrite Cancelled", "Password was not changed.")
        else:
            messagebox.showinfo("Overwrite Cancelled", "Password was not changed.")

    else:
        new_row = pd.DataFrame([[application, password]], columns=['application', 'password'])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(saved_list, index=False)
        messagebox.showinfo("Saved", f"Password for '{application}' saved.")
      

def get_pass():
    df = pd.read_csv(saved_list)
    application = app_entry.get()
    try:
        stored_password = df.loc[df['application'] == application, 'password'].values[0]
        messagebox.showinfo("Your Password", f"Password for '{application}' is '{stored_password}'.")
    except:
        messagebox.showerror('Error', 'No password found for this application!')


def del_pass():
    df = pd.read_csv(saved_list)
    application = app_entry.get()
    password = pass_entry.get()
    if application == '' or password == '':
        messagebox.showerror('Error', 'An application name and password is required to delete passwords!')
    elif application not in df['application'].values:
        messagebox.showerror('Error', f"No password found for '{application}'!")
    else:
        stored_password = df.loc[df['application'] == application, 'password'].values[0]
        if password != stored_password:
            messagebox.showerror('Error', f"Password input does not match stored password for '{application}'!")
        else:
            confirm = messagebox.askyesno("Delete?",f"Are you sure you wish to delete the password for '{application}'?")
            if confirm:
                df = df[df['application'] != application]
                df.to_csv(saved_list, index=False)
                messagebox.showinfo("Deleted", f"Password for '{application}' has been deleted.")
            else:
                messagebox.showinfo("Cancelled", "Password deletion cancelled.")

def help():
    help_window = Toplevel(root)
    help_window.title(readme)
    help_window.resizable(False, False)
    help_text = Text(help_window, wrap='word', height=20, width=67)
    with open(readme, 'r') as f:
        content = f.read()
        help_text.delete(1.0, END)
        help_text.insert(END, content)
    help_text.config(state='disabled')
    help_text.pack()

def toggle_password():
    password = pass_entry.get()
    if password == '':
        pass
    elif pass_entry.cget('show') == '':
        pass_entry.config(show='*')
        toggle_button.config(text='Show Password')
    else:
        pass_entry.config(show='')
        toggle_button.config(text='Hide Password')

def menu():
    global root
    global app_entry
    global pass_entry
    global toggle_button
    root = Tk()
    root.title('LockSmith Menu')
    root.geometry('500x165')
    root.resizable(False, False)
    
    ttk.Label(root, text="Main Menu", font=("Arial", 16)).grid(column=1, row=0)
    ttk.Label(root, text='Application:').grid(column=0, row=1)
    app_entry = ttk.Entry(root, width=50)
    app_entry.grid(column=1, row=1)
    ttk.Label(root, text='Password:').grid(column=0, row=2)
    pass_entry = ttk.Entry(root, width=50, show='*')
    pass_entry.grid(column=1, row=2)
    toggle_button = ttk.Button(root, text='Show Password', command=toggle_password)
    toggle_button.grid(column=2, row=2)
    ttk.Button(root, text="Save Password", command=save_pass).grid(column=0, row=3)
    ttk.Button(root, text="Retrieve Password", command=get_pass).grid(column=1, row=3)
    ttk.Button(root, text="Delete Password", command=del_pass).grid(column=2, row=3)
    ttk.Button(root, text="Password Generator", command=pass_gen).grid(column=1, row=4)
    ttk.Button(root, text="Help", command=help).grid(column=0, row=5)
    ttk.Button(root, text='Exit', command= lambda: [root.clipboard_clear(), root.destroy()]).grid(column=2, row=5)

    root.mainloop()
menu()