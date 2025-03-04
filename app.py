from flask import Flask, request, redirect, session
from flask import render_template
from flask import make_response
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Sfdfds1223129xcsdfasd#sdfasd'  # Set a secret key for session security

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    birthDate = db.Column(db.String(50), default= "")
    package = db.Column(db.String(50), default= "")
    expectation = db.Column(db.String(500), default= "")

    def __repr__(self):
        return '<Profile %r>' % self.name
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/user')
        except:
            return 'There was an issue adding your user'

    else:
        users = User.query.order_by(User.id).all()
        return render_template('user.html', users=users)
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/user')
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']

        try:
            db.session.commit()
            return redirect('/user')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', user=user)


@app.route("/")
def hello_world():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        profile = Profile.query.filter_by(email=email).first()
        if profile is None:
            return redirect('/login')
        else:
            if profile.password == password:
                session['user_id'] = profile.id
                return redirect('/profile')
            else:
                return render_template('login.html', error='Incorrect password')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
      if request.method == 'POST':
        birthDate = request.form['birthDate']
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        package = request.form['package']
        expectation = request.form['expectation']
        new_user = Profile(birthDate=birthDate, email=email, name=name, password=password,package=package, expectation=expectation)

        try:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect('/profile')
        except Exception as e:
            return 'There was an issue adding creating profile'+e
      else:
        return render_template('signup.html')

@app.route("/profile")
def profile():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to signup if no user is in session
    
    user_id = session['user_id']
    profile = Profile.query.get_or_404(user_id)
    return render_template('profile.html', profile=profile)

@app.route("/home")
def goHome():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to signup if no user is in session
    
    user_id = session['user_id']
    profile = Profile.query.get_or_404(user_id)
    return render_template('index.html', profile=profile)
@app.route("/blog")
def goBlog():
    return render_template('blog.html')

@app.route("/profile")
def goProfile():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to signup if no user is in session
    
    user_id = session['user_id']
    profile = Profile.query.get_or_404(user_id)
    return render_template('profile.html', profile=profile)

@app.route("/help")
def goHelp():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to signup if no user is in session
    
    user_id = session['user_id']
    profile = Profile.query.get_or_404(user_id)
    return render_template('help.html', profile=profile)

@app.route("/latest-reflection")
def goLatestReflection():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to signup if no user is in session
    
    user_id = session['user_id']
    profile = Profile.query.get_or_404(user_id)
    return render_template('latest-reflection.html', profile=profile)

@app.route("/relief-anxity")
def goReliefAnxity():
    return render_template('anxiety-relief.html')

@app.route("/relief-stress")
def goReliefStress():
    return render_template('stress-relief.html')

@app.route("/check-in")
def goCheckIn():
    return render_template('mood-overthe-week.html')

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
if __name__ == "__main__":
    app.run(debug=True)