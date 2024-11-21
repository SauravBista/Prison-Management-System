Prison Management System

This is a simple Prison Management System built with Flask. It includes functionality for managing inmate records, including adding, viewing, and deleting inmates, and provides a login system for administrators.
Features

    Admin Login: Secure login page for administrators to access the system.
    View Inmates: Display a list of all inmates stored in the database.
    Add Inmates: Form to add new inmate records to the database.
    Delete Inmates: Option to delete inmate records.
    Form Validation: Uses Flask-WTF and WTForms for secure and user-friendly form handling.
    Bootstrap Integration: Utilizes Bootstrap 5 for responsive and modern design.

Prerequisites

    Python 3.x
    Flask
    Flask-WTF
    Flask-Bootstrap
    Flask-SQLAlchemy

Installation

    Clone the repository:

    bash

git clone https://github.com/yourusername/prison-management-system.git
cd prison-management-system

Create a virtual environment and activate it:

bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the dependencies:

bash

pip install flask flask-wtf flask-bootstrap flask-sqlalchemy

Run the application:

bash

    python app.py

    The application will run on http://127.0.0.1:5000/.

Project Structure

bash

Prison Management System/
│
├── templates/                 # HTML templates
│   ├── login.html             # Login page
│   ├── landing.html           # Landing page
│   ├── inmates.html           # View inmates page
│   ├── add_inmates.html       # Add inmate form page
│   └── denied.html            # Access denied page
│
├── app.py                     # Main Flask application
├── prisoners_collection.db    # SQLite database file
└── README.md                  # This README file

Database

The project uses SQLite as the database. The database file is located at:

javascript

C:/Users/ASUS/Desktop/Prison Management System/prisoners_collection.db

Make sure this path is correct, or update the SQLALCHEMY_DATABASE_URI configuration in app.py to point to the correct database location.
Usage
Admin Login

    Navigate to http://127.0.0.1:5000/ to access the login page.

    Use the credentials:

    makefile

    Email: admin@email.com
    Password: 12345678

Managing Inmates

    View Inmates: After logging in, click on "View Inmates" to see all inmate records.
    Add Inmates: Use the "Add Inmate" button to add new inmate records.
    Delete Inmates: Use the delete button next to an inmate to remove them from the database.

License

This project is open-source and available under the MIT License.
Author

Saurav Bista
GitHub: sauravbista
