# 🔐 Password Manager

A desktop password manager built with Tkinter. Generate strong random passwords, save them with the website and email they belong to, and search for them later. Passwords are copied to your clipboard automatically.

## Features

- Strong random password generator (letters, numbers and symbols)
- Saves logins to a local `data.json` file
- Search for a saved website
- Asks before overwriting existing details
- Auto-copies passwords to the clipboard

## Built with

Python, Tkinter, pyperclip, JSON

## How to run

Requires Python 3.10+.

```bash
pip install -r requirements.txt
python main.py
```

> ⚠️ This is a learning project: passwords are stored as **plain text** in `data.json` on your computer. Don't use it for real passwords. `data.json` is ignored by git so it never gets uploaded.
