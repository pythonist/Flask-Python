from flask import Flask, request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# def create_app():
#     app = Flask(__name__)

#     with app.app_context():
#         db.create_all()
#     return app

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_database.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class ToDO(db.Model):
    #schema
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow())

    #to print or get the value
    def __repr__(self):
        return f'SNo: {self.id} Title: {self.title}'


@app.route('/',methods = ["GET","POST"])
def home_page():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        todo = ToDO(title = title,description = description)
        db.session.add(todo)
        db.session.commit()
    alltodo = ToDO.query.all()
    return render_template('index.html',alltodo = alltodo)

@app.route('/about')
def new_page():  # Corrected function name
    return "This is About Page"


@app.route('/delete/<int:id>')
def delete(id):
    todo = ToDO.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     todo = ToDO.query.get(id)
#     if request.method == 'POST':
#         todo.title = request.form['title']
#         todo.description = request.form['description']
#         db.session.commit()
#         return redirect('/')
    
#     return render_template('index.html', todo=todo)

if __name__ == "__main__":
    app.run(debug=True)
