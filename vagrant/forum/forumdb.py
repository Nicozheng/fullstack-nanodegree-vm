#
# Database access functions for the web forum.
# 

import time
import psycopg2 as psy
import bleach

## Database connection
DB = psy.connect("dbname=forum")
c = DB.cursor()

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    DB = psy.connect("dbname=forum")
    c = DB.cursor()
    query = 'select content,time from posts order by time desc;'
    c.execute(query)
    result = c.fetchall()
    DB.close()
    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in result]
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    content = bleach.clean(str(content))
    DB = psy.connect("dbname=forum")
    c = DB.cursor()
    c.execute("insert into posts (content) values (%s)", (content,))
    DB.commit()
    c.execute("delete from posts where content like '%cheese%';")
    # c.execute("update posts set content = 'cheese' where content like '%spam%';")
    DB.commit()
    DB.close()
    
