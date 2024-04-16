from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/wasteconnect"

app.config['SECRET_KEY'] = 'super-secret-key'
db = SQLAlchemy(app)

class Trash(db.Model):
    trashid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trash_type = db.Column(db.String(80), nullable=False)
    trash_quantity = db.Column(db.String(80), nullable=False)
    no_of_items = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    trash_entries = db.relationship('Trash', backref='user', lazy=True, foreign_keys="[Trash.user_id]")

    def __init__(self, name, password, email, address):
        self.name = name
        self.password = password
        self.email = email
        self.address = address

def get_logged_in_user_id():
    # Implement logic to get the user_id of the logged-in user
    # For example, you might use session variables or user authentication
    # For now, this is a placeholder that returns a static user_id
    return 1
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('welcomePage.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about_us.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        address = request.form.get('address')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = User(name=name, address=address, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('user_register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    # Your login logic or render the login template
    return render_template('user_login.html')

@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        trash_type = request.form.get('trash_type')
        trash_quantity = request.form.get('trash_quan')
        no_of_items = request.form.get('noofit')

        # Get the user_id from the logged-in user (you need to implement this part)
        user_id = get_logged_in_user_id()

        new_trash = Trash(trash_type=trash_type, trash_quantity=trash_quantity, no_of_items=no_of_items, user_id=user_id)
        db.session.add(new_trash)
        db.session.commit()

    trash = Trash.query.all()
    return render_template('index.html', trash=trash)

@app.route('/profile', methods=["GET", "POST"])
def profile():
    user = User.query.filter_by().all()
    return render_template('profile.html', user=user)

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
