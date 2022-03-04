import tkinter as tk
from tkinter import ACTIVE, messagebox
import sqlite3

conn = sqlite3.connect("database.db")


# Creates the Task table
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS Task 
    (
     taskID INTEGER PRIMARY KEY AUTOINCREMENT, 
     title TEXT
    )
    """
)
conn.close()

window = tk.Tk()
window.title("To Do List")
window.geometry("500x450+500+200")
window.config(bg="black")
window.resizable(width=False, height=False)


frame = tk.Frame(window)
frame.pack(pady=20)

listbox = tk.Listbox(
    frame,
    width=25,
    height=8,
    font=("Arial", 18),
    bd=0,
    fg="black",
    highlightthickness=0,
    selectbackground="#a6a6a6",
    activestyle="none",
)


def update_list():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        rows = cur.execute("SELECT title FROM Task").fetchall()
        for item in rows:
            for string in item:
                listbox.insert("end", string)


def delete_task():
    task = listbox.get(ACTIVE)
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(
            """
            DELETE FROM Task WHERE title = (?) LIMIT 1
            """,
            (task,),
        )

    listbox.delete(ACTIVE)


def add_task():
    task = text_box.get("1.0", "end").strip()
    if task != "":
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Task (title) values (?)", (task,))
            con.commit()
        text_box.delete("1.0", "end")
        listbox.insert("end", task)
    else:
        messagebox.showwarning("warning", "Please enter some task.")


update_list()

scrollbar = tk.Scrollbar(frame, bg="gray", activebackground="gray")
scrollbar.pack(side="right", fill="both")
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)


text_box = tk.Text(font=("Arial 20"), height=1)


add_button = tk.Button(
    window,
    text="Add Task",
    command=add_task,
    font=("Arial 20 bold"),
    activebackground="yellow",
    bg="#c5f776",
    padx=20,
    pady=10,
)

delete_button = tk.Button(
    window,
    text="Delete Task",
    command=delete_task,
    font=("Arial 20 bold"),
    activebackground="yellow",
    bg="#ff8b61",
    padx=20,
    pady=10,
)

listbox.pack(side="left", fill="both")
text_box.pack(fill="x", pady=20)
add_button.pack(fill="both", expand=True, side="left")
delete_button.pack(fill="both", expand=True, side="left")
window.mainloop()
