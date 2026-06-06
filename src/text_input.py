import tkinter as tk
from tkinter import simpledialog


def get_input():
    # Hide the main tkinter root window
    root = tk.Tk()
    root.withdraw()

    # Create the popup window
    user_input = simpledialog.askstring("Input", "Enter your text:")

    # Return the input
    if user_input:
        return user_input
    else:
        print("User cancelled or entered nothing.")
        return None

def display_question(text, image):
    pass