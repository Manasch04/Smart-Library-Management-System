import csv
import json
import logging
import hashlib
import getpass
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

from datetime import datetime, timedelta
from collections import Counter

# Configure logging
logging.basicConfig(filename="library_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

FINE_PER_DAY = 5  
BOOK_DATA_FILE = "library_data.csv"
BORROW_HISTORY_FILE = "borrowing_history.csv"
USER_DATA_FILE = "users.json"
ADMIN_DATA_FILE = "admins.json"

class Library:
    def __init__(self):
        self.books = pd.DataFrame(columns=["book_id", "title", "author", "category", "available"])
        self.users = pd.DataFrame(columns=["user_id", "name", "email", "borrowed_books"])
        self.borrow_history = pd.DataFrame(columns=["user_id", "book_id", "borrowed_date", "returned"])
        self.load_data()
    
    def load_data(self):
        if os.path.exists(BOOK_DATA_FILE):
            self.books = pd.read_csv(BOOK_DATA_FILE)
        if os.path.exists(USER_DATA_FILE):
            self.users = pd.read_csv(USER_DATA_FILE)
        if os.path.exists(BORROW_HISTORY_FILE):
            self.borrow_history = pd.read_csv(BORROW_HISTORY_FILE)
    
    def save_data(self):
        self.books.to_csv(BOOK_DATA_FILE, index=False)
        self.users.to_csv(USER_DATA_FILE, index=False)
        self.borrow_history.to_csv(BORROW_HISTORY_FILE, index=False)
    
    def add_book(self, book_id, title, author, category):
        new_book = pd.DataFrame([{"book_id": book_id, "title": title, "author": author, "category": category, "available": True}])
        self.books = pd.concat([self.books, new_book], ignore_index=True)
        self.save_data()
    
    def borrow_book(self, user_id, book_id):
        if book_id in self.books["book_id"].values and user_id in self.users["user_id"].values:
            book_index = self.books[self.books["book_id"] == book_id].index
            if not book_index.empty and self.books.loc[book_index[0], "available"]:
                self.books.loc[book_index[0], "available"] = False
                new_entry = pd.DataFrame([{"user_id": user_id, "book_id": book_id, "borrowed_date": pd.Timestamp.now(), "returned": "No"}])
                self.borrow_history = pd.concat([self.borrow_history, new_entry], ignore_index=True)
                self.save_data()
                print("Book borrowed successfully!")
            else:
                print("Book is not available.")
        else:
            print("Invalid user or book ID.")
    
    def return_book(self, user_id, book_id):
        borrow_index = self.borrow_history[
            (self.borrow_history["user_id"] == user_id) & 
            (self.borrow_history["book_id"] == book_id) & 
            (self.borrow_history["returned"] == "No")
        ].index
        if not borrow_index.empty:
            self.borrow_history.loc[borrow_index, "returned"] = "Yes"
            book_index = self.books[self.books["book_id"] == book_id].index
            if not book_index.empty:
                self.books.loc[book_index[0], "available"] = True
            self.save_data()
            print("Book returned successfully!")
        else:
            print("No record found for this book being borrowed.")
    def recommend_books(self, user_id):
        if "book_id" not in self.books.columns:
            print("Error: 'book_id' column is missing from books dataset.")
            return

        if self.borrow_history.empty:
            print("No borrowing history found. Here are some popular books:")
            if self.books.empty:
                print("No books available in the library.")
                return
            top_books = self.books.sample(min(5, len(self.books)))  # Recommend random books if no history exists
            recommendations = self.books[self.books["book_id"].isin(top_books["book_id"])]
        else:
            user_borrowed = self.borrow_history[self.borrow_history["user_id"] == user_id]["book_id"].tolist()
            
            if not user_borrowed:
                print("No borrowing history found. Here are some popular books:")
                top_books = self.borrow_history["book_id"].value_counts().head(5).index
                recommendations = self.books[self.books["book_id"].isin(top_books)]
            else:
                borrowed_categories = self.books[self.books["book_id"].isin(user_borrowed)]["category"].unique()
                recommendations = self.books[
                    (self.books["category"].isin(borrowed_categories)) & (~self.books["book_id"].isin(user_borrowed))
                ]
        
        if recommendations.empty:
            print("No specific recommendations. Try exploring new categories!")
        else:
            print("Recommended Books for You:")
            print(recommendations[["title", "author", "category"]].head(5))



    
    def view_top_borrowed_categories(self):
        top_categories = self.borrow_history.merge(self.books, on="book_id")["category"].value_counts().head(5)
        print("Top 5 Borrowed Categories:")
        print(top_categories)

    def generate_visualization(self):
        plt.figure(figsize=(10, 5))
        category_counts = self.borrow_history.merge(self.books, on="book_id")["category"].value_counts()
        category_counts.plot(kind="bar", color="skyblue")
        plt.xlabel("Category")
        plt.ylabel("Number of Borrows")
        plt.title("Most Borrowed Book Categories")
        plt.show()

class User:
    @staticmethod
    def register_user(library):
        try:
            with open(USER_DATA_FILE, "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}

        user_id = input("Enter a new user ID: ")
        user_name = input("Enter the user name: ")

        if user_id in users:
            print("User ID already exists! Try another.")
            return

        password = getpass.getpass("Create a password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        users[user_id] = {"name": user_name, "password": hashed_password}

        with open(USER_DATA_FILE, "w") as f:
            json.dump(users, f, indent=4)

        print(f"User {user_name} registered successfully!")

    def login_user(library):
        try:
            with open(USER_DATA_FILE, "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("No user data found! Please register first.")
        return None

    user_id = input("Enter User ID: ")
    password = getpass.getpass("Enter Password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if user_id in users and users[user_id]["password"] == hashed_password:
        print("Login successful!")
    else:
        print("Invalid User ID or Password. Try again.")

class Admin:
    @staticmethod
    def create_admin():
        try:
            with open(ADMIN_DATA_FILE, "r") as f:
                admins = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            admins = {}

        if len(admins) >= 2:
            print("Admin registration limit reached! Only 2 admins allowed.")
            return

        admin_id = input("Create Admin ID: ")
        password = getpass.getpass("Create Admin Password: ")

        if admin_id in admins:
            print("Admin ID already exists! Try another.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        admins[admin_id] = hashed_password

        with open(ADMIN_DATA_FILE, "w") as f:
            json.dump(admins, f, indent=4)

        print("Admin registered successfully!")

    @staticmethod
    def authenticate():
        attempts = 5
        while attempts > 0:
            admin_id = input("Enter Admin ID: ")
            password = getpass.getpass("Enter Admin Password: ")

            try:
                with open(ADMIN_DATA_FILE, "r") as f:
                    admins = json.load(f)

                if admin_id in admins and admins[admin_id] == hashlib.sha256(password.encode()).hexdigest():
                    print("Authentication successful!")
                    return admin_id
            except FileNotFoundError:
                print("Admin data file not found!")
            except json.JSONDecodeError:
                print("Error reading admin data!")

            attempts -= 1
            print(f"Incorrect details. {attempts} attempts left.")

        print("Too many failed attempts. Try again later.")
        time.sleep(5)
        return None


class LibraryAnalytics:
    def __init__(self):
        if not os.path.exists(BORROW_HISTORY_FILE):
            print("No data found for analytics.")
            return
        self.df = pd.read_csv(BORROW_HISTORY_FILE)

    def generate_reports(self):
        """Generates reports on most borrowed books, active users, and late returns."""
        if self.df.empty:
            print(" No data available for generating reports.")
            return
        self.df["Due_Date"] = pd.to_datetime(self.df["Due_Date"], errors="coerce")
        self.df["Borrow_Date"] = pd.to_datetime(self.df["Borrow_Date"], errors="coerce")
        self.df["Returned"] = self.df["Returned"].fillna("No")  # Ensure missing values are handled
        
        most_borrowed = self.df["Book_Title"].value_counts().reset_index()
        most_borrowed.columns = ["Book_Title", "Borrow_Count"]
        
        active_users = self.df["User_ID"].value_counts().reset_index()
        active_users.columns = ["User_ID", "Borrow_Count"]

         
        late_returns = self.df[(self.df["Returned"] == "No") & 
                               (pd.to_datetime("today") > self.df["Due_Date"])]

        
        with pd.ExcelWriter("Library_Analytics.xlsx") as writer:
            most_borrowed.to_excel(writer, sheet_name="Most Borrowed Books", index=False)
            active_users.to_excel(writer, sheet_name="Most Active Users", index=False)
            late_returns.to_excel(writer, sheet_name="Late Returns", index=False)

        most_borrowed.to_csv("Most_Borrowed_Books.csv", index=False)
        active_users.to_csv("Most_Active_Users.csv", index=False)
        late_returns.to_csv("Late_Returns.csv", index=False)

        print("Reports Generated Successfully! Saved as CSV & Excel.")

def main():
    library = Library()
    while True:
        print("\n1. Register User")
        print("2. Login User")
        print("3. Admin Login")
        print("4. Create Admin")  
        print("5. Recommend Books")
        print("6. Exit")
        
        choice = input("Enter choice: ")
        if choice == "1":
            register_user(library)  
        elif choice == "2":
            login_user(library)
        elif choice == "3":
            if Admin.authenticate():
                Admin.admin_dashboard(library)
        elif choice == "4":
            Admin.create_admin()  
        elif choice == "5":
            user_id = input("Enter User ID: ")
            library.recommend_books(user_id)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
