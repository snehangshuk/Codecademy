from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, validators

class TodoForm(FlaskForm):
    todo_checkbox = BooleanField(default=False)
    todo_text = StringField("Add to the todo list")
    add_todo = SubmitField("Add Todo")
    done_todo = SubmitField("Done")