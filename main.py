from flask import Flask, render_template, request, redirect
from app import views
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # import datetime
from flask_migrate import Migrate, migrate

app = Flask(__name__)


# DATABASE SETTING

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo_list.db"
db = SQLAlchemy(app)

# Setting for migrations
migrate = Migrate(app, db)

# Creation of table model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return f"{self.sno} - {self.title}"

# Create table
#db.create_all()

# URL
@app.route('/', methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        todo_title = request.form['title']
        todo_desc = request.form['desc']
        data = Todo(title=todo_title, desc=todo_desc)
        db.session.add(data)
        db.session.commit()
        
    alltodo = Todo.query.all()
    
    return render_template("index.html", alltodo=alltodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    
    if request.method == "POST":
        todo_title = request.form['title']
        todo_desc = request.form['desc']
        data = Todo.query.filter_by(sno=sno).first()
        data.title = todo_title
        data.desc = todo_desc
        db.session.add(data)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)
   
    

# RUN
if __name__ == "__main__":
    app.run(debug=True)