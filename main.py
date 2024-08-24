from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/ASUS/Desktop/Prison Management System/prisoners_collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

Bootstrap5(app)  # Initialize Flask-Bootstrap

class Inmate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    crime = db.Column(db.String(100), nullable=False)
    serve = db.Column(db.Integer, nullable=False)

class MyForm(FlaskForm):
    email = StringField(label='Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Your email is not valid")
    ])
    password = PasswordField(label='Password', validators=[
        DataRequired(message="Your password is not valid"),
        Length(min=8, message="Please enter at least 8 characters")
    ])
    submit = SubmitField(label='Submit')

class InmateForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    age = StringField(label='Age', validators=[DataRequired()])
    crime = StringField(label='Crime', validators=[DataRequired()])
    serve = StringField(label='serve', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

app.secret_key = "sauravbista"

#routing to different sections

@app.route("/", methods=["GET", "POST"])
def land():
    form = MyForm()
    if form.validate_on_submit():
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            return redirect(url_for('landing'))
        else:
            return redirect(url_for('denied'))
    return render_template("login.html", form=form)

@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/inmates", methods=["GET", "POST"])
def inmates():
    all_inmates = Inmate.query.all()
    return render_template("inmates.html", inmates=all_inmates)

@app.route("/add_inmates", methods=["GET", "POST"])
def add_inmates():
    form = InmateForm()
    if form.validate_on_submit():
        new_inmate = Inmate(
            name=form.name.data,
            age=form.age.data,
            crime=form.crime.data,
            serve=form.serve.data
        )
        db.session.add(new_inmate)
        db.session.commit()
        return redirect(url_for('inmates'))
    return render_template("add_inmates.html", form=form)

@app.route("/denied")
def denied():
    return render_template("denied.html")

@app.route("/delete/<int:id>")
def delete(id):
    inmate_to_delete = Inmate.query.get_or_404(id)
    db.session.delete(inmate_to_delete)
    db.session.commit()
    return redirect(url_for('inmates'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
