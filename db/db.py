import sqlite3
import datetime


class Db:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()
        self.connection.execute('pragma foreign_keys=ON')
        self.create_table_users()

    def create_table_users(self):
        with self.connection:
            self.cursor.execute("""
                  CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER UNIQUE,
                      username TEXT,
                      token TEXT,        
                      date_of_create DATE
                  );
              """)
            print("[INFO] Table users created successfully")

    def user_exists(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone() is not None

    def add_user(self, user, token, date_of_create):
        with self.connection:
            self.cursor.execute("""
                   INSERT INTO users (user_id, username, token, date_of_create)
                   VALUES (?, ?, ?, ?)
               """, (
                user.id, user.username, token, date_of_create
            ))
            print(f"[INFO] User {user.id} added to the database")

    def get_token_by_user_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT token FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()
            if result:
                return result[0]  # Return the token
            else:
                return None  # Return None if no matching user_id is found

    def update_token(self, user_id, new_token, date_of_create):
        with self.connection:
            self.cursor.execute("""
                UPDATE users
                SET token = ?, date_of_create = ?
                WHERE user_id = ?
            """, (new_token, date_of_create, user_id))
            print(f"[INFO] Token for user_id {user_id} updated successfully")