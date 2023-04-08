import sqlite3

conn = sqlite3.connect('src/tweets.db')
cur = conn.cursor()

# cur.execute("""CREATE TABLE users(
#     id int auto_increment primary key,
#     twitter_id varchar(255) unique
# );""")

cur.execute("""CREATE TABLE tweets (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    tweet_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); """)

conn.commit()
conn.close()