import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Fetch all emails
cursor.execute("SELECT email FROM users")
emails = cursor.fetchall()

print("Registered Emails:")
for email in emails:
    print(email[0])

conn.close()
