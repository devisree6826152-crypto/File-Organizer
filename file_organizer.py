import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime


# ----------------------------------------
# Write to log file
# ----------------------------------------
def write_log(folder_path, text):
    log_path = os.path.join(folder_path, "organize_log.txt")
    with open(log_path, "a") as log:
        log.write(text + "\n")


# ----------------------------------------
# Main Organizer Function
# ----------------------------------------
def organize_files(folder_path):
    if not folder_path:
        return

    try:
        files = os.listdir(folder_path)
        total = len(files)
        count = 0

        # Reset Progress Bar
        progress_bar["value"] = 0
        progress_bar["maximum"] = total

        write_log(folder_path, "\n------ NEW RUN: " +
                  str(datetime.now()) + " ------")

        for file in files:
            src = os.path.join(folder_path, file)

            if os.path.isfile(src):

                # Detect extension
                if "." not in file:
                    ext = "NO_EXTENSION"
                else:
                    ext = file.split(".")[-1].upper()

                # Create destination folder
                dest_folder = os.path.join(folder_path, ext)
                os.makedirs(dest_folder, exist_ok=True)

                dest = os.path.join(dest_folder, file)

                # Avoid duplicates
                if os.path.exists(dest):
                    base, extension = os.path.splitext(file)
                    file = base + "_copy" + extension
                    dest = os.path.join(dest_folder, file)

                shutil.move(src, dest)
                write_log(folder_path, f"MOVED: {file} -> {dest_folder}")

            count += 1
            progress_bar["value"] = count
            root.update_idletasks()

        messagebox.showinfo("Success", "Files organized successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ----------------------------------------
# Dark Mode Toggle
# ----------------------------------------
def toggle_dark_mode():
    if dark_mode_var.get() == 1:
        root.config(bg="#1e1e1e")
        title.config(bg="#1e1e1e", fg="white")
        select_btn.config(bg="#333333", fg="white")
        darkmode_check.config(bg="#1e1e1e", fg="white")
    else:
        root.config(bg="white")
        title.config(bg="white", fg="black")
        select_btn.config(bg="white", fg="black")
        darkmode_check.config(bg="white", fg="black")


# ----------------------------------------
# GUI WINDOW
# ----------------------------------------
root = tk.Tk()
root.title("Advanced File Organizer")
root.geometry("380x300")
root.resizable(False, False)
root.config(bg="white")

title = tk.Label(root, text="FILE ORGANIZER",
                 font=("Arial", 16, "bold"), bg="white")
title.pack(pady=10)

# Button
select_btn = tk.Button(
    root,
    text="Choose Folder",
    command=lambda: organize_files(filedialog.askdirectory()),
    font=("Arial", 12),
    padx=10,
    pady=5,
    bg="white"
)
select_btn.pack(pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, length=250)
progress_bar.pack(pady=10)

# Dark Mode Option
dark_mode_var = tk.IntVar()
darkmode_check = tk.Checkbutton(
    root,
    text="Enable Dark Mode",
    variable=dark_mode_var,
    command=toggle_dark_mode,
    bg="white",
    font=("Arial", 11)
)
darkmode_check.pack(pady=10)

root.mainloop()
