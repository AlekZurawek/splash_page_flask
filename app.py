from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key_here" # replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self, email, name):
        self.email = email
        self.name = name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        new_user = User(email=email, name=name)
        db.session.add(new_user)
        db.session.commit()

        session['base_grant_url'] = request.form.get('base_grant_url')
        session['user_continue_url'] = request.form.get('user_continue_url')

        print("Base grant URL: ", session['base_grant_url']) # Debug print
        print("User continue URL: ", session['user_continue_url']) # Debug print

        return redirect(url_for('auth', duration=cfg['session_duration']))
    return render_template('splash.html')

@app.route('/auth', methods=['GET'])
def auth():
    base_grant_url = session.get('base_grant_url')
    user_continue_url = session.get('user_continue_url')

    # the rest of your logic here

    return redirect('https://www.google.com') # Updated this line

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
