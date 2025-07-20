import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyttsx3
import time
import random
import pickle
import os
import threading

# Text-to-speech engine
engine = pyttsx3.init()

# Load tasks
if os.path.exists("study_tasks.pkl"):
    with open("study_tasks.pkl", "rb") as f:
        tasks = pickle.load(f)
else:
    tasks = []

# Speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

def save_tasks():
    with open("study_tasks.pkl", "wb") as f:
        pickle.dump(tasks, f)

def add_task():
    task = task_entry.get()
    if task.strip():
        tasks.append({"task": task, "completed": False})
        task_entry.delete(0, tk.END)
        update_task_list()
        save_tasks()
        speak("Task added")
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def delete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        del tasks[selected_index]
        update_task_list()
        save_tasks()
        speak("Task deleted")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

def complete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        tasks[selected_index]["completed"] = True
        update_task_list()
        save_tasks()
        speak("Task marked as complete")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")

def clear_all_tasks():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
        tasks.clear()
        update_task_list()
        save_tasks()
        speak("All tasks cleared")

def inspire_me():
    quotes = [
        "Keep pushing forward, you're doing great!",
        "Small steps lead to big achievements!",
        "Believe in yourself and your abilities!",
        "Progress is progress, no matter how small."
    ]
    quote = random.choice(quotes)
    speak(quote)
    messagebox.showinfo("Motivation", quote)

def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✔️" if task["completed"] else "❌"
        task_listbox.insert(tk.END, f"{task['task']} [{status}]")

# --- Timer Section ---
def start_timer():
    try:
        minutes = int(timer_entry.get())
        total_seconds = minutes * 60
        speak(f"Timer started for {minutes} minutes.")
        messagebox.showinfo("Timer", f"Focus mode for {minutes} minutes started!")
        threading.Thread(target=run_timer, args=(total_seconds,), daemon=True).start()
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number.")

def run_timer(seconds_left):
    while seconds_left >= 0:
        mins, secs = divmod(seconds_left, 60)
        time_display = f"{mins:02d}:{secs:02d}"
        countdown_var.set(f"⏳ Time Left: {time_display}")
        time.sleep(1)
        seconds_left -= 1

    countdown_var.set("")
    speak("Time's up! Great work!")
    messagebox.showinfo("Time's Up", "Time's up! Great work!")

# GUI setup
root = tk.Tk()
root.title("📚 Virtual Study Buddy")
root.geometry("550x650")
root.resizable(False, False)

# Style
style = ttk.Style()
style.configure("Rounded.TButton", padding=6, relief="flat", font=("Arial", 10), borderwidth=0)
style.map("Rounded.TButton", background=[("active", "#e6f0ff")])

# Style for the "Clear All" button (red)
style.configure("Danger.TButton",
    padding=6,
    relief="flat",
    font=("Arial", 10),
    borderwidth=0,
    foreground="white",
    background="#e74c3c"
)
style.map("Danger.TButton", background=[("active", "#c0392b")])

# Title
tk.Label(root, text="📚 Virtual Study Buddy", font=("Arial", 18, "bold")).pack(pady=10)

# Task input + Add Button
# Task input + Add Button (left aligned)
input_container = tk.Frame(root)
input_container.pack(fill="x", padx=50, pady=5, anchor="w")  # fill with left anchor

input_frame = tk.Frame(input_container)
input_frame.pack(anchor="w")  # align inner frame to the left

task_entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
task_entry.pack(side=tk.LEFT, padx=(0, 5))  # left-flush input

ttk.Button(input_frame, text="Add Task", command=add_task, style="Rounded.TButton").pack(side=tk.LEFT)


# "Current Tasks" + Clear All Button (side by side)
header_frame = tk.Frame(root)
header_frame.pack(fill=tk.X, padx=50, pady=(15, 5))

tk.Label(header_frame, text="Current Tasks", font=("Arial", 14, "bold")).pack(side=tk.LEFT)

tk.Button(
    header_frame,
    text="Clear All",
    command=clear_all_tasks,
    bg="#f87171",
    fg="white",
    font=("Arial", 10),
    relief="flat",
    padx=2,
    pady=1
).pack(side=tk.RIGHT)




# Task Listbox
task_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
task_listbox.pack(pady=5)
update_task_list()

# Instruction label (centered)
tk.Label(
    root,
    text="Select task to Mark as Completed or Delete Task",
    font=("Arial", 10, "bold")
).pack(pady=(5, 0))

# Complete/Delete buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(
    btn_frame,
    text="Mark as Complete",
    command=complete_task,
    bg="#76f871",
    fg="#0b5508",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=10,
    pady=4
).pack(side=tk.LEFT, padx=10)

tk.Button(
    btn_frame,
    text="Delete Task",
    command=delete_task,
    bg="#f87171",
    fg="#750909",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=10,
    pady=4
).pack(side=tk.LEFT, padx=10)

# Bottom row: Inspire Me + Study Timer
bottom_row = tk.Frame(root)
bottom_row.pack(pady=20, fill=tk.X, padx=20)

# Inspire Me button (rounded look)
ttk.Button(
    bottom_row,
    text="💡 Inspire Me",
    command=inspire_me,
    style="Rounded.TButton"
).pack(side=tk.LEFT, padx=30, ipadx=20, ipady=3)

# Timer setup
timer_frame = tk.Frame(bottom_row)
timer_frame.pack(side=tk.RIGHT, padx=(0, 25))

tk.Label(timer_frame, text="Timer (min):", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
timer_entry = tk.Entry(timer_frame, width=5, font=("Arial", 11))
timer_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(timer_frame, text="Start", command=start_timer, style="Rounded.TButton").pack(side=tk.RIGHT)

# Countdown label (animation below timer)
countdown_var = tk.StringVar()
countdown_var.set("")
countdown_label = tk.Label(root, textvariable=countdown_var, font=("Arial", 12, "bold"), fg="green")
countdown_label.pack(pady=(0, 15))

# Exit button
ttk.Button(root, text="Exit", command=root.quit, style="Rounded.TButton").pack(pady=10, ipadx=10)

# Start
speak("Hello Tehan! I'm your virtual study buddy. Ready to study? ")
root.mainloop()
