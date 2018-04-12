from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(5000))

    def __init__(self, title, post):
        self.title = title
        self.post = post


#@app.route('/blog', methods=['POST', 'GET'])
#def display_all_posts():
    #all_posts = Blog.query.all()
    #return render_template('blog.html', posts=all_posts)

@app.route('/blog')
def display_indv_post():
    post_id = request.args.get('id')
    if (post_id):
        indv_post = Blog.query.get(post_id)
        return render_template('ind_post.html', ind_post=ind_post)
    else:
        all_posts = Blog.query.all()
        return render_template('blog.html', posts=all_posts)


def is_empty(x):
    if len(x) == 0:
        return True
    else:
        return False


@app.route('/newpost')
def make_new_post():
    return render_template('newpost.html')

@app.route('/newpost', methods=['GET', 'POST'])
def add_entry():

   # if request.method == 'POST':
    title_error = ''
    blog_entry_error = ''

    post_title = request.form['blog_title']
    post_entry = request.form['blog_post']
    new_post = Blog(post_title, post_entry)

    if not is_empty(post_title) and not is_empty(post_entry):
        db.session.add(new_post)
        db.session.commit()
        post_link = "/blog?id=" + str(new_post.id)
        return redirect(post_link)
    else:
        if is_empty(post_title) and is_empty(post_entry):
            title_error = "Text for blog title is missing."
            blog_entry_error = "Text for blog entry is missing."
            return render_template('newpost.html', title_error=title_error, blog_entry_error=blog_entry_error)
        elif is_empty(post_title) and not is_empty(post_entry):
            title_error = "Text for blog title is missing."
            return render_template('newpost.html', title_error=title_error, post_entry=post_entry)
        elif is_empty(post_entry) and not is_empty(post_title):
            blog_entry_error = "Text for blog entry is missing."
            return render_template('newpost.html', blog_entry_error=blog_entry_error, post_title=post_title)

    #else: 
    return render_template('newpost.html')
    

@app.route('/', methods=['POST', 'GET'])
def display_blog():
    return render_template('blog.html')


if __name__ == '__main__':
    app.run()