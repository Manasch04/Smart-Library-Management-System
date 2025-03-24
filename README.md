# Smart Library Management System

##  Project Overview
This is a CLI-based Smart Library Management System that allows users to borrow, return, and recommend books while maintaining user and admin authentication. The system also generates reports and visualizes library analytics.

## Features
- User Registration & Login
- Admin Registration & Authentication
- Book Borrowing & Returning
- Book Recommendations
- Analytics & Visualization

# Project Structure
`
📦 Library Management System
 ┣ 📜 library.py (Main script)
 ┣ 📜 library_data.csv (Books Data)
 ┣ 📜 borrowing_history.csv (Borrowing Records)
 ┣ 📜 users.json (User Credentials)
 ┣ 📜 admins.json (Admin Credentials)
 ┣ 📜 requirements.txt (Dependencies)
 ┗ 📜 README.md (Project Documentation)


##  Installation
Step 1: Clone the Repository
    Open a terminal and run:

 git clone https://github.com/your-username/smart-library-management-cli.git
 cd smart-library-management-cli


Step 2: Create a Virtual Environment (Recommended)

   python -m venv venv # on windows
   source venv/bin/activate  # On Linux/macOS


Step 3: Install Dependencies

  pip install -r requirements.txt

Step 4: Start the Library System

   python library.py


Step 5: Choose an Action
   Once the system starts, use the CLI menu to interact:

1. Register User
2. Login User
3. Admin Login
4. Create Admin
5. Recommend Books
6. Exit

Use **numbers** to navigate through options.

##  User Guide
### Register a New User
- Select Option 1
- Enter a unique User ID and Name
- Create a password

### Login as a User
- Select Option 2
- Enter your User ID and Password

### Admin Authentication
- Select Option 3 (Login) or Option 4 (Create Admin)
- Admins have extra privileges to manage books and reports

### Borrow a Book
- Login as a User
- Use the borrow_book() function inside the script
- The book will be marked as borrowed

### Return a Book
- Login as a User
- Use the return_book() function inside the script
- The book will be marked as available

### View Book Recommendations
- Select Option 5
- Based on past borrowing history, the system suggests books

## Analytics & Reports
   To generate borrowing analytics, run:

  python library.py --generate-reports

  This saves reports as CSV and Excel files.

## Troubleshooting
  If you encounter errors:
  1. Ensure Python 3+ is installed (python --version)
  2. Activate the virtual environment (source venv/bin/activate)
  3. Reinstall dependencies (pip install -r requirements.txt)

## Contributing
   Feel free to fork this repository and make improvements!


Enjoy using the Library Management System!

