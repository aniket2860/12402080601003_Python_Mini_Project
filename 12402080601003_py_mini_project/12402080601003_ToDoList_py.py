# Python To-Do List Application
# Enroll num : 12402080601003
# A.D Patel Institute of Technology
import tkinter as tk
from tkinter import messagebox
import json
import os

# Name of the file used to store tasks
FILE_NAME = "tasks.json"

# List to store all tasks
tasks = []

# Load previously saved tasks from the file
def load_tasks():
    global tasks

    # Check whether the task file exists
    if os.path.exists(FILE_NAME):
        try:
            # Open the file and read saved tasks
            with open(FILE_NAME, "r") as file:
                tasks = json.load(file)

        # Handle empty or unreadable JSON files
        except (json.JSONDecodeError, OSError):
            tasks = []

# Save tasks to the JSON file
def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# Display all tasks in the list box
def refresh_tasks():
    # Remove the old task list before updating it
    task_list.delete(0, tk.END)

    # Display each task with its completion status
    for task in tasks:
        status = "✓" if task["done"] else "○"
        task_list.insert(
            tk.END, f'{status}  {task["text"]}'
        )

    # Count the number of completed tasks
    count = sum(task["done"] for task in tasks)

    # Update the completion status shown on screen
    status_label.config(
        text=f"{count} of {len(tasks)} tasks completed"
    )


# Add a new task to the list
def add_task():
    # Get the text entered by the user
    text = task_entry.get().strip()

    # Do not allow empty tasks
    if not text:
        messagebox.showwarning(
            "Empty Task", "Please enter a task."
        )
        return

    # Store the new task as a dictionary
    tasks.append({"text": text, "done": False})

    # Clear the input field
    task_entry.delete(0, tk.END)

    # Save the updated list and refresh the display
    save_tasks()
    refresh_tasks()


# Mark a selected task as completed or incomplete
def toggle_task():
    # Get the selected task's position
    selection = task_list.curselection()

    # Check whether the user selected a task
    if not selection:
        messagebox.showwarning(
            "No Selection", "Select a task first."
        )
        return

    # Find the selected task using its index
    index = selection[0]

    # Reverse the completion status
    tasks[index]["done"] = not tasks[index]["done"]

    # Save and display the updated tasks
    save_tasks()
    refresh_tasks()


# Delete the selected task
def delete_task():
    # Get the selected task's position
    selection = task_list.curselection()

    # Show a warning if no task is selected
    if not selection:
        messagebox.showwarning(
            "No Selection", "Select a task to delete."
        )
        return

    # Remove the selected task from the list
    index = selection[0]
    del tasks[index]

    # Save and refresh the task list
    save_tasks()
    refresh_tasks()


# Remove all tasks that have been completed
def clear_completed():
    global tasks

    # Keep only tasks that are not completed
    tasks = [task for task in tasks if not task["done"]]

    # Save and update the task list
    save_tasks()
    refresh_tasks()


# Create the main application window
root = tk.Tk()

# Set the window title, size and background colour
root.title("My To-Do List")
root.geometry("500x550")
root.minsize(400, 450)
root.configure(bg="#F2F5FA")


# Display the main heading
title = tk.Label(
    root,
    text="MY TO-DO LIST",
    font=("Arial", 22, "bold"),
    bg="#F2F5FA",
    fg="#243B64"
)
title.pack(pady=(25, 5))


# Display a short description below the heading
subtitle = tk.Label(
    root,
    text="Organize your day, one task at a time.",
    font=("Arial", 10),
    bg="#F2F5FA",
    fg="#65748B"
)
subtitle.pack(pady=(0, 20))


# Create a frame to hold the input field and Add button
input_frame = tk.Frame(root, bg="#F2F5FA")
input_frame.pack(fill="x", padx=25)


# Create the field where users enter new tasks
task_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    relief="solid",
    bd=1
)
task_entry.pack(side="left", fill="x", expand=True, ipady=9)

# Allow users to add a task by pressing Enter
task_entry.bind("<Return>", lambda event: add_task())


# Create the Add button
add_button = tk.Button(
    input_frame,
    text="Add",
    command=add_task,
    bg="#315EFB",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=18,
    pady=8
)
add_button.pack(side="left", padx=(8, 0))


# Create the list box that displays all tasks
task_list = tk.Listbox(
    root,
    font=("Arial", 12),
    selectmode=tk.SINGLE,
    activestyle="none",
    bg="white",
    fg="#243B64",
    selectbackground="#DCE6FF",
    selectforeground="#243B64",
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground="#D8DFEA"
)
task_list.pack(fill="both", expand=True, padx=25, pady=20)


# Display the number of completed tasks
status_label = tk.Label(
    root,
    text="0 of 0 tasks completed",
    font=("Arial", 10),
    bg="#F2F5FA",
    fg="#65748B"
)
status_label.pack(pady=(0, 10))


# Create a frame to hold the action buttons
button_frame = tk.Frame(root, bg="#F2F5FA")
button_frame.pack(pady=(0, 15))


# Button to complete or undo a task
tk.Button(
    button_frame,
    text="Mark Done / Undo",
    command=toggle_task,
    bg="#18865B",
    fg="white",
    relief="flat",
    padx=12,
    pady=8
).pack(side="left", padx=4)


# Button to delete the selected task
tk.Button(
    button_frame,
    text="Delete",
    command=delete_task,
    bg="#D94343",
    fg="white",
    relief="flat",
    padx=18,
    pady=8
).pack(side="left", padx=4)


# Button to remove every completed task
tk.Button(
    button_frame,
    text="Clear Completed",
    command=clear_completed,
    bg="#52627A",
    fg="white",
    relief="flat",
    padx=12,
    pady=8
).pack(side="left", padx=4)


# Load saved tasks when the application starts
load_tasks()

# Display the loaded tasks
refresh_tasks()

# Keep the application window running
root.mainloop()