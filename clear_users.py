import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Delete all rows from users table
cursor.execute("DELETE FROM users")
conn.commit()

print("All user accounts have been deleted.")

conn.close()
