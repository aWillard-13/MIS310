# Andrew Willard
# MIS-310
# IA3 - problem 2


""" Magic Date Checker """


import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import calendar
import random


############################################### Logic ###############################################

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

    popup.update_idletasks()
    w = popup.winfo_width()
    h = popup.winfo_height()
    x = root.winfo_x() + (root.winfo_width() // 2) - (w // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (h // 2)
    popup.geometry(f"{w}x{h}+{x}+{y}")

    popup.grab_set()
    ok_button.focus_set()

def check_date():
    selected_date = cal.selection_get()
    month = selected_date.month
    day = selected_date.day
    full_year = selected_date.year
    short_year = full_year % 100

    if month * day == short_year:
        show_dark_messagebox("Magic Date!", f"The date {month}/{day}/{full_year} is magic!")
    else:
        show_dark_messagebox("Not Magic", f"The date {month}/{day}/{full_year} is not magic.\nSorry...")

def update_entries_from_calendar(event=None):
    date = cal.selection_get()
    day_var.set(date.day)
    month_var.set(date.month)
    year_var.set(date.year)

def update_calendar_from_entries(*args):
    try:
        new_day = int(day_var.get())
        new_month = int(month_var.get())
        new_year = int(year_var.get())
        new_date = datetime(new_year, new_month, new_day)
        cal.selection_set(new_date)
    except: pass


############################################### Date Adjustments ###############################################
def adjust_date_by_keyboard(days=0, months=0, years=0):
    try:
        day = int(day_var.get())
        month = int(month_var.get())
        year = int(year_var.get())

        if months != 0:
            month += months
            while month > 12:
                month -= 12
                year += 1
            while month < 1:
                month += 12
                year -= 1
                if year < 1:
                    year = 1
                    month = 1
                    break
            max_day = calendar.monthrange(year, month)[1]
            day = min(day, max_day)

        if years != 0:
            year = max(1, year + years)  # prevent year from going below 1
            max_day = calendar.monthrange(year, month)[1]
            day = min(day, max_day)

        if days != 0:
            current = datetime(year, month, day)
            current += timedelta(days=days)
            year, month, day = current.year, current.month, current.day

        day_var.set(str(day))
        month_var.set(str(month))
        year_var.set(str(year))
        update_calendar_from_entries()
    except: pass

scroll_mode = 0  # 0 = days, 1 = months, 2 = years

def on_calendar_mousewheel(event):
    delta = 1 if event.delta > 0 else -1
    if event.state & 0x0004:  # Ctrl key
        adjust_date_by_keyboard(months=delta)
    elif event.state & 0x0001:  # Shift key
        adjust_date_by_keyboard(years=delta)
    else:
        adjust_date_by_keyboard(days=delta)


############################################### Magic Date Generator ###############################################
def generate_random_magic_date(start_year=1900, end_year=2100):
    magic_dates = []
    for year in range(start_year, end_year + 1):
        short_year = year % 100
        for month in range(1, 13):
            if short_year % month == 0:
                day = short_year // month
                if 1 <= day <= calendar.monthrange(year, month)[1]:
                    magic_dates.append(datetime(year, month, day))
    return random.choice(magic_dates)

def set_random_magic_date():
    date = generate_random_magic_date()
    day_var.set(str(date.day))
    month_var.set(str(date.month))
    year_var.set(str(date.year))
    update_calendar_from_entries()


############################################### UI Setup ###############################################
root = tk.Tk()
root.title("Magic Date Checker")
root.configure(bg="#1E1E1E")

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()
window_height = monitor_height * 0.45
window_width = monitor_width * 0.20
root.geometry(f"{int(window_width)}x{int(window_height)}+{int((monitor_width - window_width) / 2)}+{int((monitor_height - window_height) / 2)}")

month_var = tk.StringVar()
day_var = tk.StringVar()
year_var = tk.StringVar()

month_var.trace_add('write', update_calendar_from_entries)
day_var.trace_add('write', update_calendar_from_entries)
year_var.trace_add('write', update_calendar_from_entries)

input_frame = tk.Frame(root, bg="#1E1E1E")
input_frame.pack(pady=(10, 0))

def create_label_input(label, var, width=10):
    frame = tk.Frame(input_frame, bg="#1E1E1E")
    frame.pack(side="left", padx=10)

    tk.Label(frame, text=label, fg="white", bg="#1E1E1E").pack()

    def adjust_value(delta):
        try:
            current = int(var.get())
        except ValueError:
            current = 1
        if var == month_var:
            adjust_date_by_keyboard(months=delta)
        elif var == day_var:
            adjust_date_by_keyboard(days=delta)
        elif var == year_var:
            adjust_date_by_keyboard(years=delta)

    up_btn = tk.Button(frame, text="      ▲      ", command=lambda: adjust_value(1), font=("Sudo", 5),
                       bg="gray20", fg="white", width=10)
    up_btn.pack()

    entry = tk.Entry(frame, textvariable=var, width=width, justify="center",
                     bg="black", fg="white", insertbackground="white")
    entry.pack()

    down_btn = tk.Button(frame, text="      ▼      ", command=lambda: adjust_value(-1), font=("Sudo", 5),
                         bg="gray20", fg="white", width=10)
    down_btn.pack()

    def on_mousewheel(event):
        delta = 1 if event.delta > 0 else -1
        adjust_value(delta)

    for widget in (frame, entry, up_btn, down_btn):
        widget.bind("<MouseWheel>", on_mousewheel)

create_label_input("    Month    ", month_var)
create_label_input("    Day      ", day_var)
create_label_input("    Year     ", year_var, width=8)

cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd', firstweekday="sunday",
               background="black", foreground="white", headersbackground="gray30", normalbackground="gray50",
               bordercolor="black", weekendbackground="gray20", weekedaybackground="gray10",
               othermonthbackground="gray20", othermonthwebackground="gray30",
               selectbackground="gray30", selectforeground="white")
cal.pack(pady=20)
cal.bind("<<CalendarSelected>>", update_entries_from_calendar)

# Scroll when mouse is over calendar
cal.bind("<Enter>", lambda e: root.bind_all("<MouseWheel>", on_calendar_mousewheel))
cal.bind("<Leave>", lambda e: root.unbind_all("<MouseWheel>"))

tk.Button(root, text="    Check Magic Date    ", command=check_date,
          bg="gray20", fg="white", activebackground="gray30", activeforeground="white").pack(pady=(5, 2))

# Invisible button that sets a random magic date # Debug
invisible_btn = tk.Button(root, text="                               ", command=set_random_magic_date, bg="#1E1E1E",
                          fg="#1E1E1E", activebackground="#1E1E1E", borderwidth=0)
invisible_btn.pack(ipady=0, pady=(0, 0))

root.bind("<Return>", lambda event: check_date())
root.bind("<Escape>", lambda event: root.destroy())
root.bind("<Up>", lambda e: adjust_date_by_keyboard(years=1))
root.bind("<Down>", lambda e: adjust_date_by_keyboard(years=-1))
root.bind("<Left>", lambda e: adjust_date_by_keyboard(days=-1))
root.bind("<Right>", lambda e: adjust_date_by_keyboard(days=1))


update_entries_from_calendar()
root.mainloop()
