import json
from pathlib import Path
from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox

import pyperclip

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data.json"
LOGO_FILE = BASE_DIR / "logo.png"
DEFAULT_EMAIL = "your-email@example.com"


# ---------------------------- DATA HELPERS ------------------------------- #
def load_data():
    """Return the saved passwords, or an empty dict if there is no (valid) file yet."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as data_file:
            return json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=4)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)  # Clear previous password
    password_entry.insert(0, password)
    try:
        pyperclip.copy(password)
    except pyperclip.PyperclipException:
        pass  # No clipboard available - the password is still shown in the box


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get()

    if not website or not email or not password:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        return

    data = load_data()
    if website in data:
        overwrite = messagebox.askyesno(
            title=website,
            message=f"There are already details saved for {website}.\nDo you want to replace them?")
        if not overwrite:
            return

    data[website] = {"email": email, "password": password}
    write_data(data)
    messagebox.showinfo(title="Saved", message=f"Details for {website} saved.")
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    website_entry.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().strip()
    if not website:
        messagebox.showinfo(title="Oops", message="Type a website to search for.")
        return

    data = load_data()
    if not data:
        messagebox.showinfo(title="Error", message="No data file found yet - add a password first.")
    elif website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        try:
            pyperclip.copy(password)
            note = "\n\n(Password copied to clipboard)"
        except pyperclip.PyperclipException:
            note = ""
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}{note}")
    else:
        messagebox.showinfo(title="Error", message=f"No details for {website} exist.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200, highlightthickness=0)
logo_img = PhotoImage(file=LOGO_FILE)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="e")
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky="e")
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="e")

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, sticky="ew")
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
email_entry.insert(0, DEFAULT_EMAIL)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="ew")

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="ew")
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="ew")
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2, sticky="ew")

# Enter key saves
window.bind("<Return>", lambda event: save())

window.mainloop()
