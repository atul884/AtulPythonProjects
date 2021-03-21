from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email

 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Atulblog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jack'
 
db = SQLAlchemy(app)
 
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
 
@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
 
    return render_template('index.html', posts=posts)
 
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
 
    return render_template('post.html', post=post)
 
@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/add')
def add():
    return render_template('add.html')
 
@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
 
    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
 
    db.session.add(post)
    db.session.commit()
 
    return redirect(url_for('index'))

class SignUpForm(Form):
    firstname= TextField('First Name', validators= [DataRequired()])
    lastname = TextField('Last Name', validators= [DataRequired()])
    username = TextField('User Name', validators= [ DataRequired()])
    password = PasswordField('Password',validators=[ DataRequired()])
    email = EmailField('Email', validators= [DataRequired(), Email()])
    submit = SubmitField('Sign Up')


class SignInForm(Form):
    email = EmailField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min=6, max=30)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')

class AboutUserForm(Form):
    firstname= TextField('First Name', validators= [DataRequired()])
    lastname = TextField('Last Name', validators= [DataRequired()])
    username = TextField('User Name', validators= [ DataRequired()])
    password = PasswordField('Password',validators=[ DataRequired()])
    email = EmailField('Email', validators= [DataRequired(), Email()])


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signupform = SignUpForm(request.form)
    if request.method == 'POST':
        reg = User(signupform.firstname.data, signupform.lastname.data,\
         signupform.username.data, signupform.password.data,\
         signupform.email.data)
        db.session.add(reg)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('signup.html', signupform=signupform)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    signinform = SignInForm()
    if request.method == 'POST':
        em = signinform.email.data
        log = User.query.filter_by(email=em).first()
        if log.password == signinform.password.data:
            current_user = log.username
            session['current_user'] = current_user
            session['user_available'] = True
            return redirect(url_for('show_posts'))
    return render_template('signin.html', signinform=signinform)

@app.route('/about_user')
def about_user():
    aboutuserform = AboutUserForm()
    if session['user_available']:
        user = User.query.filter_by(username=session['current_user']).first()
        return render_template('about_user.html', user=user, aboutuserform=aboutuserform)
    flash('You are not a Authenticated User')
    return redirect(url_for('index'))



@app.route('/logout')
def logout():
    session.clear()
    session['user_available'] = False
    return redirect(url_for('index'))

  
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
