from flask import Flask, render_template, request, redirect, url_for
from forms import TodoForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

todos = ["Learn Python", "Learn Flask", "Build cool app"]

@app.route("/", methods=["GET", "POST"])
def index():
    todoform = TodoForm()
    if request.method == "POST":
        if todoform.validate_on_submit():
            if 'add_todo' in request.form:
                todos.append(todoform.todo_text.data)
            elif 'done_todo' in request.form:
                #pass
                #if todoform.todo_checkbox.data == "True":
                #    done_value = todoform.todo_checkbox.label
                #    todos.remove(done_value)
    return render_template("index.html", todos=todos, template_form=TodoForm())