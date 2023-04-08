import sqlite3

conn = sqlite3.connect('tweets.db')
cur = conn.cursor()

# cur.execute("""CREATE TABLE users(
#     id int auto_increment primary key,
#     twitter_id varchar(255) unique
# );""")

# cur.execute("""CREATE TABLE tweets (
#     user_id varchar(255),
#     tweet_id varchar(255),
#     timestamp datetime,
#     tweet_data blob,
#     PRIMARY KEY (user_id, tweet_id)
# ); """)

conn.commit()
conn.close()