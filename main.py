# IMPORTS
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

#---------------------------------------------------------
# FLASK APP AND SQLALCHEMY CONFIGS
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:last_assignment@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#---------------------------------------------------------
# blogz = DATABASE (DB/db) NAME
# BLOG = TABLE NAME FOR BLOG POSTS
# ENTRY = SINGLE POST
# POSTS = ALL POSTS IN BLOG
# ID = SINGLE POST'S PRIMARY KEY
# HEADING = TABLE HEADER FOR BLOG & ENTRY'S TITLE
# CONTENT = TABLE HEADER FOR BLOG & ENTRY'S BODY
# USER = USER INFO TABLE IN DB
# EMAIL = TABLE HEADER FOR USER EMAIL
# PASSWORD = TABLE HEADER FOR USER PW
#---------------------------------------------------------
# PYTHON PERSISTENT CLASS THAT INITIALLY CREATES TABLE+ROWS IN MYSQL DB

# TABLE FOR POSTS
# TODO - We'll also need to amend the Blog class in main.py 
    # (and in the database) so that it has a property called 
    # owner_id which is a foreign key linking the user's id to 
    # the blog post. And we'll need to amend the Blog constructor 
    # so that it takes in a user object (again, you can review the 
    # Get It Done! code for a reminder of how to do this)
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(120))
    content = db.Column(db.String(250))

    def __init__(self,heading,content):
        self.heading = heading
        self.content = content

# TABLE FOR USER INFO
# TODO - blogs which signifies a relationship between 
    # the blog table and this user, thus binding this 
    # user with the blog posts they write.
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password):
        self.email = email
        self.password = password
#---------------------------------------------------------
# TODO - add a require_login function and decorate it with 
    # @app.before_request. 
    # The routes that we'll allow are: 'login', 'list_blogs' 
    # (or whatever you have named your route handler 
    # function for /blog), 'index', and 'signup'.
    
    # Note that when we use request.endpoint to match against 
    # our allowed_routes list, the endpoint is the name of the 
    # view function, not the url path. That is why in the list 
    # above we put 'login' in the allowed_routes list, rather 
    # than '/login'. And if you have a different name for the 
    # view function for /blog than list_blogs, substitute your 
    # function name in the list we create above.

    # If the user is trying to go to any route besides these 
    # and is not logged in (their username is not stored in a 
    # session), then we want to redirect them to the /login page.
#---------------------------------------------------------  
# TODO - We'll have a logout function that handles a POST 
    # request to /logout and redirects the user to /blog after 
    # deleting the username from the session.
#---------------------------------------------------------
# TODO - We want to require that users have an account 
    # and be logged in to be able to access the /newpost page. 
    # So we'll need the session object to work this magic. 
    # And don't forget the secret key!!
#---------------------------------------------------------
# APP LOOKS FOR ('/') ON START. MUST REDIRECT
@app.route('/', methods=['GET'])
def start():
    return redirect('/blog')
#---------------------------------------------------------
# DIPLAYS THE index.html PAGE
# OBJECTIVE - display a list of all the usernames. 
    # You can call this page "Home".
# TODO - Now we can see a list of all blogs by 
    # all users on the /blog page, but what if a visitor 
    # to the site only wants to see the blogs for a particular 
    # author? To make that easy for the visitor, let's add a 
    # "Home" page that will live at the route / and will display 
    # a list of the usernames for all the authors on the site. 
    # Make a template called index.html that displays this list, 
    # and in main.py create a route handler function for it (named
    # index so that it is included in the allowed routes we listed 
    # above).
# TODO - We also need to modify our index.html. For each author name listed, 
    # add a link to the author's individual blog user page.
    
    # User is on the / page ("Home" page) and clicks on an author's 
    # username in the list and lands on the individual blog user's page.
    
    # User is on the /blog page and clicks on the author's username 
    # in the tagline and lands on the individual blog user's page.
    
    # User is on the individual entry page (e.g., /blog?id=1) and clicks 
    # on the author's username in the tagline and lands on the individual 
    # blog user's page.
@app.route('/index', methods=['GET'])
def index():
    return redirect('/')
#---------------------------------------------------------
# HANDLES SIGNUP INFO & DIPLAYS THE signup.html FORM
# TODO - For /signup page:
    # User enters new, valid username, a valid password, and verifies password correctly and is redirected to the '/newpost' page with their username being stored in a session.
    # User leaves any of the username, password, or verify fields blank and gets an error message that one or more fields are invalid.
    # User enters a username that already exists and gets an error message that username already exists.
    # User enters different strings into the password and verify fields and gets an error message that the passwords do not match.
    # User enters a password or username less than 3 characters long and gets either an invalid username or an invalid password message.
@app.route('/signup', methods=['GET'])
def signup():
    return redirect('/')
#---------------------------------------------------------
# HANDLES LOGIN INFO & DIPLAYS THE login.html FORM
# TODO - User enters a username that is stored in the db with an 
    # incorrect password and is redirected to the /login page 
    # with a message that their password is incorrect.
    # User tries to login with a username that is not stored in 
    # the db and is redirected to the /login page with a message 
    # that this username does not exist.
# TODO - For /login page:
    # User enters a username that is stored in the database with the correct password and is redirected to the /newpost page with their username being stored in a session.
    # User enters a username that is stored in the database with an incorrect password and is redirected to the /login page with a message that their password is incorrect.
    # User tries to login with a username that is not stored in the database and is redirected to the /login page with a message that this username does not exist.
    # User does not have an account and clicks "Create Account" and is directed to the /signup page.
@app.route('/login', methods=['GET'])
def login():
    return redirect('/')
#---------------------------------------------------------
# DISPLAYS ALL BLOG POSTS ON blog.html
# GETS ID AND RENDERS new_entry.html WITH SPECIFIC ENTRY
@app.route('/blog', methods=['GET'])
def main_page():
    if request.args.get('id'):
        entry_id = request.args.get('id')
        single_entry = Blog.query.get(entry_id)
        return render_template('new_entry.html',tab_title="Blog Home Page",page_header="Most Recent Entry:",single_entry=single_entry)
    else:
        posts = Blog.query.all()
        return render_template('blog.html',tab_title="Blog Home Page",page_header="Blogs:",posts=posts)

# TODO - We will also add a singleUser.html template that will 
    # be used to display only the blogs associated with a single given 
    # author. It will be used when we dynamically generate a page 
    # using a GET request with a user query parameter on the /blog 
    # route (similar to how we dynamically generated individual blog 
    # entry pages in the last assignment).
# TODO - Just as we created a page to dynamically display individual 
    # blog posts in Build-a-Blog, we'll create a page to dynamically display the 
    # posts of each individual user. We'll use a GET request on the /blog path 
    # with a query parameter of ?user=userId where "userId" is the integer matching 
    # the id of the user whose posts we want to feature. And we'll need to create a 
    # template for this page.
    
    # There are three ways that users can reach this page and they all 
    # require that we make some changes to our templates. We will need to 
    # display, as a link, the username of the author of each blog post in 
    # a tagline on the individual blog entry page and on the /blog page. 
    # Check out our demo app and see the line "Written by..." underneath the 
    # body of the blog posts.

    # Remember that each Blog object has an owner associated with it 
    # (passed to it in the constructor), so you can access the properties of 
    # that owner (such as username, or id) with dot notation.

    # Then you'll have to amend the /blog route handler to render the correct 
    # template (either the one for the individual blog user page, or the one for 
    # the individual blog entry page) based on the arguments in the request (i.e., 
    # which name the query parameter has). If the query param is user, then you 
    # need to use the template for the individual user page and pass it a list of 
    # all the blogs associated with that user.
#---------------------------------------------------------
# DISPLAY THE NEW ENTRY FORM
# VALIDATE USER INPUT & RENDER FORM W/ ERRORS
# SUBMIT TO THE DB
# REDIRECT TO THE QUERY & DISPLAY THE SPECIFIC ENTRY

# TODO - User enters a username that is stored in the db 
    # with the correct password and is redirected to the /newpost 
    # page with their username being stored in a session.

# TODO - We'll also need to amend the Blog class in main.py 
    # (and in the database) so that it has a property called 
    # owner_id which is a foreign key linking the user's id to 
    # the blog post. And we'll need to amend the Blog constructor 
    # so that it takes in a user object (again, you can review the 
    # Get It Done! code for a reminder of how to do this). And think 
    # about what you'll need to do in your /newpost route handler 
    # function since there is a new parameter to consider when 
    # creating a blog entry.
@app.route('/new_entry', methods=['POST','GET'])
def validate_submit_form():

    if request.method == 'POST':
        heading = request.form['heading']
        content = request.form['content']

        heading_error = ''
        content_error = ''

        if len(heading) > 120:
            heading_error = "Title length requirements: 120 Characters Only"
        if len(heading) == 0:
            heading_error = "Title required to submit."
        if len(content) > 250:
            content_error = "Content length requirements: 250 Characters Only"
        if len(content) == 0:
            content_error = "Content required to submit."
        
        if heading_error or content_error:
            return render_template('form.html',
                tab_title="New Entry",page_header="New Post",
                heading_error=heading_error,content_error=content_error)
        else:
            new_entry = Blog(heading,content)
            db.session.add(new_entry)
            db.session.commit()
            query = "/blog?id=" + str(new_entry.id)
            return redirect(query)

    return render_template('form.html',tab_title="New Entry",page_header="New Post")
#---------------------------------------------------------
# Functionality Check:
    # User is logged in and adds a new blog post, then is redirected to a page featuring the individual blog entry they just created (as in Build-a-Blog).
    # User visits the /blog page and sees a list of all blog entries by all users.
    # User clicks on the title of a blog entry on the /blog page and lands on the individual blog entry page.
    # User clicks "Logout" and is redirected to the /blog page and is unable to access the /newpost page (is redirected to /login page instead).
#---------------------------------------------------------
# "SHIELD THE CODE"
    # Shields any code within the conditional so that the code is only run when this .py file is run directly

if __name__ == '__main__':
    app.run()