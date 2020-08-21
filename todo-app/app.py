from flask import Flask, render_template, request, redirect, url_for, flash
from forms import TodoForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

#todos = ["Learn Python", "Learn Flask", "Build cool app"]

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myTodoDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app)

#declaring the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True) #primary key column
    todo_text = db.Column(db.String(120), index = True, unique = True) # Todo text
    
    #Get a nice printout for Todo objects
    def __repr__(self):
        return "{}".format(self.todo_text)

@app.route("/")
def index():
    todoform = TodoForm()
    todos = Todo.query.all()
    return render_template("index.html", todos=todos, template_form=TodoForm())

@app.route("/add_todo", methods=["GET", "POST"])
def add_todo():
    todoform = TodoForm()
    if request.method == "POST":
        if todoform.validate_on_submit():
            if 'add_todo' in request.form:
                #todos.append(todoform.todo_textbox.data)
                if len(todoform.todo_textbox.data) != 0:
                    db.session.add(Todo(todo_text=todoform.todo_textbox.data))
                    try:
                        db.session.commit()
                    except Exception:
                        db.session.rollback()
                else:
                    flash ("Ensure you have entered text for todo")
            return redirect(url_for('index'))    

@app.route("/done_todo/<int:todo_id>", methods=["GET", "POST"])
def done_todo(todo_id):
    todo_to_remove = Todo.query.get(todo_id)
    #using db.session delete the item
    db.session.delete(todo_to_remove)
    #commit the deletion
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')    