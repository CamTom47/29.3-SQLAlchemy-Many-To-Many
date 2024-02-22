"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, Users
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

    new_user = Users(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/')



@app.route('/users/<int:id>')
def user_details(id):
    """Shows the details of a user"""

    user = Users.query.get_or_404(id)
    return render_template('user_details.html', user=user)



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