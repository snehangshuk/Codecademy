from app import db, Posts, User

import os
import datetime

#if os.path.exists('posts_DB.db'):
#  os.remove('posts_DB.db')

#db.create_all()

# user1 = User(user_id = 1, username = 'Snehangshu', email = 'snehangshu@gmail.com', password = '12345')
# user2 = User(user_id = 2, username = 'Somangshu', email = 'somangshu.karmakar@gmail.com', password = '12345')
# post1 = Posts(title = "My first post", content = "This is the very first intro post", user_id = 1)
# post2 = Posts(title = "My second post", content = "This is the very first intro post", user_id = 1)
# post3 = Posts(title = "My intro post", content = "This is the very first intro post", user_id = 2)
# db.session.add(user1)
# db.session.add(user2)
# db.session.add(post1)
# db.session.add(post2)
# db.session.add(post3)
# try:
#   db.session.commit()
# except Exception:
#   db.session.rollback()

post_rec = Posts.query.join(User.posts).filter(User.username=='Somangshu').all()
#post_rec = Posts.query.all()
for post in post_rec:
  print(post.user_id)
