"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, Users, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'secrety'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
toolbar = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()

@app.route('/')
def home_page():
    users = Users.query.all()
    """Show all of the users of blogly"""
    return redirect('/users')

@app.route('/users')
def show_users():
    users = Users.query.all()
    """Show all of the users of blogly"""
    return render_template('users.html', users = users)



@app.route('/users/new')
def add_user():
    """Add a user to the blogly db"""
    return render_template('add_users.html')



@app.route('/users', methods=['POST'])
def create_user():
    users = Users.query.all()
    """Show all of the users of blogly after adding a new user"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if image_url == "":
        image_url = 'https://img.freepik.com/premium-vector/account-icon-user-icon-vector-graphics_292645-552.jpg?w=740'

    new_user = Users(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/')



@app.route('/users/<int:id>')
def user_details(id):
    """Shows the details of a user"""

    user = Users.query.get_or_404(id)
    posts = Post.query.filter(Post.user_id == id)
    return render_template('user_details.html', user=user, posts = posts)



@app.route('/users/<int:id>/edit')
def edit_user_info(id):
    """Shows the edit user form"""
    user = Users.query.get(id)
    return render_template('user_edit.html', user=user)



@app.route('/users/<int:id>/edit', methods=['POST'])
def update_db(id):
    """Returns to users detail page after updating their information and updates the DB"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    updated_user = Users.query.get(id)

    updated_user.first_name = first_name
    updated_user.last_name = last_name
    updated_user.image_url = image_url

    db.session.commit()
    
    return redirect('/users')




@app.route('/users/<int:id>/delete', methods=['POST'])
def remove_user_from_db(id):
    """Selects a user based on their id and removes them from the DB"""
    id = id

    Users.query.filter_by(id = id).delete()
    db.session.commit()
    
    users = Users.query.all()

    return render_template('users.html', users=users)




"""Post functionality """
@app.route('/users/<int:id>/posts/new')
def show_add_post_form(id):

    user = Users.query.get(id)
    tags = Tag.query.all()
    """Show form to add a post for user"""
    return render_template('post_form.html', user = user, tags = tags)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def submit_post_create_form(id):
    """Handle add form; add post and redirect to the user details page"""

    post_title = request.form['post-title']
    post_content = request.form['post-content']
    user_id = id
    tags = request.form.getlist('post-tags', type=str)

    new_post = Post(title = post_title, content = post_content, user_id = user_id )

    db.session.add(new_post)
    db.session.commit()

    for tag in tags:
        tag_id = Tag.query.filter(Tag.name == tag).one().id
        post_tag = PostTag(post_id = new_post.id, tag_id = tag_id)
        db.session.add(post_tag)
        db.session.commit()

    return redirect(f'/users/{id}')

@app.route('/posts/<int:id>')
def show_posts(id):
    """Show a post. Show buttons to edit and delete the post"""
    post = Post.query.get(id)
    post_tags = post.tag
    return render_template('post_page.html', post = post, post_tags = post_tags)

@app.route('/posts/<int:id>/edit')
def show_edit_post_form(id):
    """Show form to edit a post, and to cancel (back to user page)"""
    post = Post.query.get(id)
    tags = Tag.query.all()

    return render_template('post_edit_form.html', post=post, tags = tags )

@app.route('/posts/<int:id>/edit', methods=['POST'])
def submit_post_edit_form(id):
    """Handle editing of post. Redirect back to the post view"""

    updated_post = Post.query.get(id)
    updated_post.title = request.form['post-title']
    updated_post.content = request.form['post-content']
    tags = request.form.getlist('post-tags', type=str)

    db.session.add(updated_post)
    db.session.commit()

    existing_post_tags = PostTag.query.filter(PostTag.post_id == id).all()

    for post_tag in existing_post_tags:
        db.session.delete(post_tag)
        db.session.commit()

    for tag in tags:
        tag_id = Tag.query.filter(Tag.name == tag).one().id
        post_tag = PostTag(post_id = updated_post.id, tag_id = tag_id)
        db.session.add(post_tag)
        db.session.commit()

    return redirect(f'/posts/{id}')
    
@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    """Handle editing of post. Redirect back to the post view"""

    user_id = Post.query.get(id).user.id
    Post.query.filter(Post.id == id).delete()
    db.session.commit()

    
    return redirect(f'/users/{user_id}')



"""Tag functionality"""



@app.route('/tags')
def show_all_tags():
    """List all tags, with links to the tag detail page"""
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/<int:id>')
def show_tag_details(id):
    """Show detail about a tag, including which posts they occur in. Has links to edit form and to the delete"""
    tag = Tag.query.get(id)
    posts = tag.post
    return render_template('tag_details.html', tag = tag, posts = posts )

@app.route('/tags/new')
def show_tag_form():
    """Shows a form to add a new tag"""
    return render_template('tag_create_form.html')

@app.route('/tags/new', methods=['POST'])
def handle_tag_add_form():
    """Handle tag add form and redirect to tag list"""
    tag_name = request.form['tag-name']
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:id>/edit')
def show_tag_edit_form(id):
    """Show edit form for a tag"""

    tag = Tag.query.get(id)
    return render_template('/tag_edit_form.html', tag = tag)

@app.route('/tags/<int:id>/edit', methods = ['POST'])
def handle_tag_edit_form(id):
    """Handle edit tag form and redirect to tag list"""
    
    updated_tag = Tag.query.get(id)
    updated_tag.name = request.form['tag-name']
    db.session.add(updated_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    """Deletes a tag"""
    Tag.query.filter(Tag.id == id).delete()
    db.session.commit()
    return redirect('/tags')