from flask import render_template, request, redirect, url_for, abort  
from . import main  
from .forms import BlogForm
from ..models import User 
from flask_login import login_required, current_user
from .. import db

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to The best Blog Website Online'


    return render_template('index.html', title = title)

@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        title = blog_form.title.data
        blog = blog_form.text.data
        category = blog_form.category.data

        # Updated blog instance
        new_blog = Blog(blog_title=title,blog_content=blog,category=category,user=current_user,likes=0,dislikes=0)

        # Save blog method
        new_blog.save_blog()
        return redirect(url_for('.index'))

    title = 'New blog'
    return render_template('new_blog.html',title = title,blog_form=blog_form )

@main.route('/blog/<int:id>', methods = ['GET','POST'])
def blog(id):
    blog = Blog.get_blog(id)
    posted_date = blog.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        blog.likes = blog.likes + 1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog/{blog_id}".format(blog_id=blog.id))

    elif request.args.get("dislike"):
        blog.dislikes = blog.dislikes + 1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog/{blog_id}".format(blog_id=blog.id))
    
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,blog_id = blog)

        new_comment.save_comment()


    comments = Comment.get_comments(blog)
    
    return render_template("blog.html", blog = blog, date = posted_date, comment_form = comment_form, comments = comments)

@main.route('/user/<uname>/blogs')
def user_blogs(uname):
    user = User.query.filter_by(username=uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).all()
    blogs_count = Blog.count_blogs(uname)
    user_joined = user.date_joined.strftime('%b,%d,%y')
    
    return render_template("profile/blogs.html",user = user, blogs = blogs, blogs_count= blogs_count,date= user_joined)

