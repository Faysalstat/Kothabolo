from flask import Flask, request, redirect
from flask import render_template
from flask import make_response
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
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
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
if __name__ == "__main__":
    app.run(debug=True)