from tkinter import *
from tkinter import ttk, messagebox
from random import choice
from string import digits, punctuation
import pandas as pd
from pathlib import Path
from cryptography.fernet import Fernet

# Creates a blank password string
pw = ''
# saves the filepaths of all relevant files
words_list = Path(__file__).with_name('words.txt')
saved_list = Path(__file__).with_name('saved.csv')
readme = Path(__file__).with_name('README.txt')
saved_key = Path(__file__).with_name('filekey.key')
words = open(words_list, "r").readlines()
# Remove newline characters from each word
words = [word.strip() for word in words]

while True:
# Tries to open the key file
    try:
        with open(saved_key, 'rb') as f:
            key = f.read()
        fernet = Fernet(key)
        break
# Creates a new encryption key and saves it to a file if one does not exist
    except:
        key = Fernet.generate_key()
        with open(saved_key, 'wb') as f:
            f.write(key)

# Decrypts saved.csv
def decrypt():
    with open(saved_list, 'rb') as f:
        encrypted = f.read()

    decrypted = fernet.decrypt(encrypted)

    with open(saved_list, 'wb') as f:
        f.write(decrypted)

# Encrypts saved.csv
def encrypt():
    with open(saved_list, 'rb') as f:
        original = f.read()
    encrypted = fernet.encrypt(original)
    with open(saved_list, 'wb') as f:
        f.write(encrypted)

# Tries to open the list of saved passwords
try:
    open(saved_list, 'r')
# Creates and encrypts new list of saved passwords if it does not exist
except:
    with open(saved_list, 'w') as f:
        f.write('application,password')
    encrypt()

def new_pass():
    global pw
    pw = ""
# Generates 3 words from words.txt
    for i in range(3):
        word = choice(words).capitalize()
        pw += word
# Generates a random digit
    random_number = choice(digits)
# Generates a random symbol that is not a comma or bracket of any kind
    while True:
        random_symbol = choice(punctuation)
        if random_symbol in {',', '(', ')', '[', ']', '{', '}'}:
            continue
        break
# Adds the number and symbol to the end of the 3 random words
    pw += random_number
    pw += random_symbol
    pass_label.config(text='Your new password: ' + pw)

# Copies password to clipboard
def copy_to_clipboard():
# Clears clipboard
    passgen.clipboard_clear()
# Saves last generated password to clipboard
    passgen.clipboard_append(pw)
    passgen.update()
    messagebox.showinfo('Copy to Clipboard','Password copied!')

# Password generator menu
def pass_gen():
    global pass_label
    global passgen
    passgen = Toplevel(root)
    passgen.title('LockSmith PassGen')
    passgen.geometry('350x150')
# Makes window un-rezisable
    passgen.resizable(False, False) 

    ttk.Label(passgen, text="Password Generator", font=("Arial", 16)).pack()
# Button to generate new password
    ttk.Button(passgen, text="Generate Password", command=new_pass).pack()
# Label to display generated password
    pass_label = ttk.Label(passgen, text="")
    pass_label.pack()
# Button to copy displayed password to clipboard
    ttk.Button(passgen, text="Copy to Clipboard", command=copy_to_clipboard).pack()
    ttk.Button(passgen, text="Back", command= passgen.destroy).pack()

    passgen.mainloop()

# Saves password to saved.csv
def save_pass():
    decrypt()
    df = pd.read_csv(saved_list)
    application = app_entry.get()
    password = pass_entry.get()
# Checks both fields have an input
    if application == '' or password == '':
        messagebox.showerror('Error', 'An application name and password is required before saving!')
# Checks application exists in saved.csv
    elif application in df['application'].values:
        overwrite = messagebox.askyesno("Overwrite?", f"Password for '{application}' already exists! Would you like to overwrite this password?")
        if overwrite:
            confirm = messagebox.askyesno("Overwrite?",f"Are you sure you wish to overwrite the password for '{application}'?")
# Overwrites existing password 
            if confirm:
                df.loc[df['application'] == application, 'password'] = password
                df.to_csv(saved_list, index=False)
                messagebox.showinfo("Overwrite Successful", f"Password for '{application}' overwritten.")
            else:
                messagebox.showinfo("Overwrite Cancelled", "Password was not changed.")
        else:
            messagebox.showinfo("Overwrite Cancelled", "Password was not changed.")
    else:
# Saves new password
        new_row = pd.DataFrame([[application, password]], columns=['application', 'password'])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(saved_list, index=False)
        messagebox.showinfo("Saved", f"Password for '{application}' saved.")
    encrypt()
      
# Displays existing password from saved.csv to user
def get_pass():
    decrypt()
    df = pd.read_csv(saved_list)
    application = app_entry.get()
# Displays password if application input exists in saved.csv
    try:
        stored_password = df.loc[df['application'] == application, 'password'].values[0]
        messagebox.showinfo("Your Password", f"Password for '{application}' is '{stored_password}'.")
# Error if application does not exist
    except:
        messagebox.showerror('Error', 'No password found for this application!')
    encrypt()

# Deletes a password from saved.csv
def del_pass():
    decrypt()
    df = pd.read_csv(saved_list)
    application = app_entry.get()
    password = pass_entry.get()
# Checks  both fields have an input
    if application == '' or password == '':
        messagebox.showerror('Error', 'An application name and password is required to delete passwords!')
    elif application not in df['application'].values:
        messagebox.showerror('Error', f"No password found for '{application}'!")
# Checks input password matches saved password 
    else:
        stored_password = df.loc[df['application'] == application, 'password'].values[0]
        if password != stored_password:
            messagebox.showerror('Error', f"Password input does not match stored password for '{application}'!")
        else:
            confirm = messagebox.askyesno("Delete?",f"Are you sure you wish to delete the password for '{application}'?")
# Deletes application and password
            if confirm:
                df = df[df['application'] != application]
                df.to_csv(saved_list, index=False)
                messagebox.showinfo("Deleted", f"Password for '{application}' has been deleted.")
            else:
                messagebox.showinfo("Cancelled", "Password deletion cancelled.")
    encrypt()

# Window to display contents of  README.txt to user
def help():
    help_window = Toplevel(root)
    help_window.title(readme)
    help_window.resizable(False, False)
    help_text = Text(help_window, wrap='word', height=20, width=67)
# Reads file and writes the content to help_text
    with open(readme, 'r') as f:
        content = f.read()
        help_text.delete(1.0, END)
        help_text.insert(END, content)
# Makes text unable to be edited
    help_text.config(state='disabled')
    help_text.pack()

    help_window.mainloop()

# Shows/hides password input
def toggle_password():
# Button will not change states if password entry is empty
    password = pass_entry.get()
    if password == '':
        pass
# Gets the state of the password entry's show option, meaning what character the text is replaced with
# If show is blank, pressing the button will change it to *, and the text of the button to Show Password
    elif pass_entry.cget('show') == '':
        pass_entry.config(show='*')
        toggle_button.config(text='Show Password')
# If show is *, pressing the button will make it blanl, and change the text of the button to Hide Password
    else:
        pass_entry.config(show='')
        toggle_button.config(text='Hide Password')

# Main menu window
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
# Entry box for application and password
    ttk.Label(root, text='Application:').grid(column=0, row=1)
    app_entry = ttk.Entry(root, width=50)
    app_entry.grid(column=1, row=1)
    ttk.Label(root, text='Password:').grid(column=0, row=2)
    pass_entry = ttk.Entry(root, width=50, show='*')
    pass_entry.grid(column=1, row=2)
# Button to show/hide password
    toggle_button = ttk.Button(root, text='Show Password', command=toggle_password)
    toggle_button.grid(column=2, row=2)
# Options
    ttk.Button(root, text="Save Password", command=save_pass).grid(column=0, row=3)
    ttk.Button(root, text="Retrieve Password", command=get_pass).grid(column=1, row=3)
    ttk.Button(root, text="Delete Password", command=del_pass).grid(column=2, row=3)
    ttk.Button(root, text="Password Generator", command=pass_gen).grid(column=1, row=4)
    ttk.Button(root, text="Help", command=help).grid(column=0, row=5)
# Clears the clipboard and exits the program
    ttk.Button(root, text='Exit', command= lambda: [root.clipboard_clear(), root.destroy()]).grid(column=2, row=5)

    root.mainloop()
menu()