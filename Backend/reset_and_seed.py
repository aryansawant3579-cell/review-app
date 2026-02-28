"""
Reset the database and seed it with sample data.
Run from the Backend directory: python reset_and_seed.py
"""
import os
import sys

# Ensure we use the same DB path as the app (run from Backend dir)
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BACKEND_DIR)
sys.path.insert(0, BACKEND_DIR)

from app import app, db, User, Branch, Review
from seed_reviews import seed_database
import random
from datetime import datetime, timedelta


def reset_and_seed():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()
        print("Seeding database...")
        seed_database(num_branches=5, reviews_per_branch=200)
        
        # Print counts to verify
        print("\n--- Database contents ---")
        print(f"Users: {User.query.count()}")
        print(f"Branches: {Branch.query.count()}")
        print(f"Reviews: {Review.query.count()}")
        print("\n--- Login as admin ---")
        print("Email: admin@example.com")
        print("Password: password123")
        print("\nRestart the backend (python app.py) and refresh the app.")


if __name__ == "__main__":
    reset_and_seed()
