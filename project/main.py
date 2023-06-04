from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Restaurant, MenuItem, User, Rating, Booking
from datetime import datetime, timedelta
from sqlalchemy import asc, text
from . import db

main = Blueprint('main', __name__)
#Show all restaurants
@main.route('/')
@main.route('/restaurant/')
def showRestaurants():
  restaurants = db.session.query(Restaurant).order_by(asc(Restaurant.name))
  return render_template('restaurants.html', restaurants = restaurants)

#Create a new restaurant
@main.route('/restaurant/new/', methods=['GET','POST'])
@login_required
def newRestaurant():
  if request.method == 'POST':
      newRestaurant = Restaurant(name = request.form['name'])
      db.session.add(newRestaurant)
      flash('New Restaurant %s Successfully Created' % newRestaurant.name)
      db.session.commit()
      return redirect(url_for('main.showRestaurants'))
  else:
      return render_template('newRestaurant.html')

#Edit a restaurant
@main.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
@login_required
def editRestaurant(restaurant_id):
  editedRestaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedRestaurant.name = request.form['name']
        flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
        return redirect(url_for('main.showRestaurants'))
  else:
    return render_template('editRestaurant.html', restaurant = editedRestaurant)


#Delete a restaurant
@main.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET','POST'])
@login_required
def deleteRestaurant(restaurant_id):
  restaurantToDelete = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
    db.session.delete(restaurantToDelete)
    flash('%s Successfully Deleted' % restaurantToDelete.name)
    db.session.commit()
    return redirect(url_for('main.showRestaurants', restaurant_id = restaurant_id))
  else:
    return render_template('deleteRestaurant.html',restaurant = restaurantToDelete)

#Show a restaurant menu
@main.route('/restaurant/<int:restaurant_id>/')
@main.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', items = items, restaurant = restaurant)
     


#Create a new menu item
@main.route('/restaurant/<int:restaurant_id>/menu/new/',methods=['GET','POST'])
@login_required
def newMenuItem(restaurant_id):
  restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
      newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
      db.session.add(newItem)
      db.session.commit()
      flash('New Menu %s Item Successfully Created' % (newItem.name))
      return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
  else:
      return render_template('newmenuitem.html', restaurant_id = restaurant_id)

#Edit a menu item
@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
@login_required
def editMenuItem(restaurant_id, menu_id):

    editedItem = db.session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        db.session.add(editedItem)
        db.session.commit() 
        flash('Menu Item Successfully Edited')
        return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)

#Delete a menu item
@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
@login_required
def deleteMenuItem(restaurant_id,menu_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    itemToDelete = db.session.query(MenuItem).filter_by(id = menu_id).one() 
    if request.method == 'POST':
        db.session.delete(itemToDelete)
        db.session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item = itemToDelete)
    
@main.route('/restaurant/<int:restaurant_id>/menu/1/')
@login_required
def rating1(restaurant_id):
    newRating = Rating(r_id=restaurant_id,u_id = current_user.u_id, score = 1)
    db.session.add(newRating)
    flash('only 1 :(')
    db.session.commit()
    return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
    
            
@main.route('/restaurant/<int:restaurant_id>/menu/2/')
@login_required
def rating2(restaurant_id):
    newRating = Rating(r_id=restaurant_id,u_id = current_user.u_id, score = 2)
    db.session.add(newRating)
    flash('2...really')
    db.session.commit()
    return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))

@main.route('/restaurant/<int:restaurant_id>/menu/3/')
@login_required
def rating3(restaurant_id):
    newRating = Rating(r_id=restaurant_id,u_id = current_user.u_id, score = 3)
    db.session.add(newRating)
    flash('guess we can do better')
    db.session.commit()
    return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))

@main.route('/restaurant/<int:restaurant_id>/menu/4/')
@login_required
def rating4(restaurant_id):
    newRating = Rating(r_id=restaurant_id,u_id = current_user.u_id, score = 4)
    db.session.add(newRating)
    flash('good enuf')
    db.session.commit()
    return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))

@main.route('/restaurant/<int:restaurant_id>/menu/5/')
@login_required
def rating5(restaurant_id):
    newRating = Rating(r_id=restaurant_id,u_id = current_user.u_id, score = 5)
    db.session.add(newRating)
    flash('thank you for the rating!!!')
    db.session.commit()
    return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))

#login
@main.route('/login')
def login():
    return render_template('login.html')

#login is as a user
@main.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    #checks the database for the user and hashed passwords
    if not user or not (check_password_hash(user.password, password)):
        flash('Please check your login details and try again.')
        current_app.logger.warning("User login failed")
        return redirect(url_for('main.login')) # reloads the page if failed login
    
    # user is logged in and redirects to the profile page
    login_user(user)
    return redirect(url_for('main.profile'))
# profile page
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

# signup page
@main.route('/signup')
def signup():
    return render_template('signup.html')

#sign up as a user
@main.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password = generate_password_hash(password, method='sha256')
    user = db.session.execute(text('select * from user where email = "?"')).all()
    if len(user) > 0: 
        flash('Email address already exists')  
        current_app.logger.debug("User email already exists")
        return redirect(url_for('main.signup'))

    new_user = User(email=email, name=name, password=password)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.login'))

#logout
@main.route('/logout')
@login_required
def logout():
    logout_user();
    return redirect(url_for('main.showRestaurants'))

#booking
@main.route('/restaurant/<int:restaurant_id>/create_booking', methods=['GET', 'POST'])
@login_required
def create_booking(restaurant_id):
    if request.method == 'POST':
        booking_time_str = request.form.get('booking_time')

        # Convert the string date/time to a Python datetime object.
        booking_time = datetime.strptime(booking_time_str, '%Y-%m-%dT%H:%M')
        current_time = datetime.now()
        if booking_time < current_time or booking_time > current_time + timedelta(days=365):
            flash('Invalid booking time. Please enter a valid date.')
            return redirect(url_for('main.create_booking', restaurant_id=restaurant_id))

        # Create and save the booking
        booking = Booking(restaurant_id=restaurant_id, user_id=current_user.u_id, booking_time=booking_time)
        db.session.add(booking)
        db.session.commit()

        flash('Booking created successfully')
        return redirect(url_for('main.showRestaurants'))

    return render_template('createBooking.html', restaurant_id=restaurant_id)