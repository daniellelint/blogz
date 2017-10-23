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
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(120))
    content = db.Column(db.String(250))

    def __init__(self,heading,content):
        self.heading = heading
        self.content = content

# TABLE FOR USER INFO
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self,email,password):
        self.email = email
        self.password = password

#---------------------------------------------------------
# APP LOOKS FOR ('/') ON START. MUST REDIRECT

@app.route('/', methods=['GET'])
def start():
    return redirect('/blog')

#---------------------------------------------------------

@app.route('/blog', methods=['GET'])
def main_page():
    if request.args.get('id'):
        entry_id = request.args.get('id')
        single_entry = Blog.query.get(entry_id)
        return render_template('new_entry.html',tab_title="Blog Home Page",page_header="Most Recent Entry:",single_entry=single_entry)
    else:
        posts = Blog.query.all()
        return render_template('blog.html',tab_title="Blog Home Page",page_header="Blogs:",posts=posts)

#---------------------------------------------------------

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
# "SHIELD THE CODE"
    # Shields any code within the conditional so that the code is only run when this .py file is run directly

if __name__ == '__main__':
    app.run()