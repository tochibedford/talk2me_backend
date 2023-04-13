import sqlite3

def createTweetsTable():
    # Connect to the database
    conn = sqlite3.connect("data/tweets.db")
    conn.execute("PRAGMA timezone = 'UTC'")
    cur = conn.cursor()

    # Create the tweets table if it doesn't already exist
    cur.execute("""CREATE TABLE IF NOT EXISTS tweets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        tweet_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT (strftime('%s','now','utc'))
    ); """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def getUserFromDB(user_id):
    conn = sqlite3.connect("data/tweets.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tweets WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    conn.close()

    return result

#a function to insert or update a tweet
def insertUserTweets(user_id, tweet_text):
    conn = sqlite3.connect("data/tweets.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tweets (user_id, tweet_text, created_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (user_id, tweet_text))
    conn.commit()
    conn.close()

def updateUserTweets(user_id, tweet_text):
    conn = sqlite3.connect("data/tweets.db")
    cur = conn.cursor()
    cur.execute("UPDATE tweets SET tweet_text=?, created_at=CURRENT_TIMESTAMP WHERE user_id=?", (tweet_text, user_id))
    conn.commit()
    conn.close()