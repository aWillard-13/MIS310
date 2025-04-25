# Andrew Willard
# 20251604
# Dice Roller App

"""
Based on the use of the Dice game (with the use of random lib).
a GUI has been added. a button to roll dice.
the ability to add or subtract the number of dice rolls has been implemented.
the scope has changed.
the type of dice has been expanded on with the introduction of the concept of "I am making this for DND dice now."
the dice are now tracked in a dnd like fashion "#d#". the first being the count of dice, the second being the number of sides.
7 dice types have been added.
the ability to increase and decrease each die with the mouse scroll wheel has been added.
error handling added.
custom darkmode pop out windows added.
when the #d# of a die is clicked, a pop up window where the person can type in the desired number of dice of that type.

"""

"""
Future plans.
want to add a flip a coin button. 
(can put that where the "dnd dice app" text is. this is not important.)
fix the dice. 
     the 100 is functioning like a percentile roll. make it so.
     add a real 100 die (just a 10 with an extra 0).
     add a custom dice where the user can roll a number of user input side dice.
instead of using a pop up window to display the results,
     I want to have them show up on their own GUI part. maybe just story that info in the bottom history section.
     turn history into a breakout menu??

"""

import tkinter as tk
from datetime import datetime
import random
import os

############################################### Logic ###############################################

#function that creates our own messagebox to use with a dark theme.
def show_dark_messagebox(title, message):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.configure(bg="#1E1E1E")
    popup.resizable(False, False)

    tk.Label(popup, text=message, bg="#1E1E1E", fg="white", wraplength=300, justify="center").pack(padx=20, pady=20)

    def close(event=None):
        popup.destroy()

    ok_button = tk.Button(popup, text="        OK        ", command=close,
                          bg="gray30", fg="white", activebackground="gray50", activeforeground="white")
    ok_button.pack(pady=(5, 20))

    popup.bind("<Return>", close)
    popup.bind("<Escape>", close)

    popup.update_idletasks()
    w = popup.winfo_width()
    h = popup.winfo_height()
    x = root.winfo_x() + (root.winfo_width() // 2) - (w // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (h // 2)
    popup.geometry(f"{w}x{h}+{x}+{y}")

    popup.grab_set()
    ok_button.focus_set()

def show_dice_input_popup(sides):
    popup = tk.Toplevel(root)
    popup.title(f"Set d{sides} Amount")
    popup.configure(bg="#1E1E1E")
    popup.resizable(False, False)

    tk.Label(popup, text=f"Enter number of d{sides} dice:", fg="white", bg="#1E1E1E",
             font=("Helvetica", 11)).pack(pady=(15, 5))

    dice_var = tk.StringVar(value="") # set val to null
    entry = tk.Entry(popup, textvariable=dice_var, width=10, justify="center",
                     bg="black", fg="white", insertbackground="white")
    entry.pack(pady=5)



    def apply_and_close():
        try:
            value = int(dice_var.get())
            if value >= 0:
                dice_counts[sides] = value
                update_dice_display()
            else:
                raise ValueError
        except ValueError:
            show_dark_messagebox("Invalid Input", "Please enter a non-negative integer.")
        popup.destroy()

    ok_btn = tk.Button(popup, text="  OK  ", command=apply_and_close,
                       bg="gray30", fg="white", activebackground="gray50", activeforeground="white")
    ok_btn.pack(pady=(10, 15))

    popup.bind("<Return>", lambda e: apply_and_close())
    popup.bind("<Escape>", lambda e: popup.destroy())

    popup.update_idletasks()
    w = popup.winfo_width()
    h = popup.winfo_height()
    x = root.winfo_x() + (root.winfo_width() // 2) - (w // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (h // 2)
    popup.geometry(f"{w}x{h}+{x}+{y}")

    popup.grab_set()
    entry.focus_set()

dice_counts = {4: 0, 6: 0, 8: 0, 10: 0, 12: 0, 20: 0, 100: 0}
dice_labels = {}
history_log = []

def update_dice_display():
    for sides, label in dice_labels.items():
        count = dice_counts[sides]
        label_text = f"{count}d{sides}"
        label.config(text=label_text)

def modify_dice(sides, delta):
    new_count = dice_counts[sides] + delta
    if new_count >= 0:
        dice_counts[sides] = new_count
    update_dice_display()

def clear_pool():
    for key in dice_counts:
        dice_counts[key] = 0
    update_dice_display()

def roll_dice():
    try:
        mod = int(modifier_var.get())
    except ValueError:
        mod = 0

    total = mod
    breakdown = []

    for sides, count in dice_counts.items():
        for _ in range(count):
            roll = random.randint(1, sides)
            total += roll
            breakdown.append(f"d{sides}: {roll}")

    timestamp = datetime.now().strftime("%H:%M:%S")
    mod_str = f" (Modifier: {mod:+})" if mod != 0 else ""

    if total == mod:
        show_dark_messagebox("No Dice", "You haven't added any dice to roll.")
    else:
        result = f"[{timestamp}] Total: {total}{mod_str}\n" + "\n".join(breakdown)
        history_log.append(result)
        update_history_display()
        show_dark_messagebox("Roll Result", result)

def update_history_display():
    history_box.config(state='normal')
    history_box.delete(1.0, tk.END)
    for entry in reversed(history_log[-10:]):
        history_box.insert(tk.END, entry + "\n\n")
    history_box.config(state='disabled')

def on_mousewheel(event, sides):
    delta = 1 if event.delta > 0 else -1
    modify_dice(sides, delta)

def clear_history():
    history_log.clear()
    history_box.config(state='normal')
    history_box.delete("1.0", tk.END)
    history_box.config(state='disabled')

############################################### UI Setup ###############################################

root = tk.Tk()
root.title("D&D Dice Roller")
root.configure(bg="#1E1E1E")

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()
window_height = monitor_height * 0.80
window_width = monitor_width * 0.20
win_x_coord = int((monitor_width - window_width) / 2)
win_y_coord = int((monitor_height - window_height) / 4)
root.geometry(f"{int(window_width)}x{int(window_height)}+{win_x_coord}+{win_y_coord}")

# Disable window resizing
root.resizable(width=False, height=False)

title_label = tk.Label(root, text=" - DnD Dice App -", fg="white", bg="#1E1E1E", font=("Helvetica", 16, "bold"))
title_label.pack(pady=(10, 10))

icon_path = "gameDie.png"

if os.path.exists(icon_path):
    try:
        icon_image = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon_image)
    except tk.TclError as e:
        print("Error loading icon image:", e)
else:
    print(f"Error: '{icon_path}' not found. Please make sure it exists in the same folder.")

main_frame = tk.Frame(root, bg="#1E1E1E")
main_frame.pack()

# Add arrow buttons and label display for each die type
for sides in sorted(dice_counts.keys()):
    frame = tk.Frame(main_frame, bg="#1E1E1E")
    frame.pack(pady=6)

    left_btn = tk.Button(frame, text="◀", command=lambda s=sides: modify_dice(s, -1),
                         bg="gray20", fg="white", activebackground="gray30", width=4)
    left_btn.pack(side="left", padx=5)

    label = tk.Label(frame, text=f"0d{sides}", fg="white", bg="#1E1E1E", width=10, font=("Helvetica", 12))
    label.pack(side="left", padx=5)
    dice_labels[sides] = label

    # NEW: Bind label click to open input popup
    label.bind("<Button-1>", lambda e, s=sides: show_dice_input_popup(s))

    right_btn = tk.Button(frame, text="▶", command=lambda s=sides: modify_dice(s, 1),
                          bg="gray20", fg="white", activebackground="gray30", width=4)
    right_btn.pack(side="left", padx=5)

    for widget in (left_btn, label, right_btn):
        widget.bind("<Enter>", lambda e, s=sides, w=widget: w.bind_all("<MouseWheel>", lambda ev: on_mousewheel(ev, s)))
        widget.bind("<Leave>", lambda e, w=widget: w.unbind_all("<MouseWheel>"))

modifier_frame = tk.Frame(root, bg="#1E1E1E")
modifier_frame.pack(pady=(15, 5))
tk.Label(modifier_frame, text="Modifier:", fg="white", bg="#1E1E1E", font=("Helvetica", 12)).pack(side="left", padx=(0, 8))
modifier_var = tk.StringVar(value="0")
modifier_entry = tk.Entry(modifier_frame, textvariable=modifier_var, width=5,
                          bg="black", fg="white", insertbackground="white", justify="center")
modifier_entry.pack(side="left")

button_frame = tk.Frame(root, bg="#1E1E1E")
button_frame.pack(pady=(15, 10))

roll_btn = tk.Button(button_frame, text="  Roll Dice  ", command=roll_dice,
                     bg="green", fg="white", activebackground="darkgreen", width=20)
roll_btn.pack(pady=5)

clear_buttons_frame = tk.Frame(button_frame, bg="#1E1E1E")
clear_buttons_frame.pack(pady=5)

clear_btn = tk.Button(clear_buttons_frame, text="  Clear Pool  ", command=clear_pool,
                      bg="gray30", fg="white", activebackground="gray50", width=10)
clear_btn.pack(side=tk.LEFT, padx=(0, 5))

clear_history_button = tk.Button(clear_buttons_frame, text="  Clear History  ", command=clear_history,
                                 bg="gray30", fg="white", activebackground="gray50", width=10)
clear_history_button.pack(side=tk.LEFT, padx=(5, 0))

history_frame = tk.Frame(root, bg="#1E1E1E")
history_frame.pack(pady=(20, 10))
tk.Label(history_frame, text="Roll History:", fg="white", bg="#1E1E1E", font=("Helvetica", 12)).pack()

history_box = tk.Text(history_frame, height=10, width=31, bg="black", fg="white", state='disabled', wrap="word")
history_box.pack()

root.bind("<Return>", lambda event: roll_dice())
root.bind("<Escape>", lambda event: root.destroy())

root.mainloop()