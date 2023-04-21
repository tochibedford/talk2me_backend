import sqlite3
from dotenv import load_dotenv
load_dotenv()
import os
import mysql.connector as sql

if os.getenv("LOCAL") == "True":
    ssl_cert = os.getenv("SSL_CERT_LOCAL")
else:
    ssl_cert = os.getenv("SSL_CERT")

def createTweetsTable():
    conn = sql.connect(
            host= os.getenv("HOST"),
            user=os.getenv("RUSERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            ssl_verify_identity=True,
            ssl_ca=ssl_cert

        )
    cur = conn.cursor()

    # Create the tweets table if it doesn't already exist
    cur.execute("""CREATE TABLE IF NOT EXISTS tweets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id TEXT NOT NULL,
        tweet_text LONGTEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ); """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def getUserFromDB(user_id):
    conn = sql.connect(
            host= os.getenv("HOST"),
            user=os.getenv("RUSERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            ssl_verify_identity=True,
            ssl_ca=ssl_cert

        )
    cur = conn.cursor()
    cur.execute("SELECT * FROM tweets WHERE user_id=%s", (user_id,))
    result = cur.fetchone()
    conn.close()

    return result

#a function to insert or update a tweet
def insertUserTweets(user_id, tweet_text):
    conn = sql.connect(
            host= os.getenv("HOST"),
            user=os.getenv("RUSERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            ssl_verify_identity=True,
            ssl_ca=ssl_cert

        )
    cur = conn.cursor()
    cur.execute("INSERT INTO tweets (user_id, tweet_text, created_at) VALUES (%s, %s, CURRENT_TIMESTAMP)", (user_id, tweet_text))
    conn.commit()
    conn.close()

def updateUserTweets(user_id, tweet_text):
    conn = sql.connect(
            host= os.getenv("HOST"),
            user=os.getenv("RUSERNAME"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            ssl_verify_identity=True,
            ssl_ca=ssl_cert

        )
    cur = conn.cursor()
    cur.execute("UPDATE tweets SET tweet_text=%s, created_at=CURRENT_TIMESTAMP WHERE user_id=%s", (tweet_text, user_id))
    conn.commit()
    conn.close()