import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect("library.db")
cursor = conn.cursor()


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    available INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    FOREIGN KEY(book_id) REFERENCES books(id)
)
""")

conn.commit()


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("Library Management System")

root.geometry("1100x700")

root.configure(bg="#eaf2f8")


# ==========================================
# HEADING
# ==========================================

heading = tk.Label(
    root,
    text="LIBRARY MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#1a5276",
    fg="white",
    pady=15
)

heading.pack(fill="x")


subtitle = tk.Label(
    root,
    text="Manage Books | Issue Books | Return Books",
    font=("Arial", 12),
    bg="#eaf2f8",
    fg="#154360"
)

subtitle.pack(pady=10)


# ==========================================
# INPUT FRAME
# ==========================================

input_frame = tk.LabelFrame(
    root,
    text="Book Information",
    font=("Arial", 13, "bold"),
    bg="#d6eaf8",
    padx=15,
    pady=15
)

input_frame.pack(fill="x", padx=20, pady=10)


# Book ID

tk.Label(
    input_frame,
    text="Book ID:",
    bg="#d6eaf8"
).grid(row=0, column=0, padx=10, pady=10)

id_entry = tk.Entry(input_frame, width=25)

id_entry.grid(row=0, column=1, padx=10)


# Book Title

tk.Label(
    input_frame,
    text="Book Title:",
    bg="#d6eaf8"
).grid(row=0, column=2, padx=10)

title_entry = tk.Entry(input_frame, width=25)

title_entry.grid(row=0, column=3, padx=10)


# Author

tk.Label(
    input_frame,
    text="Author:",
    bg="#d6eaf8"
).grid(row=1, column=0, padx=10, pady=10)

author_entry = tk.Entry(input_frame, width=25)

author_entry.grid(row=1, column=1, padx=10)


# Quantity

tk.Label(
    input_frame,
    text="Quantity:",
    bg="#d6eaf8"
).grid(row=1, column=2, padx=10)

quantity_entry = tk.Entry(input_frame, width=25)

quantity_entry.grid(row=1, column=3, padx=10)


# ==========================================
# BOOK TABLE
# ==========================================

table_frame = tk.LabelFrame(
    root,
    text="Book Records",
    font=("Arial", 13, "bold"),
    bg="#eaf2f8"
)

table_frame.pack(fill="both", expand=True, padx=20, pady=10)


columns = (
    "ID",
    "Title",
    "Author",
    "Quantity",
    "Available"
)

book_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)


for col in columns:

    book_table.heading(col, text=col)

    book_table.column(
        col,
        width=150,
        anchor="center"
    )


book_table.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ==========================================
# CLEAR INPUT FIELDS
# ==========================================

def clear_fields():

    id_entry.delete(0, tk.END)

    title_entry.delete(0, tk.END)

    author_entry.delete(0, tk.END)

    quantity_entry.delete(0, tk.END)


# ==========================================
# DISPLAY BOOKS
# ==========================================

def display_books():

    for row in book_table.get_children():

        book_table.delete(row)

    cursor.execute("SELECT * FROM books")

    records = cursor.fetchall()

    for record in records:

        book_table.insert(
            "",
            tk.END,
            values=record
        )


# ==========================================
# ADD BOOK
# ==========================================

def add_book():

    title = title_entry.get().strip()

    author = author_entry.get().strip()

    quantity = quantity_entry.get().strip()

    if not title or not author or not quantity:

        messagebox.showwarning(
            "Warning",
            "Please fill all book details."
        )

        return

    try:

        quantity = int(quantity)

        if quantity <= 0:

            messagebox.showwarning(
                "Warning",
                "Quantity must be greater than zero."
            )

            return

    except ValueError:

        messagebox.showerror(
            "Error",
            "Enter a valid quantity."
        )

        return

    cursor.execute("""
    INSERT INTO books
    (title, author, quantity, available)
    VALUES (?, ?, ?, ?)
    """, (title, author, quantity, quantity))

    conn.commit()

    display_books()

    clear_fields()

    messagebox.showinfo(
        "Success",
        "Book added successfully!"
    )


# ==========================================
# SELECT BOOK
# ==========================================

def select_book(event):

    selected = book_table.focus()

    if selected:

        values = book_table.item(
            selected,
            "values"
        )

        clear_fields()

        id_entry.insert(0, values[0])

        title_entry.insert(0, values[1])

        author_entry.insert(0, values[2])

        quantity_entry.insert(0, values[3])


book_table.bind(
    "<ButtonRelease-1>",
    select_book
)


# ==========================================
# UPDATE BOOK
# ==========================================

def update_book():

    book_id = id_entry.get().strip()

    title = title_entry.get().strip()

    author = author_entry.get().strip()

    quantity = quantity_entry.get().strip()

    if not book_id or not title or not author or not quantity:

        messagebox.showwarning(
            "Warning",
            "Select a book and fill all details."
        )

        return

    try:

        quantity = int(quantity)

        if quantity < 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Error",
            "Enter a valid quantity."
        )

        return

    cursor.execute(
        "SELECT quantity, available FROM books WHERE id=?",
        (book_id,)
    )

    old_book = cursor.fetchone()

    if old_book is None:

        messagebox.showerror(
            "Error",
            "Book not found."
        )

        return

    old_quantity, old_available = old_book

    issued_count = old_quantity - old_available

    if quantity < issued_count:

        messagebox.showerror(
            "Error",
            "Quantity cannot be less than issued books."
        )

        return

    new_available = quantity - issued_count

    cursor.execute("""
    UPDATE books
    SET title=?, author=?, quantity=?, available=?
    WHERE id=?
    """, (
        title,
        author,
        quantity,
        new_available,
        book_id
    ))

    conn.commit()

    display_books()

    clear_fields()

    messagebox.showinfo(
        "Success",
        "Book updated successfully!"
    )


# ==========================================
# DELETE BOOK
# ==========================================

def delete_book():

    book_id = id_entry.get().strip()

    if not book_id:

        messagebox.showwarning(
            "Warning",
            "Select a book first."
        )

        return

    cursor.execute(
        "SELECT id FROM issued_books WHERE book_id=?",
        (book_id,)
    )

    if cursor.fetchone():

        messagebox.showerror(
            "Error",
            "This book has an outstanding issue record. Return it first."
        )

        return

    answer = messagebox.askyesno(
        "Confirm",
        "Do you want to delete this book?"
    )

    if answer:

        cursor.execute(
            "DELETE FROM books WHERE id=?",
            (book_id,)
        )

        conn.commit()

        display_books()

        clear_fields()

        messagebox.showinfo(
            "Success",
            "Book deleted successfully!"
        )


# ==========================================
# SEARCH BOOK
# ==========================================

def search_book():

    keyword = search_entry.get().strip()

    for row in book_table.get_children():

        book_table.delete(row)

    cursor.execute("""
    SELECT * FROM books
    WHERE title LIKE ? OR author LIKE ?
    """, (
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))

    records = cursor.fetchall()

    for record in records:

        book_table.insert(
            "",
            tk.END,
            values=record
        )


# ==========================================
# ISSUE BOOK
# ==========================================

def issue_book():

    book_id = id_entry.get().strip()

    student_name = student_entry.get().strip()

    if not book_id or not student_name:

        messagebox.showwarning(
            "Warning",
            "Select a book and enter student name."
        )

        return

    cursor.execute(
        "SELECT available FROM books WHERE id=?",
        (book_id,)
    )

    result = cursor.fetchone()

    if result is None:

        messagebox.showerror(
            "Error",
            "Book not found."
        )

        return

    if result[0] <= 0:

        messagebox.showwarning(
            "Warning",
            "Book is not available."
        )

        return

    cursor.execute("""
    INSERT INTO issued_books
    (book_id, student_name)
    VALUES (?, ?)
    """, (book_id, student_name))

    cursor.execute("""
    UPDATE books
    SET available = available - 1
    WHERE id=?
    """, (book_id,))

    conn.commit()

    display_books()

    display_issued_books()

    student_entry.delete(0, tk.END)

    clear_fields()

    messagebox.showinfo(
        "Success",
        "Book issued successfully!"
    )


# ==========================================
# RETURN BOOK
# ==========================================

def return_book():

    selected = issued_table.focus()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Select an issued book first."
        )

        return

    values = issued_table.item(
        selected,
        "values"
    )

    issue_id = values[0]

    book_id = values[1]

    cursor.execute(
        "DELETE FROM issued_books WHERE id=?",
        (issue_id,)
    )

    cursor.execute("""
    UPDATE books
    SET available = available + 1
    WHERE id=?
    """, (book_id,))

    conn.commit()

    display_books()

    display_issued_books()

    messagebox.showinfo(
        "Success",
        "Book returned successfully!"
    )


# ==========================================
# DISPLAY ISSUED BOOKS
# ==========================================

def display_issued_books():

    for row in issued_table.get_children():

        issued_table.delete(row)

    cursor.execute("""
    SELECT
        issued_books.id,
        books.id,
        books.title,
        issued_books.student_name
    FROM issued_books
    JOIN books
    ON issued_books.book_id = books.id
    """)

    records = cursor.fetchall()

    for record in records:

        issued_table.insert(
            "",
            tk.END,
            values=record
        )


# ==========================================
# BUTTON FRAME
# ==========================================

button_frame = tk.Frame(
    root,
    bg="#eaf2f8"
)

button_frame.pack(pady=10)


# ADD BUTTON

tk.Button(
    button_frame,
    text="Add Book",
    width=15,
    bg="#229954",
    fg="white",
    command=add_book
).grid(row=0, column=0, padx=5)


# UPDATE BUTTON

tk.Button(
    button_frame,
    text="Update Book",
    width=15,
    bg="#2874a6",
    fg="white",
    command=update_book
).grid(row=0, column=1, padx=5)


# DELETE BUTTON

tk.Button(
    button_frame,
    text="Delete Book",
    width=15,
    bg="#c0392b",
    fg="white",
    command=delete_book
).grid(row=0, column=2, padx=5)


# CLEAR BUTTON

tk.Button(
    button_frame,
    text="Clear",
    width=15,
    bg="#7f8c8d",
    fg="white",
    command=clear_fields
).grid(row=0, column=3, padx=5)


# ==========================================
# SEARCH FRAME
# ==========================================

search_frame = tk.Frame(
    root,
    bg="#eaf2f8"
)

search_frame.pack(pady=5)


tk.Label(
    search_frame,
    text="Search Book:",
    bg="#eaf2f8",
    font=("Arial", 11)
).grid(row=0, column=0, padx=5)


search_entry = tk.Entry(
    search_frame,
    width=30
)

search_entry.grid(row=0, column=1, padx=5)


tk.Button(
    search_frame,
    text="Search",
    command=search_book,
    bg="#8e44ad",
    fg="white"
).grid(row=0, column=2, padx=5)


tk.Button(
    search_frame,
    text="Show All",
    command=display_books,
    bg="#34495e",
    fg="white"
).grid(row=0, column=3, padx=5)


# ==========================================
# ISSUE BOOK FRAME
# ==========================================

issue_frame = tk.LabelFrame(
    root,
    text="Issue Book",
    font=("Arial", 12, "bold"),
    bg="#d5f5e3",
    padx=10,
    pady=10
)

issue_frame.pack(fill="x", padx=20, pady=10)


tk.Label(
    issue_frame,
    text="Student Name:",
    bg="#d5f5e3"
).grid(row=0, column=0, padx=10)


student_entry = tk.Entry(
    issue_frame,
    width=30
)

student_entry.grid(row=0, column=1, padx=10)


tk.Button(
    issue_frame,
    text="Issue Selected Book",
    command=issue_book,
    bg="#239b56",
    fg="white",
    width=20
).grid(row=0, column=2, padx=10)


# ==========================================
# ISSUED BOOKS TABLE
# ==========================================

issued_frame = tk.LabelFrame(
    root,
    text="Issued Books Records",
    font=("Arial", 12, "bold"),
    bg="#eaf2f8"
)

issued_frame.pack(fill="both", expand=True, padx=20, pady=10)


issued_columns = (
    "Issue ID",
    "Book ID",
    "Book Title",
    "Student Name"
)


issued_table = ttk.Treeview(
    issued_frame,
    columns=issued_columns,
    show="headings",
    height=5
)


for col in issued_columns:

    issued_table.heading(
        col,
        text=col
    )

    issued_table.column(
        col,
        width=180,
        anchor="center"
    )


issued_table.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


tk.Button(
    root,
    text="Return Selected Book",
    command=return_book,
    bg="#d35400",
    fg="white",
    width=25,
    font=("Arial", 11, "bold")
).pack(pady=5)


# ==========================================
# START APPLICATION
# ==========================================

display_books()

display_issued_books()


def close_application():

    conn.close()

    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


root.mainloop()