from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
import datetime

app = Flask(__name__)
#set the SQLALCHEMY_DATABASE_URI key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts_DB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
#create an SQLAlchemy object named `db` and bind it to your app
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.TIMESTAMP, index = True, unique = False, default=datetime.datetime.now())
    title = db.Column(db.String(50), index = True, unique = False)
    content = db.Column(db.String(500), index = False, unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def get_post(post_id):
        post = Posts.query.get(post_id)
        if post is None:
            abort(404)
        return post

    def add_post(title, content, user_id):
        db.session.add(Posts(title=title, content=content, user_id=user_id))
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    def edit_post(self, title, content):
        self.title = title
        self.content = content
        self.created = datetime.datetime.now()
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    def delete_post(self):
        db.session.delete(self)
        try:
            db.session.commit() 
        except Exception:
            db.session.rollback()        

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)
    posts = db.relationship('Posts', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self):
        return str(self.user_id)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.user_id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)   

    #def is_authenticated(self):
        """Return True if the user is authenticated."""
    #    return self.authenticated     

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#a simple initial index
@app.route('/')
@app.route('/index')
def index():
    posts = Posts.query.all()
    return render_template('index.html', posts=posts)

# login route
@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm(meta={'csrf': False})
  if form.validate_on_submit():
    # query User here:
    user = User.query.filter_by(email=form.email.data).first()
    # check if a user was found and the form password matches here:
    if user and user.check_password(form.password.data):  
      # login user here:
      login_user(user, remember=form.remember.data)
      flash('Logged in successfully.')
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('index'))
    else:
      flash('User or password is incorrect!!')
      return redirect(url_for('login'))
  return render_template('login.html', form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    flash('Logged out successfully.')
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('index'))

# registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm(meta={'csrf': False})
  if form.validate_on_submit():
    # define user with data from form here:
    user = User(username=form.username.data, email=form.email.data)
    # set user's password here:
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('register.html', title='Register', form=form)

@app.route('/<int:post_id>')
def post(post_id):
    post = Posts.get_post(post_id)
    #postedby_id = post.user_id
    postedby = User.query.get(post.user_id)
    return render_template('post.html', post=post, postedby_name=postedby.username)

@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            Posts.add_post(title, content, current_user.user_id)
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=["GET", "POST"])
@login_required
def edit(id):
    post = Posts.get_post(id)
    posts_owned = Posts.query.join(User.posts).filter(User.username==current_user.username).all()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            for post_owned in posts_owned:
                if post.id == post_owned.id:
                    post.edit_post(title, content)
                else:
                    flash('You are not authorized to edit the post')            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
                
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=["GET", "POST"])
@login_required
def delete(id):
    post = Posts.get_post(id)
    post.delete_post()
    flash('"{}" was successfully deleted!'.format(post.title))
    return redirect(url_for('index'))   

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    #flash('You must be logged in to view that page.')
    return redirect(url_for('login'))
    #return "You are not logged in. Click here to get <a href="+ str("/login")+">Login</a>"    