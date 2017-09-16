from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Instantiate Flask app
app = Flask(__name__)

# Boot up and connect to database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#########################################

# Show all restaurants
# /restaurant
# /
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
	restaurants = session.query(Restaurant)
	return render_template('restaurants.html', restaurants=restaurants)

# Create a new restaurant
# /restaurant/new
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['name'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')

# Edit a restaurant
# /restaurant/<int:restaurant_id>/edit
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant=editedRestaurant)

# Delete a restaurant
# /restaurant/<int:restaurant_id>/delete
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(deletedRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant=deletedRestaurant)

# JSON endpoint for restaurants
@app.route('/restaurant/JSON/')
def restaurantsJSON():
	restaurants = session.query(Restaurant)
	return jsonify(Restaurants=[r.serialize for r in restaurants])

#########################################

# Show a restaurant menu
# /restaurant/<int:restaurant_id>/menu
# /restaurant/<int:restaurant_id>
@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

	# Organize menu items into different courses
	appetizers = []
	entrees = []
	desserts = []
	beverages = []
	for item in items:
		if item.course == 'Appetizer':
			appetizers.append(item)
		elif item.course == 'Entree':
			entrees.append(item)
		elif item.course == 'Dessert':
			desserts.append(item)
		else:
			beverages.append(item)

	return render_template('menu.html', items=items, restaurant=restaurant, appetizers=appetizers, entrees=entrees, desserts=desserts, beverages=beverages)

# Create a new menu item
# /restaurant/<int:restaurant_id>/menu/new
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['menuName'], description=request.form['menuDescription'], price=request.form['menuPrice'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant=restaurant)

# Edit a menu item
# /restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		editedItem.name = request.form['menuName']
		editedItem.description = request.form['menuDescription']
		editedItem.price = request.form['menuPrice']
		editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		return redirect('showMenu', restaurant_id=restaurant_id)
	else:
		return render_template('editMenuItem.html', restaurant=restaurant, item=editedItem)

# Delete a menu item
# /restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		return redirect('showMenu', restaurant_id=restaurant_id)
	else:
		return render_template('deleteMenuItem.html', restaurant=restaurant, item=deletedItem)

# JSON endpoint for restaurant menu
@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
@app.route('/restaurant/<int:restaurant_id>/JSON/')
def restaurantMenuJSON(restaurant_id):
	menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in menuItems])

# JSON endpoint for restaurant menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
	return jsonify(MenuItem=menuItem.serialize)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
