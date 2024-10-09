import sqlite3


# Create a database connection and table for users
def create_database():
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()

    # Create Users table  
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (  
                        id INTEGER PRIMARY KEY,  
                        username TEXT NOT NULL,  
                        email TEXT NOT NULL,  
                        status TEXT NOT NULL)''')

    # Insert some dummy accounts  
    cursor.execute("INSERT INTO Users (username, email, status) VALUES ('john_doe', 'john_doe@example.com', 'active')")
    cursor.execute(
        "INSERT INTO Users (username, email, status) VALUES ('jane_doe', 'jane_doe@example.com', 'inactive')")

    conn.commit()
    conn.close()


create_database()
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import schedule
import time

# Function to send notification email
def send_notification_email(to_email, subject, body):
    from_email = 'your_email@gmail.com'
    password = 'your_password'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        server.quit()

# Function to check accounts and send notifications
def check_accounts():
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()

    cursor.execute("SELECT username, email FROM Users WHERE status='inactive'")
    inactive_users = cursor.fetchall()

    for username, email in inactive_users:
        subject = "Account Inactive Notification"
        body = f"Dear {username},\n\nYour account is currently inactive. Please contact support."
        send_notification_email(email, subject, body)

    conn.close()

# Schedule the task to run every minute
schedule.every(1).minutes.do(check_accounts)

print("Automatic Account Notification program started.")

while True:
    schedule.run_pending()
    time.sleep(1)