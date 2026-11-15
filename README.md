📚 Library Management System

1. Introduction

The Library Management System is a desktop-based application developed using Python. It is designed to manage library activities easily and efficiently.

This project helps librarians maintain book records, search books, issue books to students, and manage book returns.

2. Objectives

- To manage library records digitally.
- To reduce manual paperwork.
- To make book searching easier.
- To maintain book issue and return records.
- To save time and improve accuracy.

3. Technologies Used

- Programming Language: Python
- Frontend: Tkinter
- Backend: SQLite Database
- IDE: Visual Studio Code

4. Features

1. Add new books.
2. Display all books.
3. Search books by title or author.
4. Update book information.
5. Delete book records.
6. Issue books to students.
7. Return issued books.
8. Automatically update book availability.
9. Store records permanently in a database.

5. Project Folder Structure

Library_Management_System/
│
├── main.py
├── library.db
├── README.md
└── .gitignore

6. Installation and Execution

Follow these steps to run the project:

1. Install Python on your computer.
2. Download or clone this repository.
3. Open the project folder in VS Code.
4. Open the terminal.
5. Run the following command:

python main.py

6. The Library Management System application will open.

7. Database

SQLite is used to store book details and student issue records.

The database contains two tables:

- Books: Stores book ID, title, author, quantity, and availability.
- Issued Books: Stores issue ID, book ID, and student name.

8. Advantages

- Easy to use.
- Saves time.
- Reduces paperwork.
- Provides quick book searching.
- Maintains organized records.
- Automatically manages available book quantities.

9. Future Scope

- Admin login system.
- Student registration.
- Automatic fine calculation.
- Issue and return dates.
- Generate library reports.
- Export records to Excel.

10. Developed By

Name: Praminder Kaur

Course: B.Tech CSE (AI & ML)

Project: Library Management System

11. Conclusion

The Library Management System makes library management easier, faster, and more organized. It demonstrates the practical use of Python programming, GUI development, and database management.