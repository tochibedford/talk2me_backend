import sqlite3

conn = sqlite3.connect('/application/data/tweets.db')

# database has the schema:

# cur.execute("""CREATE TABLE tweets (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id TEXT NOT NULL,
#     tweet_text TEXT NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# ); """)

# conn.commit()
# conn.close()

def getUserFromDB(user_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tweets WHERE user_id=?", (user_id,))
    result = cur.fetchone()

    return result

#a function to insert or update a tweet
def insertUserTweets(user_id, tweet_text):
    cur = conn.cursor()
    cur.execute("INSERT INTO tweets (user_id, tweet_text, created_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (user_id, tweet_text))
    conn.commit()

def updateUserTweets(user_id, tweet_text):
    print(user_id, tweet_text)
    cur = conn.cursor()
    cur.execute("UPDATE tweets SET tweet_text=?, created_at=CURRENT_TIMESTAMP WHERE user_id=?", (tweet_text, user_id))
    conn.commit()