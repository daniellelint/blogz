from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
#---------------------------------------------------------
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:last_assignment@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'ksj56na20sj9g'
#---------------------------------------------------------
# blogz = DATABASE (DB/db) NAME
# BLOG = TABLE NAME FOR BLOG POSTS
# ENTRY = SINGLE POST
# POSTS = ALL POSTS IN BLOG
# ID = SINGLE POST'S PRIMARY KEY & SINGLE USER'S PRIMARY KEY
# HEADING = TABLE HEADER FOR BLOG & ENTRY'S TITLE
# CONTENT = TABLE HEADER FOR BLOG & ENTRY'S BODY
# USER = TABLE NAME FOR USERS IN DB
# EMAIL = COLUMN HEADER FOR USER EMAIL
# PASSWORD = COLUMN HEADER FOR USER PW
# AUTHOR_ID = FOREIGN KEY LINKED TO USER.ID TO JOIN BLOG TABLE TO USER TABLE
#---------------------------------------------------------
# PYTHON PERSISTENT CLASS THAT INITIALLY CREATES TABLE+ROWS IN MYSQL DB

# TABLE FOR POSTS
# DEFINES author_id = a foreign key linking the user's id to the blog post. 
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(120))
    content = db.Column(db.String(250))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,heading,content,author):
        self.heading = heading
        self.content = content
        self.author = author

# TABLE FOR USER INFO
# DEFINES relationship between blog table and user
    # bind user with the ENTIRES they write.
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    posts = db.relationship('Blog', backref='author')

    def __init__(self,email,password):
        self.email = email
        self.password = password

    def __repr__(self):
        return self.email
#---------------------------------------------------------
# DEFINES VALIDATION FUNCTIONS (taken from user-signup assignment, adapted)
def validate_email(email):
    email_error = ''
    if email == "":
        email_error = "Email required to submit."
        return email_error
    if " " in email:
        email_error = "Email address cannot contain spaces."
        return email_error
    if len(email) >= 100:
        email_error = "Email length requirements: 3 - 100 Characters Only"
        return email_error
    if len(email) <= 3:
        email_error = "Email length requirements: 3 - 100 Characters Only"
        return email_error
    if '@' not in email:
        email_error = "Input requires the following characters to be a valid email address: @"
        return email_error
    if '.' not in email:
        email_error = "Input requires the following characters to be a valid email address: ."
        return email_error
    else:
        return ''

def validate_pw(password,password_check):
    password_error = ''
    password_check_error = ''
    if len(password) == 0 and len(password_check) == 0:
        password_error = "Password required to submit."
        return password_error
    if len(password) > 100 or len(password) < 3:
        password_error = "Password length requirements: 3 - 100 Characters Only"
        return password_error
    if " " in password:
        password_error = "Password must not contain spaces."
        return password_error 
    if password != password_check:
        password_error = "Passwords must match."
        return password_error
    else:
        return ''

def validate_nE_heading(heading):
    heading_error = ''

    if len(heading) > 120:
        heading_error = "Title length requirements: 120 Characters Only"
        return heading_error
    if len(heading) == 0:
        heading_error = "Title required to submit."
        return heading_error
    else:
        return ''

def validate_nE_content(content):
    content_error = ''

    if len(content) > 250:
        content_error = "Content length requirements: 250 Characters Only"
        return content_error
    if len(content) == 0:
        content_error = "Content required to submit."
        return content_error
    else:
        return ''
#---------------------------------------------------------
@app.before_request
def require_login():
    allowed_routes = ['login','signup','index','blog']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')
#---------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    return render_template('index.html',tab_title="Blog Home Page",users=users)
#---------------------------------------------------------
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_check = request.form['password_check']
        email_error = validate_email(email)
        password_error = validate_pw(password, password_check)
        user_exists_error = 'This user already exists'

        existing_user = User.query.filter_by(email=email).first()
        if not email_error and not password_error:
            if not existing_user:
                new_user = User(email, password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = email
                return redirect('/')
            else:
                # if it is the right email w/ the wrong password 
                    # redirected to get login
                return redirect('/login')
        else:
            return render_template('signup.html', email_error = email_error, email = email, 
                                    password_error = password_error)
    else:
        if request.method == 'GET':
            return render_template('signup.html',tab_title="Signup (get)")
#---------------------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_check = request.form['password_check']
        email_error = validate_email(email)
        password_error = validate_pw(password, password_check)
        login_error = "User does not exist"
        
        if not email_error and not password_error:
            user = User.query.filter_by(email=email).first()
            #this works with not inserted but not correct 
            if user and user.password == password:
                session['email'] = email
                return redirect('/')
            else:
                return render_template('login.html',tab_title="Log In (post1)",email=email,login_error=login_error)
        else:
            return render_template('login.html',tab_title="Log In (post2)",email_error = email_error, email = email, 
                                    password_error = password_error)
    if request.method == 'GET':
        return render_template('login.html',tab_title="Log In (get)")
#---------------------------------------------------------
@app.route('/blog', methods=['GET', 'POST'])
def main_page():
    posts = Blog.query.all()
    user = Blog.query.all()
    id = request.query_string
    if request.args.get('id'):
        entry_id = request.args.get('id')
        single_entry = Blog.query.get(entry_id)
        return render_template('single_entry.html',tab_title="View Blogs",single_entry=single_entry)
    else:
        posts = Blog.query.all()
        return render_template('blog.html',tab_title="View Blogs",posts=posts)
#---------------------------------------------------------
@app.route('/new_entry', methods=['POST','GET'])
def validate_submit_new_entry():

    if request.method == 'POST':
        heading = request.form['heading']
        content = request.form['content']

        heading_error = validate_nE_heading(heading)
        content_error = validate_nE_content(content)

        if heading_error or content_error:
            return render_template('new_entry.html',tab_title="New Entry (post)",
                heading_error=heading_error,content_error=content_error)
        else:
            email = request.form['email']
            author = User.query.filter_by(email=session['email']).first()
            new_entry = Blog(heading,content,author)
            db.session.add(new_entry)
            db.session.commit()
            query = "/blog?id=" + str(new_entry.id)
            return redirect(query)

    return render_template('new_entry.html',tab_title="New Entry (get)")
#---------------------------------------------------------  
@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')
#---------------------------------------------------------
# Functionality Check:
    # User is logged in and adds a new blog post, then is redirected to a page 
        # featuring the individual blog entry they just created (as in Build-a-Blog).
    # User visits the /blog page and sees a list of all blog entries by all users.
    # User clicks on the title of a blog entry on the /blog page and lands on the 
        # individual blog entry page.
    # User clicks "Logout" and is redirected to the /blog page and is unable to 
        # access the /newpost page (is redirected to /login page instead).
#---------------------------------------------------------
# "SHIELD THE CODE"
    # Shields any code within the conditional so that the code is only run when this .py file is run directly

if __name__ == '__main__':
    app.run()