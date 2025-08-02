import tkinter as tk
from tkinter import messagebox
import datetime
import json

# Global dictionary to hold attendance (now it loads from a file)
def load_attendance():
    try:
        with open("attendance_records.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "Aishwarya": [],
            "Nishika": [],
            "Harish": [],
            "Krishna": [],
            "Sandeep": []
        }

def save_attendance():
    with open("attendance_records.json", "w") as file:
        json.dump(attendance_data, file)

attendance_data = load_attendance()

# Utility to get current date
def get_today_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# ---------- HOME SCREEN ----------
def home_screen():
    root = tk.Tk()
    root.title("Student Attendance System")
    root.geometry("500x400")

    tk.Label(root, text="Welcome to Student Attendance System", font=("Helvetica", 16, "bold")).pack(pady=40)

    tk.Button(root, text="Admin Login", width=20, height=2, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
              command=lambda: [root.destroy(), admin_login_window()]).pack(pady=20)

    tk.Button(root, text="Student Login", width=20, height=2, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"),
              command=lambda: [root.destroy(), student_login_window()]).pack(pady=20)

    root.mainloop()

# ---------- ADMIN PANEL ----------
def admin_login_window():
    win = tk.Tk()
    win.title("Admin Login")
    win.geometry("400x300")

    tk.Label(win, text="Admin Login", font=("Helvetica", 18, "bold")).pack(pady=20)

    tk.Label(win, text="Username").pack()
    user_entry = tk.Entry(win)
    user_entry.pack()

    tk.Label(win, text="Password").pack()
    pass_entry = tk.Entry(win, show="*")
    pass_entry.pack()

    def validate():
        if user_entry.get() == "admin" and pass_entry.get() == "admin123":
            win.destroy()
            admin_panel()
        else:
            messagebox.showerror("Login Failed", "Incorrect credentials")

    tk.Button(win, text="Login", command=validate, bg="green", fg="white", font=("Helvetica", 12)).pack(pady=20)

    win.mainloop()

def admin_panel():
    win = tk.Tk()
    win.title("Admin Panel")
    win.geometry("600x500")

    tk.Label(win, text="Admin Panel - Student Attendance", font=("Helvetica", 16, "bold")).pack(pady=20)

    frame = tk.Frame(win)
    frame.pack()

    # Show attendance records
    text = tk.Text(frame, width=70, height=15)
    text.pack()

    def refresh_records():
        text.delete("1.0", tk.END)
        for student, dates in attendance_data.items():
            status = "Present on: " + ", ".join(dates) if dates else "Absent"
            text.insert(tk.END, f"{student}: {status}\n")

    refresh_records()

    # Manual marking
    tk.Label(win, text="Manually mark attendance:").pack(pady=10)
    student_var = tk.StringVar(win)
    student_var.set("Aishwarya")
    dropdown = tk.OptionMenu(win, student_var, *attendance_data.keys())
    dropdown.pack()

    def mark_attendance():
        student = student_var.get()
        today = get_today_date()
        if today not in attendance_data[student]:
            attendance_data[student].append(today)
            refresh_records()
            save_attendance()  # Save to file
            messagebox.showinfo("Success", f"Marked {student} as present for today.")
        else:
            messagebox.showinfo("Info", f"{student} is already marked present today.")

    tk.Button(win, text="Mark Attendance", command=mark_attendance, bg="orange", fg="white").pack(pady=10)

    # Back button to go back to the home screen
    def go_back():
        win.destroy()
        home_screen()

    tk.Button(win, text="Back", command=go_back, bg="red", fg="white").pack(pady=10)

    win.mainloop()

# ---------- STUDENT PANEL ----------
def student_login_window():
    win = tk.Tk()
    win.title("Student Login")
    win.geometry("400x300")

    tk.Label(win, text="Student Login", font=("Helvetica", 18, "bold")).pack(pady=20)

    tk.Label(win, text="Enter your name").pack()
    student_var = tk.StringVar(win)
    student_var.set("Aishwarya")
    dropdown = tk.OptionMenu(win, student_var, *attendance_data.keys())
    dropdown.pack(pady=10)

    def login_student():
        name = student_var.get()
        win.destroy()
        student_panel(name)

    tk.Button(win, text="Login", command=login_student, bg="#2196F3", fg="white").pack(pady=20)

    win.mainloop()

def student_panel(name):
    win = tk.Tk()
    win.title(f"{name} - Student Panel")
    win.geometry("500x400")

    tk.Label(win, text=f"Welcome, {name}", font=("Helvetica", 16, "bold")).pack(pady=20)

    def mark_attendance():
        today = get_today_date()
        if name in ["Aishwarya", "Nishika", "Harish"]:
            if today not in attendance_data[name]:
                attendance_data[name].append(today)
                save_attendance()  # Save to file
                messagebox.showinfo("Success", "Attendance marked successfully!")
            else:
                messagebox.showinfo("Info", "Attendance already marked today.")
        else:
            messagebox.showerror("Error", "Fingerprint not recognized. Access Denied.")

    tk.Button(win, text="Mark Attendance (Fingerprint)", command=mark_attendance,
              bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=20)

    # View own attendance
    def view_my_attendance():
        record = attendance_data.get(name, [])
        message = f"Present on: {', '.join(record)}" if record else "You are absent on all days."
        messagebox.showinfo("Attendance Record", message)

    tk.Button(win, text="View My Attendance", command=view_my_attendance,
              bg="#2196F3", fg="white", font=("Helvetica", 12)).pack(pady=10)

    # Back button to go back to the home screen
    def go_back():
        win.destroy()
        home_screen()

    tk.Button(win, text="Back", command=go_back, bg="red", fg="white").pack(pady=10)

    win.mainloop()

# Start the program
home_screen()


