import json
import tkinter as tk
from tkinter import messagebox

# File to store tasks
TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    try:
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Add a new task
def add_task(tasks, description, priority, task_listbox):
    if description.strip() == "":
        messagebox.showwarning("Input Error", "Task description cannot be empty.")
        return
    tasks.append({"description": description, "priority": priority, "status": "Pending"})
    update_task_listbox(tasks, task_listbox)
    save_tasks(tasks)

# Update task listbox
def update_task_listbox(tasks, task_listbox):
    task_listbox.delete(0, tk.END)
    for idx, task in enumerate(tasks, start=1):
        task_listbox.insert(tk.END, f"{idx}. {task['description']} | Priority: {task['priority']} | Status: {task['status']}")

# Mark a task as completed
def complete_task(tasks, task_listbox):
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "No task selected.")
        return
    task_idx = selected[0]
    tasks[task_idx]["status"] = "Completed"
    update_task_listbox(tasks, task_listbox)
    save_tasks(tasks)

# Delete a task
def delete_task(tasks, task_listbox):
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "No task selected.")
        return
    task_idx = selected[0]
    tasks.pop(task_idx)
    update_task_listbox(tasks, task_listbox)
    save_tasks(tasks)

# Main GUI application
def main():
    tasks = load_tasks()

    # Initialize the main window
    root = tk.Tk()
    root.title("To-Do List")

    # Task listbox
    task_listbox = tk.Listbox(root, width=50, height=15)
    task_listbox.pack(pady=10)

    # Update task listbox on startup
    update_task_listbox(tasks, task_listbox)

    # Task description entry
    description_label = tk.Label(root, text="Task Description:")
    description_label.pack()
    description_entry = tk.Entry(root, width=50)
    description_entry.pack(pady=5)

    # Priority selection
    priority_label = tk.Label(root, text="Priority:")
    priority_label.pack()
    priority_var = tk.StringVar(value="low")
    priority_frame = tk.Frame(root)
    priority_frame.pack(pady=5)
    tk.Radiobutton(priority_frame, text="Low", variable=priority_var, value="low").pack(side=tk.LEFT)
    tk.Radiobutton(priority_frame, text="Medium", variable=priority_var, value="medium").pack(side=tk.LEFT)
    tk.Radiobutton(priority_frame, text="High", variable=priority_var, value="high").pack(side=tk.LEFT)

    # Buttons
    add_button = tk.Button(root, text="Add Task", command=lambda: add_task(tasks, description_entry.get(), priority_var.get(), task_listbox))
    add_button.pack(pady=5)

    complete_button = tk.Button(root, text="Mark as Completed", command=lambda: complete_task(tasks, task_listbox))
    complete_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Task", command=lambda: delete_task(tasks, task_listbox))
    delete_button.pack(pady=5)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
