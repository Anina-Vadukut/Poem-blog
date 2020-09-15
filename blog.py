from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, LoginManager, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from blog_model import Blog
from user import User
import os

app = Flask(__name__)
app.secret_key = "ysoserious"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.before_request
def before_request_func():
    db.create_all()


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

        

@app.route('/', methods=['GET', 'POST'])
def main():
        
     return render_template('base.html')



@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    
    if request.method == 'POST':
         title = request.form['title']
         body = request.form['body']
         
         if title and body:
             data = Blog(title, body, "null")
             db.session.add(data)
             db.session.commit()
             flash("Submission Successful")
         else:
             flash("Enter the required fields")
             
         return render_template('submit.html')
     
    return render_template('submit.html')



@app.route('/search', methods=['GET', 'POST'])
def search():
    result = {}
    if request.method == 'POST':
         srch = request.form['text']
    search = "%{}%".format(srch)
    records = Blog.query.filter(Blog.key.like(search)).all()
    for row in records:
        r = row.title
        result[r] = row.poem
    
    return render_template('search.html', records=result)

@app.route('/poem', methods=['GET', 'POST'])
def poem():
     return render_template('poem.html')
 
@app.route('/about', methods=['GET', 'POST'])
def about():
     return render_template('about.html')
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    #if current_user.is_authenticated:
     #   return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        #user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        flash("Welcome " + current_user.username)
        return redirect(url_for('submit'))
    return render_template('login.html', title='Sign In', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))



    
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()
     