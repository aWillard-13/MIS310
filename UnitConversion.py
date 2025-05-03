# Andrew Willard
# 20250410
# Unit Conversion App

"""
This code is an expansion on the unit conversion program.
"""

"""
Added a GUI.
Added various units to convert to / from.
expanded upon the various types of measurement.
added tabs to swap between the measurement types.
implemented pandas and notebooks to switch the units. 
     (liked this more than the dropdown or radio buttons)
added the scroll wheel function that I have implemented so many times before.
"""

#Libs
import tkinter as tk
from tkinter import ttk
import pandas as pd
import os

#Unit conversion dict
unit_data = {
    "Distance": {
        "Centimeter": 0.01,
        "Inch": 0.0254,
        "Foot": 0.3048,
        "Meter": 1,
        "Kilometer": 1000,
        "Mile": 1609.34
    },
    "Mass": {
        "Gram": 0.001,
        "Ounce": 0.0283495,
        "Pound": 0.453592,
        "Kilogram": 1
    },
    "Temperature": {
        "Celsius": "C",
        "Fahrenheit": "F",
        "Kelvin": "K"
    },
    "Volume": {
        "Milliliter": 0.001,
        "Pint": 0.473176,
        "Gallon": 3.78541,
        "Liter": 1,
        "Cubic Meter": 1000
    },
    "Time": {
        "Second": 1,
        "Minute": 60,
        "Hour": 3600,
        "Day": 86400,
        "Week": 604800,
        "Month": 2628288,
        "Year": 31536000
    }
}

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius": return value *9/5+32 if to_unit == "Fahrenheit" else value + 273.15
    elif from_unit == "Fahrenheit": return (value-32) *5/9 if to_unit == "Celsius" else (value - 32) *5/9+273.15
    elif from_unit == "Kelvin": return value - 273.15 if to_unit == "Celsius" else (value - 273.15) *9/5+32


def setup_style(root):
    style = ttk.Style(root)
    style.theme_use("alt")  # alt, clam, classic, default, vista, winnative, xpnative

    # Color vars
    common_bg_gray = "#212121"
    alt_bg_gray = "#2e2e2e"
    common_fg_gray = "#cccccc"
    alt_fg_gray = "#bbbbbb"
    three, four, five = "#333333", "#444444", "#555555"

    # Configure multiple styles
    configs = {
        "TNotebook": {"background": common_bg_gray},
        "TNotebook.Tab": {"background": three, "foreground": common_fg_gray, "padding": 8},
        "TFrame": {"background": common_bg_gray},
        "TLabel": {"background": common_bg_gray, "foreground": common_fg_gray},
        "TEntry": {"fieldbackground": alt_bg_gray, "foreground": alt_fg_gray, "insertcolor": "white"},
        "Treeview": {"background":alt_bg_gray, "foreground":alt_fg_gray, "fieldbackground":alt_bg_gray, "rowheight":25},
        "Treeview.Heading": {"background": four, "foreground": common_fg_gray, "anchor": "center"},
        "TButton": {"background": four, "foreground": common_fg_gray}
    }

    for widget, opts in configs.items():
        style.configure(widget, **opts)

    # Maps for interaction states
    style.map("TNotebook.Tab", background=[("selected", five)])
    style.map("Treeview", background=[("selected", four)])


root = tk.Tk()
root.title("Unit Converter")

icon_path = "angledRuler.png"

if os.path.exists(icon_path):
    try:
        icon_image = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon_image)
    except tk.TclError as e:
        print("Error loading icon image:", e)
else:
    print(f"Error: '{icon_path}' not found. Please make sure it exists in the same folder.")




window_width, window_height = 311, 375
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
x, y = int((screen_width - window_width) / 2), int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="gray")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)


#create top tabs based on the unit data list
tab_entries = {}
def build_tab(category):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=category)

    units = list(unit_data[category].keys())
    df = pd.DataFrame(units, columns=["Unit"])

    container = ttk.Frame(frame)
    container.pack(pady=15)

    left_box = ttk.Frame(container)
    right_box = ttk.Frame(container)
    left_box.pack(side="left", padx=10, expand=True)
    right_box.pack(side="right", padx=10, expand=True)

    #prevents the entry of anything that isn't a number or - or .
    def validate_input(new_value):
        if new_value == "" or new_value == "-" or new_value == ".": return True
        try: float(new_value); return True
        except ValueError: return False
    gate_keep = (root.register(validate_input), "%P")

    ttk.Label(left_box, text="From").pack(pady=(0, 2))
    from_entry_var = tk.StringVar()
    from_entry = ttk.Entry(left_box, textvariable=from_entry_var, width=16, validate="key", validatecommand=gate_keep)
    from_entry.pack(pady=(0, 5),ipady=3)
    tab_entries[category] = from_entry_var

    tree_from = ttk.Treeview(left_box, columns=("Unit",), show="headings", height=7)
    tree_from.heading("Unit", text="Unit")
    tree_from.column("Unit", anchor="center", width=100)
    for x, row in df.iterrows(): tree_from.insert("", "end", values=(row["Unit"],))
    tree_from.pack()

    # Swap Button
    def swap_units():
        from_sel = tree_from.selection()
        to_sel = tree_to.selection()
        if from_sel and to_sel:
            from_unit = tree_from.item(from_sel[0])["values"][0]
            to_unit = tree_to.item(to_sel[0])["values"][0]
            # Swap selections
            for iid in tree_from.get_children():
                if tree_from.item(iid)["values"][0] == to_unit: tree_from.selection_set(iid)
            for iid in tree_to.get_children():
                if tree_to.item(iid)["values"][0] == from_unit: tree_to.selection_set(iid)
            update_conversion()

    # Centered Swap Button
    swap_frame = ttk.Frame(frame)
    swap_frame.pack(pady=5,ipady=20)
    swap_button = ttk.Button(swap_frame, text="Swap", command=lambda: swap_selection(tree_from, tree_to))
    swap_button.pack()

    # switches the tree selections with the press of the swap button
    def swap_selection(tree1, tree2):
        sel1 = tree1.selection()
        sel2 = tree2.selection()
        if sel1 and sel2:
            val1 = tree1.item(sel1[0])["values"][0]
            val2 = tree2.item(sel2[0])["values"][0]
            for item in tree1.get_children():
                if tree1.item(item)["values"][0] == val2: tree1.selection_set(item)
            for item in tree2.get_children():
                if tree2.item(item)["values"][0] == val1: tree2.selection_set(item)
            update_conversion()

    def scroll_selection(tree, direction):
        items = tree.get_children()
        if not items:
            return
        selected = tree.selection()
        if selected:
            idx = items.index(selected[0])
        else:
            idx = 0

        new_idx = idx + direction
        new_idx = max(0, min(len(items) - 1, new_idx))
        tree.selection_set(items[new_idx])
        tree.see(items[new_idx])
        update_conversion()

    ttk.Label(right_box, text="To").pack(pady=(0, 2))
    to_entry_var = tk.StringVar()
    to_entry = ttk.Entry(right_box, textvariable=to_entry_var, width=16, state='readonly',
                         background="#000", foreground='gray20')
    to_entry.pack(pady=(0, 5),ipady=3)

    tree_to = ttk.Treeview(right_box, columns=("Unit",), show="headings", height=7)
    tree_to.heading("Unit", text="Unit")
    tree_to.column("Unit", anchor="center", width=100)
    for z, row in df.iterrows(): tree_to.insert("", "end", values=(row["Unit"],))
    tree_to.pack()

    def on_mousewheel(event, tree=tree_from):
        scroll_selection(tree, -1 if event.delta > 0 else 1)
        return "break"
    def on_mousewheel_to(event, tree=tree_to):
        scroll_selection(tree, -1 if event.delta > 0 else 1)
        return "break"

    #Points what it is converting to... and from
    def update_conversion(*args):
        try:
            value = float(from_entry_var.get())
            from_item = tree_from.selection()
            to_item = tree_to.selection()
            if not from_item or not to_item: return
            from_unit = tree_from.item(from_item[0])["values"][0]
            to_unit = tree_to.item(to_item[0])["values"][0]

            if category == "Temperature": result = convert_temperature(value, from_unit, to_unit)
            else:
                factor_from = unit_data[category][from_unit]
                factor_to = unit_data[category][to_unit]
                result = value * (factor_from / factor_to)

            # Format result based on its value
            if result == int(result): formatted_result = str(int(result))
            elif abs(result) >= 1: formatted_result = f"{result:.4f}".rstrip("0").rstrip(".")
            else: formatted_result = f"{result:.10f}".rstrip("0").rstrip(".")

            to_entry_var.set(formatted_result)
        except Exception: to_entry_var.set(" <-- Enter Value")

    from_entry.bind("<KeyRelease>", update_conversion)
    tree_from.bind("<<TreeviewSelect>>", update_conversion)
    tree_to.bind("<<TreeviewSelect>>", update_conversion)

    # Scroll support
    def bind_scroll_selection(tree):
        def on_mousewheel(event):
            items = tree.get_children()
            if not items: return "break"
            selected = tree.selection()
            if selected: index = items.index(selected[0])
            else:
                index = 0
                tree.selection_set(items[0])
                return "break"
            delta = -1 if event.delta > 0 else 1  # Scroll up = move up, down = move down
            new_index = max(0, min(index + delta, len(items) - 1))
            tree.selection_set(items[new_index])
            tree.see(items[new_index])  # Make sure it's visible
            update_conversion()
            return "break"

        tree.bind("<Enter>", lambda e: tree.bind_all("<MouseWheel>", on_mousewheel))
        tree.bind("<Leave>", lambda e: tree.unbind_all("<MouseWheel>"))

    bind_scroll_selection(tree_from)
    bind_scroll_selection(tree_to)

    # Default select first items
    def select_first_items():
        if tree_from.get_children():
            tree_from.selection_set(tree_from.get_children()[0])
        if tree_to.get_children():
            tree_to.selection_set(tree_to.get_children()[0])
        update_conversion()

    # ensure trees are rendered first
    frame.after(100, select_first_items)

for cat in unit_data:
    build_tab(cat)

def on_tab_scroll(event):
    direction = -1 if event.delta > 0 else 1
    current = notebook.index(notebook.select())
    total_tabs = notebook.index("end")
    new_index = (current + direction) % total_tabs
    notebook.select(new_index)

notebook.bind("<MouseWheel>", on_tab_scroll)




# Scroll notebook tab bar with mouse wheel
def notebook_scroll(event):
    notebook.xview_scroll(-1 if event.delta > 0 else 1, "units")
notebook.bind("<Enter>", lambda e: notebook.bind_all("<MouseWheel>", notebook_scroll))
notebook.bind("<Leave>", lambda e: notebook.unbind_all("<MouseWheel>"))


# Handle number key presses to type into current tab's "from" entry
def key_input(event):
    if event.char.isdigit():
        current_tab = notebook.tab(notebook.select(), "text")
        entry_var = tab_entries.get(current_tab)
        if entry_var: entry_var.set(entry_var.get())

root.bind("<Key>", key_input)

# Apply the style
setup_style(root)

#run GUI
root.mainloop()
