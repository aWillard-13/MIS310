# Andrew Willard
# 20250504
# Patient information Interface

"""
I have to stop. the Scope keeps moving. we are done. I have to be done.
This is a code that pulls and pushes patient information from various .json files.
based off the first code we worked on in class:
    I expanded on the idea by making the code store the information in a .json...
    Created a GUI that references this information...
    Broke out the json into 3 different files.
    added 3 different tabs, scaled it back and removed the tkcalendar (it worked but it was too much)
    deleted 1 tab.
    made both tabs semi usable.

future:
    need to add error handling and records with issues.
    need to add an admin tab that breaks down every json file and it's contents for easy editing and updating.
    add doc profiles?
    bring back the schedulerTab.
"""

#Libs
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import json
import os
from datetime import datetime, timedelta, timezone

PATIENTS_FILE = "patients.json"
DOCTORS_FILE = "doctors.json"
APPOINTMENTS_FILE = "appointments.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def save_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def get_time_slots(work_hours):
    start_str, end_str = work_hours.split("-")
    start_time = datetime.strptime(start_str, "%H:%M")
    end_time = datetime.strptime(end_str, "%H:%M")
    slots = []
    while start_time < end_time:
        slots.append(start_time.strftime("%I:%M %p"))
        start_time += timedelta(minutes=30)
    return slots

class PatientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Record System")
        self.root.configure(bg="#222")
        self.root.resizable(width=False, height=False)

        window_width, window_height = 750, 600
        self.root.geometry(f"{window_width}x{window_height}")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.patients = load_data(PATIENTS_FILE)
        self.appointments = load_data(APPOINTMENTS_FILE)
        self.doctors = load_data(DOCTORS_FILE)

        self.current_index = None

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.create_patient_tab()
        self.create_appointment_tab()

        self.populate_patient_list()
        self.populate_appointment_table()


#######################################################################################################################


    def create_patient_tab(self):
        self.patient_frame = tk.Frame(self.notebook, bg="#222")
        self.notebook.add(self.patient_frame, text="Patients")

        self.left_frame = tk.Frame(self.patient_frame, bg="#333")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.patient_frame, bg="#222")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.patient_listbox = tk.Listbox(self.left_frame, width=30, bg="#111", fg="white", font=("default", 12))
        self.patient_listbox.pack(padx=10, pady=10, ipadx=1, fill=tk.Y, expand=True)
        self.patient_listbox.bind("<<ListboxSelect>>", self.load_selected_patient)

        tk.Button(self.left_frame, text="Add New Patient", command=self.add_new_patient, bg="#4CAF50", fg="white").pack(pady=5)
        tk.Button(self.left_frame, text="Delete", command=self.delete_patient, bg="#f44336", fg="white").pack(pady=5)

        self.fields = {}
        field_names = ["name", "age", "gender", "symptoms", "diagnosis", "medications", "allergies"]
        for i, field in enumerate(field_names):
            tk.Label(self.right_frame, text=field.capitalize() + ":", bg="#222", fg="white").grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(self.right_frame, bg="gray", width=50)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.fields[field] = entry

        tk.Label(self.right_frame, text="New Patient?", bg="#222", fg="white").grid(row=len(field_names), column=0, sticky="e")
        self.new_patient_var = tk.BooleanVar()
        self.new_patient_check = tk.Checkbutton(self.right_frame, variable=self.new_patient_var, bg="#222", fg="white", selectcolor="gray")
        self.new_patient_check.grid(row=len(field_names), column=1, sticky="w")

        tk.Label(self.right_frame, text="   Next Appointment:", bg="#222", fg="white").grid(row=8, column=0, sticky="e")
        self.appointment_Label = tk.Label(self.right_frame, bg="gray", width=30)
        self.appointment_Label.grid(row=8, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self.right_frame, text="Doctor:", bg="#222", fg="white").grid(row=9, column=0, sticky="e", pady=5)
        self.doctor_var = tk.StringVar()
        self.doctor_dropdown = ttk.Combobox(self.right_frame, textvariable=self.doctor_var, values=[d["name"] for d in self.doctors], width=28)
        self.doctor_dropdown.grid(row=9, column=1, sticky="w", padx=5)

        tk.Label(self.right_frame, text="Next Available:", bg="#222", fg="white").grid(row=10, column=0, sticky="e", pady=5)
        self.next_available_var = tk.StringVar()
        self.next_available_dropdown = ttk.Combobox(self.right_frame, textvariable=self.next_available_var, width=28)
        self.next_available_dropdown.grid(row=10, column=1, sticky="w", padx=5)
        self.next_available_dropdown.bind("<<ComboboxSelected>>", self.update_time_slot_combo)

        tk.Label(self.right_frame, text="Appointment Time:", bg="#222", fg="white").grid(row=11, column=0, sticky="e", pady=5)
        self.appointment_time_var = tk.StringVar()
        self.appointment_combo = ttk.Combobox(self.right_frame, textvariable=self.appointment_time_var, width=28)
        self.appointment_combo.grid(row=11, column=1, sticky="w", padx=5)

        tk.Button(self.right_frame, text="Add Appointment", command=self.add_appointment, bg="#2196F3", fg="white").grid(row=12, column=1, sticky="w", pady=5)

        tk.Label(self.right_frame, text="Doctor Notes:", bg="#222", fg="white").grid(row=13, column=0, sticky="ne", padx=5)
        self.notes_entry = tk.Text(self.right_frame, bg="gray", width=38, height=4)
        self.notes_entry.grid(row=13, column=1, padx=5)

        tk.Button(self.right_frame, text="Add Note", command=self.add_note, bg="#2196F3", fg="white").grid(row=14, column=1, sticky="w", pady=5)
        tk.Button(self.right_frame, text=" Save ", command=self.save_patient, bg="#4CAF50", fg="white").grid(row=15, column=1, pady=30, ipadx=20)

        self.doctor_dropdown.bind("<<ComboboxSelected>>", self.populate_available_slots)


    def get_available_slots(self, doctor_name):
        doctor = next((d for d in self.doctors if d["name"] == doctor_name), None)
        if not doctor or "work_hours" not in doctor:
            return []

        start_hour, end_hour = map(lambda t: int(t.split(":" )[0]), doctor["work_hours"].split("-"))
        now = datetime.now()
        slots = []

        for i in range(14):
            date = now + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            day_slots = []
            for hour in range(start_hour, end_hour):
                for minute in (0, 30):
                    slot_time = f"{date_str} {hour:02}:{minute:02}"
                    if not any(appt for appt in self.appointments if appt["doctor"] == doctor_name and f"{appt['date']} {appt['time']}" == slot_time):
                        day_slots.append(slot_time)
            if day_slots:
                slots.extend(day_slots)
        return slots


    def populate_available_slots(self, event):
        doctor_name = self.doctor_var.get()
        slots = self.get_available_slots(doctor_name)
        dates = sorted(set(s.split()[0] for s in slots))
        self.next_available_dropdown["values"] = dates
        self.appointment_combo.set("")


    def update_time_slot_combo(self, event):
        selected_date = self.next_available_var.get()
        doctor_name = self.doctor_var.get()
        all_slots = self.get_available_slots(doctor_name)
        times = [datetime.strptime(s.split()[1], "%H:%M").strftime("%I:%M %p") for s in all_slots if s.startswith(selected_date)]
        self.appointment_combo["values"] = times


    def load_selected_patient(self, event):
        selection = self.patient_listbox.curselection()
        if selection:
            index = selection[0]
            self.current_index = index
            patient = self.patients[index]
            for key in self.fields:
                self.fields[key].delete(0, tk.END)
                self.fields[key].insert(0, str(patient.get(key, "")))
            self.new_patient_var.set(patient.get("new_patient", False))
            self.notes_entry.delete("1.0", tk.END)
            if "notes" in patient:
                self.notes_entry.insert(tk.END, "\n".join(patient["notes"]))
            self.doctor_var.set(patient.get("doctor", ""))
            self.next_available_var.set("")
            self.appointment_combo.set("")

            selected_name = patient["name"]
            future_appointments = []
            now = datetime.now()
            for appt in self.appointments:
                if appt["patient"] == selected_name:
                    try:
                        dt_obj = datetime.strptime(f"{appt.get('date', '')} {appt.get('time', '')}", "%Y-%m-%d %H:%M")
                        if dt_obj > now:
                            future_appointments.append(dt_obj)
                    except:
                        pass
            if future_appointments:
                next_appt = min(future_appointments)
                est_next = next_appt.replace(tzinfo=timezone.utc)
                formatted = est_next.strftime("%B %d at %I:%M %p")
                self.appointment_Label.config(text=formatted)
            else:
                self.appointment_Label.config(text="No future appointments")


    def save_patient(self):
        data = {k: self.fields[k].get() for k in self.fields}
        try:
            data["age"] = int(data["age"])
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return
        data["new_patient"] = self.new_patient_var.get()
        data["notes"] = self.patients[self.current_index].get("notes", []) if self.current_index is not None else []
        data["doctor"] = self.doctor_var.get()

        if self.current_index is not None:
            self.patients[self.current_index] = data
        else:
            self.patients.append(data)

        save_data(self.patients, PATIENTS_FILE)
        self.populate_patient_list()
        messagebox.showinfo("Saved", "Patient record saved successfully.")


    def add_appointment(self):
        patient_name = self.fields["name"].get()
        doctor_name = self.doctor_var.get()
        date = self.next_available_var.get()
        time_str = self.appointment_time_var.get()
        if not date or not time_str:
            messagebox.showerror("Error", "Please select both date and time.")
            return

        time_24h = datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")

        appointment = {
            "patient": patient_name,
            "doctor": doctor_name,
            "date": date,
            "time": time_24h
        }
        self.appointments.append(appointment)
        save_data(self.appointments, APPOINTMENTS_FILE)
        self.populate_appointment_table()
        messagebox.showinfo("Success", "Appointment added successfully.")


    def add_note(self):
        note = self.notes_entry.get("1.0", tk.END).strip()
        if self.current_index is not None and note:
            self.patients[self.current_index].setdefault("notes", []).append(note)
            save_data(self.patients, PATIENTS_FILE)


    def delete_patient(self):
        selection = self.patient_listbox.curselection()
        if selection:
            index = selection[0]
            del self.patients[index]
            save_data(self.patients, PATIENTS_FILE)
            self.populate_patient_list()


    def populate_patient_list(self):
        self.patient_listbox.delete(0, tk.END)
        for p in self.patients:
            self.patient_listbox.insert(tk.END, p["name"])


    def populate_appointment_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for appt in self.appointments:
            try:
                dt_obj = datetime.strptime(f"{appt.get('date', '')} {appt.get('time', '')}", "%Y-%m-%d %H:%M")
                est_dt = dt_obj.replace(tzinfo=timezone.utc)
                formatted_time = est_dt.strftime('%B %d at %I:%M %p')
            except Exception:
                formatted_time = f"{appt.get('date', '')} {appt.get('time', '')}"
            self.tree.insert("", tk.END, values=(appt.get("patient", "Unknown"), formatted_time, appt.get("doctor", "Unassigned")))


    def create_appointment_tab(self):
        self.appt_tab = tk.Frame(self.notebook, bg="#222")
        self.notebook.add(self.appt_tab, text="Appointments")

        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview", background="lightgray", foreground="black", fieldbackground="gray")

        self.tree = ttk.Treeview(self.appt_tab, columns=("patient", "datetime", "doctor"), show="headings")
        self.tree.heading("patient", text="Patient")
        self.tree.heading("datetime", text="Date/Time")
        self.tree.heading("doctor", text="Doctor")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_new_patient(self):
        for field in self.fields.values():
            field.delete(0, tk.END)
        self.new_patient_var.set(False)
        self.current_index = None
        self.patient_listbox.selection_clear(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)
        self.doctor_var.set("")
        self.appointment_combo.set("")
        self.next_available_var.set("")


#######################################################################################################################


    def create_appointment_tab(self):
        self.appt_tab = tk.Frame(self.notebook)
        self.notebook.add(self.appt_tab, text="Appointments")

        # Style adjustments for dark theme
        self.appt_tab.configure(background="#2e2e2e")
        # Style Treeview with dark colors
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Treeview", background="#3c3f41", foreground="white", fieldbackground="#3c3f41", rowheight=25)
        style.map("Treeview", background=[("selected", "#6a6a6a")])
        style.configure("Treeview.Heading", background="#2e2e2e", foreground="white")

        self.tree = ttk.Treeview(self.appt_tab, columns=("patient", "datetime", "doctor"), show="headings")
        self.tree.heading("patient", text="Patient")
        self.tree.heading("datetime", text="Date/Time")
        self.tree.heading("doctor", text="Doctor")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.display_patient_info)

        self.info_label = tk.Label(self.appt_tab, text="Select \nan appointment \nto view details.")
        self.info_label.pack(pady=10)

        btn_frame = tk.Frame(self.appt_tab)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Delete Appointment", command=self.delete_appointment,
                  bg="#5c5c5c", fg="white"

                  ).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reschedule Appointment", command=self.open_reschedule_dialog,
                  bg="#5c5c5c",
                  fg="white").pack(side=tk.LEFT, padx=5)


    def display_patient_info(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        patient_name = values[0]
        patient = next((p for p in self.patients if p["name"] == patient_name), None)
        if patient:
            info = f"Name: {patient.get('name', '')}\nAge: {patient.get('age', '')}\nGender: {patient.get('gender', '')}"
            self.info_label.config(text=info)


    def delete_appointment(self):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        patient_name, dt_str, doctor = values
        date, time = dt_str.split()
        self.appointments = [a for a in self.appointments if not (a["patient"] == patient_name and a["date"] == date and a["time"] == time)]
        save_data(self.appointments, APPOINTMENTS_FILE)
        self.populate_appointment_table()
        self.info_label.config(text="Appointment deleted.")


    def open_reschedule_dialog(self):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        patient_name, dt_str, doctor_name = values

        top = tk.Toplevel(self.root)
        top.title("Reschedule Appointment")
        tk.Label(top, text="Select new time:").pack(pady=5)

        slot_var = tk.StringVar()
        combo = ttk.Combobox(top, textvariable=slot_var, width=30)
        combo.pack(pady=5)

        available = self.get_available_slots(doctor_name)
        combo["values"] = available


        def confirm():
            new_slot = slot_var.get()
            if new_slot:
                date, time = new_slot.split()
                for appt in self.appointments:
                    if appt["patient"] == patient_name and appt["doctor"] == doctor_name:
                        appt["date"] = date
                        appt["time"] = time
                        break
                save_data(self.appointments, APPOINTMENTS_FILE)
                self.populate_appointment_table()
                top.destroy()

        tk.Button(top, text="Confirm", command=confirm).pack(pady=5)


    def get_available_slots(self, doctor_name):
        doctor = next((d for d in self.doctors if d["name"] == doctor_name), None)
        if not doctor:
            return []

        start_hour, end_hour = map(lambda t: int(t.split(":")[0]), doctor["work_hours"].split("-"))
        now = datetime.now()
        slots = []

        for i in range(28):
            day = now + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            for h in range(start_hour, end_hour):
                for m in (0, 30):
                    slot = f"{date_str} {h:02}:{m:02}"
                    if not any(appt["date"] == date_str and appt["time"] == f"{h:02}:{m:02}" and appt["doctor"] == doctor_name for appt in self.appointments):
                        slots.append(slot)
        return slots


if __name__ == "__main__":
    root = tk.Tk()
    app = PatientApp(root)
    root.mainloop()
