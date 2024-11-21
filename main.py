from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.file import FileAllowed, FileRequired
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/ASUS/Desktop/Prison Management System/prisoners_collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16 MB

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Create the uploads folder if it does not exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

Bootstrap5(app)  # Initialize Flask-Bootstrap

class Inmate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    crime = db.Column(db.String(100), nullable=False)
    serve = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(100), nullable=True)
    date_of_arrest = db.Column(db.Date)
    serve_time = db.Column(db.Integer)  # Number of days to serve
    release_date = db.Column(db.Date)  # This field can be calculated
    
    def __repr__(self):
        return f'<Inmate {self.name}>'

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
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    age = IntegerField('Age', validators=[DataRequired()])
    crime = StringField('Crime', validators=[DataRequired()])
    
    # Date of arrest as a DateField
    date_of_arrest = DateField('Date of Arrest', format='%Y-%m-%d', validators=[DataRequired()])

    # Serve time in days as an IntegerField
    serve = IntegerField('Serve Time (in days)', validators=[DataRequired()])
    
    # Photo field remains the same
    photo = FileField('Inmate Photo', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    
    submit = SubmitField('Submit')

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
    
    # Calculate the date of release for each inmate
    inmates = Inmate.query.all()  # Assuming you're using SQLAlchemy to fetch inmates from the database
    
    for inmate in inmates:
        # Make sure the serve_time and date_of_arrest are available
        if inmate.serve_time and inmate.date_of_arrest:
            # Calculate the release date by adding serve_time (in days) to date_of_arrest
            inmate.release_date = inmate.date_of_arrest + timedelta(days=inmate.serve_time)
        else:
            inmate.release_date = None  # If serve_time or date_of_arrest is missing, leave release_date as None
        
        # Convert dates to strings for better display in the template
        if inmate.date_of_arrest:
            inmate.date_of_arrest_str = inmate.date_of_arrest.strftime('%Y-%m-%d')
        else:
            inmate.date_of_arrest_str = "N/A"
        
        if inmate.release_date:
            inmate.release_date_str = inmate.release_date.strftime('%Y-%m-%d')
        else:
            inmate.release_date_str = "N/A"  # If no release_date is calculated

    return render_template('inmates.html', inmates=inmates)
    
    # Optionally, commit changes to the database if you want to save release_date changes
    # db.session.commit()

    return render_template('inmates.html', inmates=inmates)

@app.route("/add_inmates", methods=["GET", "POST"])
def add_inmates():
    form = InmateForm()

    if form.validate_on_submit():
        # Handle file upload
        filename = None
        if form.photo.data:
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)

        # Process other form fields (e.g., name, age, crime, etc.)
        # Assuming you're saving these to a database:
        new_inmate = Inmate(
            name=form.name.data,
            age=form.age.data,
            crime=form.crime.data,
            serve=form.serve.data,
            photo=filename  # Save filename, not the file object
        )
        db.session.add(new_inmate)
        db.session.commit()

        flash('Inmate added successfully!', 'success')
        return redirect(url_for('inmates'))  # Redirect to the inmates view page

    return render_template('add_inmates.html', form=form)

@app.route("/denied")
def denied():
    return render_template("denied.html")

@app.route("/delete/<int:id>")
def delete(id):
    inmate_to_delete = Inmate.query.get_or_404(id)
    db.session.delete(inmate_to_delete)
    db.session.commit()
    return redirect(url_for('inmates'))

@app.route('/edit_inmate/<int:id>', methods=['GET', 'POST'])
def edit_inmate(id):
    # Fetch the inmate by ID
    inmate = Inmate.query.get_or_404(id)
    
    if request.method == 'POST':
        # Get form data
        inmate.name = request.form['name']
        inmate.age = request.form['age']
        inmate.crime = request.form['crime']
        inmate.serve = request.form['serve']
        
        # Handle photo upload if a new photo is provided
        photo = request.files.get('photo')
        if photo:
            # Save the new photo and update the inmate's photo field
            photo_filename = save_photo(photo)  # Assuming save_photo is a function that saves the file
            inmate.photo = photo_filename

        # Commit changes to the database
        db.session.commit()

        # Redirect to the inmates list page
        return redirect(url_for('inmates'))  # Adjust the URL to your listing page

    # If GET request, display the current data in the form
    return render_template('edit_inmate.html', inmate=inmate)

def save_photo(photo):
    filename = secure_filename(photo.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    photo.save(filepath)
    return filename

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
