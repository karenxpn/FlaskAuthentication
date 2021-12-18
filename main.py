from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from flask_login import login_required, LoginManager, logout_user, login_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from services.database_service import UserService

db.init_app(app)
service = UserService()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return service.get_user_by_id(user_id)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = service.add_user(request.form)
        if user:
            login_user(user)
            return redirect(url_for('secrets'))
        else:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = service.login_user(password=request.form.get('password'),
                                  email=request.form.get('email'))
        if user:
            login_user(user)
            return redirect(url_for('secrets'))
        else:
            return jsonify(error={"Not found": "Please check your email and password"})
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()


@app.route('/download')
@login_required
def download():
    return send_from_directory(app.static_folder, 'files/cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True)
