import json
import os
import logging
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

# Logging setup
logging.basicConfig(filename="library_errors.log", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# File paths
BOOKS_FILE = "books.json"
USERS_FILE = "users.json"
BORROW_HISTORY_FILE = "borrow_history.json"

# Load JSON data
def load_data(file, default_data={}):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return default_data

# Save JSON data
def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Load data
books = load_data(BOOKS_FILE, {})
users = load_data(USERS_FILE, {})
borrow_history = load_data(BORROW_HISTORY_FILE, {})

# Classes
class Book:
    def __init__(self, title, author, category, available=True):
        self.title = title
        self.author = author
        self.category = category
        self.available = available

class User:
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.password = password
        if user_id not in users:
            users[user_id] = {"name": name, "password": password, "borrowed_books": []}
            save_data(USERS_FILE, users)

    def borrow_book(self, book_title):
        if book_title in books and books[book_title]["available"]:
            books[book_title]["available"] = False
            users[self.user_id]["borrowed_books"].append(book_title)
            borrow_history.setdefault(self.user_id, []).append(book_title)
            save_data(BOOKS_FILE, books)
            save_data(BORROW_HISTORY_FILE, borrow_history)
            save_data(USERS_FILE, users)
            print(f"{self.name} borrowed {book_title}")
        else:
            print("Book is not available!")

    def return_book(self, book_title):
        if book_title in users[self.user_id]["borrowed_books"]:
            users[self.user_id]["borrowed_books"].remove(book_title)
            books[book_title]["available"] = True
            save_data(BOOKS_FILE, books)
            save_data(USERS_FILE, users)
            print(f"{self.name} returned {book_title}")
        else:
            print("Book not borrowed by user!")
    
    def get_recommendations(self):
        print("\nBook Recommendations for You:")
        user_history = borrow_history.get(self.user_id, [])
        if not user_history:
            print("No history found. Try borrowing books first!")
            return

        categories = [books[book]['category'] for book in user_history if book in books]
        most_frequent_category = max(set(categories), key=categories.count)
        recommended_books = [title for title, details in books.items() if details['category'] == most_frequent_category and details['available']]
        
        if recommended_books:
            print("Recommended Books:")
            for book in recommended_books[:3]:
                print(f"- {book}")
        else:
            print("No recommendations available.")

class Admin:
    ADMIN_ID = "admin"
    ADMIN_PASSWORD = "admin123"
    
    def authenticate(self, username, password):
        return username == self.ADMIN_ID and password == self.ADMIN_PASSWORD

    def add_book(self, title, author, category):
        books[title] = {"author": author, "category": category, "available": True}
        save_data(BOOKS_FILE, books)
        print(f"Book {title} added!")

    def remove_book(self, title):
        if title in books:
            del books[title]
            save_data(BOOKS_FILE, books)
            print(f"Book {title} removed!")
        else:
            print("Book not found!")
    
    def view_active_users(self):
        active_users = [user for user, details in users.items() if details['borrowed_books']]
        print("Active Users:", active_users if active_users else "No active users.")
    
    def view_available_books(self):
        available_books = [title for title, details in books.items() if details['available']]
        print("Available Books:")
        for book in available_books:
            print(f"- {book}")

admin = Admin()

def main():
    while True:
        print("\nLibrary Management System")
        print("1. Librarian")
        print("2. User")
        print("3. Admin")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            admin.view_active_users()
            admin.view_available_books()
        
        elif choice == "2":
            new_user = input("Are you a new user? (yes/no): ").strip().lower()
            if new_user == "yes":
                user_id = input("Enter new User ID: ")
                name = input("Enter your name: ")
                password = input("Create a password: ")
                users[user_id] = {"name": name, "password": password, "borrowed_books": []}
                save_data(USERS_FILE, users)
            else:
                while True:
                    user_id = input("Enter User ID: ")
                    password = input("Enter Password: ")
                    if user_id in users and users[user_id]["password"] == password:
                        break
                    print("Incorrect credentials. Try again.")
            
            user = User(user_id, users[user_id]["name"], users[user_id]["password"])
            while True:
                print("\nUser Menu:")
                print("1. Borrow Book")
                print("2. Return Book")
                print("3. Get Recommendations")
                print("4. Exit")
                user_choice = input("Enter choice: ")
                if user_choice == "1":
                    book_title = input("Enter Book Title: ")
                    user.borrow_book(book_title)
                elif user_choice == "2":
                    book_title = input("Enter Book Title: ")
                    user.return_book(book_title)
                elif user_choice == "3":
                    user.get_recommendations()
                elif user_choice == "4":
                    break
        
        elif choice == "3":
            username = input("Enter Admin Username: ")
            password = input("Enter Admin Password: ")
            if admin.authenticate(username, password):
                while True:
                    print("\nAdmin Menu:")
                    print("1. Add Book")
                    print("2. Remove Book")
                    print("3. Exit")
                    admin_choice = input("Enter choice: ")
                    if admin_choice == "1":
                        title = input("Enter Book Title: ")
                        author = input("Enter Author: ")
                        category = input("Enter Category: ")
                        admin.add_book(title, author, category)
                    elif admin_choice == "2":
                        title = input("Enter Book Title: ")
                        admin.remove_book(title)
                    elif admin_choice == "3":
                        break
        
        elif choice == "4":
            break

if __name__ == "__main__":
    main()

