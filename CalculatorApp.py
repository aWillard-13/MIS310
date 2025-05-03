# Andrew Willard
# Assignment 6
# MIS310
# Calculator

"""
This is an upgraded version of the calculator app we made in class with keyboard button inputs.
proper operator functioning (when the user presses enter, then presses a number, it clears out the entry first.

"""

#import Libraries
import tkinter as tk
from tkinter import StringVar, ttk

last_operator = ""
last_operand = ""

def btn_click(item):
    global expression
    global last_pressed_equal
    # Check if the user pressed "=" previously
    if last_pressed_equal:
        if item.isdigit() or item == '.':
            expression = ""
        last_pressed_equal = False
    expression += str(item)
    input_text.set(expression)

def btn_clear():
    global expression, last_pressed_equal
    expression = ""
    last_pressed_equal = False
    input_text.set("")

def btn_equal():
    global expression, last_pressed_equal, last_operator, last_operand

    if not expression:
        return

    try:
        # Save expression before evaluating
        if not last_pressed_equal:
            last_equation.set(expression)
            result = str(eval(expression))
            input_text.set(result)
            # Save operator and right-hand operand
            for i in range(len(expression)):
                if expression[i] in "+-*/":
                    last_operator = expression[i]
                    last_operand = expression[i+1:]
                    break
            expression = result
            last_pressed_equal = True
        else:
            # Repeat operation with last operator/operand
            if last_operator and last_operand:
                expression = expression + last_operator + last_operand
                last_equation.set(expression)
                result = str(eval(expression))
                input_text.set(result)
                expression = result
    except Exception:
        input_text.set("Error")
        expression = ""
        last_pressed_equal = False


"""
def btn_equal():
    global expression
    global last_pressed_equal
    try:
        result = eval(expression)
        # If the result is an integer, convert it to an integer to remove .0
        if result.is_integer():
            result = int(result)
        input_text.set(result)
        expression = str(result)
        last_pressed_equal = True
    except Exception:
        input_text.set("Error")
        expression = ""
        last_pressed_equal = False
"""

# Handles keyboard input, assigns
def key_handler(event):
    global expression
    key = event.keysym
    char = event.char
    if char.isalpha() and char.lower() not in ('c', 'x'):
        return

    if key == "Return":
        btn_equal()
    elif key in ("BackSpace", "Delete"):
        global expression
        expression = expression[:-1]
        input_text.set(expression)
    elif key == "Escape" or char.lower() == "c":
        btn_clear()
    elif char.lower() == "x":
        btn_click("*")
    elif char in "0123456789+-*/.=.":
        btn_click(char)



# Initialize Tkinter root window
root = tk.Tk()
root.title("Calculator 2.0")

root.resizable(width=False, height=False)
root.configure(bg="#2E2E2E")

# window size and location
window_width, window_height = 320, 500
root.geometry(f"{window_width}x{window_height}")
monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()
y_move = 2.5
x_move = 2
yyy = (monitor_height / y_move) - (window_height / y_move)
xxx = (monitor_width / x_move) - (window_width / x_move)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, xxx, yyy))

expression = ""
last_pressed_equal = False
input_text = StringVar()

last_equation = tk.StringVar()
label_last = tk.Label(root, textvariable=last_equation, font=("Arial", 12), fg="gray", bg="#2E2E2E", anchor="e")
label_last.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, ipadx=5, ipady=5, pady=2)

entry = tk.Entry(root, textvariable=input_text, font=("Arial", 20), bg="#1E1E1E", fg="white", bd=5, justify="right")
entry.grid(row=1, column=0, columnspan=4, ipadx=10, ipady=20, padx=2, pady=2, sticky="nsew")

"""
entry = tk.Entry(root, textvariable=input_text, font=("Arial", 20), bg="#1E1E1E", fg="white", bd=5, justify="right") # , state="readonly")
entry.grid(row=0, column=0, columnspan=4, ipadx=10, ipady=20, padx=2, pady=2, sticky="nsew")
"""
def filter_keys(event):
    # If the pressed key is a letter, block it from entry (unless it's c...)
    if event.char.isalpha() and event.char.lower() not in ('c', 'x'):
        return "break"
entry.bind("<KeyPress>", filter_keys)

buttons = [('C', 2, [0, 2, 2]),                   ('/', 2, 3),
           ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('*', 3, 3),
           ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3),
           ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
           ('0', 6, [0, 1]),         ('.', 6, 2), ('=', 6, 3)]

for (text, row, col) in buttons:
    if text == '=':
        btn = tk.Button(root, text=text, font=("Arial", 20), bg="#FF9800", fg="black", padx=20, pady=20,
                        command=btn_equal)
    elif text == 'C':
        btn = tk.Button(root, text=text, font=("Arial", 20), bg="#D32F2F", fg="white", padx=20, pady=20,
                        command=btn_clear)
        btn.grid(row=row, column=col[0], columnspan=3, sticky='nsew')
        continue
    elif text == '0':
        btn = tk.Button(root, text=text, font=("Arial", 20), bg="#424242", fg="white", padx=20, pady=20,
                        command=lambda t=text: btn_click(t))
        btn.grid(row=row, column=col[0], columnspan=2, sticky='nsew')
        continue
    else:
        btn = tk.Button(root, text=text, font=("Arial", 20), bg="#424242", fg="white", padx=20, pady=20,
                        command=lambda t=text: btn_click(t))
    btn.grid(row=row, column=col, sticky='nsew')

# Adjust row/column weights
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Bind keyboard events
entry.focus_set()
root.bind("<Key>", key_handler)

root.mainloop()
