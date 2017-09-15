from flask import Flask, render_template, request, redirect, url_for
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

# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

# Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

## course: Appetizer, Entree, Dessert, Beverage

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
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	return render_template('editMenuItem.html', restaurant=restaurant, item=item)

# Delete a menu item
# /restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	return render_template('deleteMenuItem.html', restaurant=restaurant, item=item)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
