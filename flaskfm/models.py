from app import app, db

#the User model: each user has a username, and a playlist_id foreign key referring
#to the user's Playlist
class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(50), index = True, unique = True) 
  playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
  
  #representation method
  def __repr__(self):
        return "{}".format(self.username)

#create the Song model here + add a nice representation method
class Song(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  artist = db.Column(db.String(50), index = True, unique = False)
  title = db.Column(db.String(50), index = True, unique = False)
  n = db.Column(db.Integer, index = False, unique = False)

  #representation method
  def __repr__(self):
        return "{}".format(self.title)
    
#create the Item model here + add a nice representation method
class Item(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
  playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))

  #representation method
  def __repr__(self):
        return "{}".format(self.song_id)

#create the Playlist model here + add a nice representation method
class Playlist(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  '''To complete this one-to-many relationship, you need to add another field in the Playlist model called items (notice how we use the plural variable name since it’s a one-to-MANY relationship).
  Add a new field called items to the Playlist model instantiated using .db.relationship() that references the Item table. The backreference field should be called playlist, as in “each item belongs to a playlist”. Set lazy to dynamic and set the cascade deletion if you wish.'''
  items = db.relationship('Item', backref='playlist', lazy='dynamic')

  #representation method
  def __repr__(self):
        return "{}".format(self.items)
