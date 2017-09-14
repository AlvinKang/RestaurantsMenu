from flask import Flask
app = Flask(__name__)

# Show all restaurants
# /restaurants
# /
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
	return "This page will show all my restaurants"

# Create a new restaurant
# /restaurant/new
@app.route('/restaurant/new/')
def newRestaurant():
	return "This page will be for making a new restaurant"

# Edit a restaurant
# /restaurant/<int:restaurant_id>/edit
@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	return "This page will be for editing restaurant {}".format(restaurant_id)

# Delete a restaurant
# /restaurant/<int:restaurant_id>/delete
@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
	return "This page will be for deleting restaurant {}".format(restaurant_id)

#########################################

# Show a restaurant menu
# /restaurant/<int:restaurant_id>/menu
# /restaurant/<int:restaurant_id>
@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
	return "This page is the menu for restaurant {}".format(restaurant_id)

# Create a new menu item
# /restaurant/<int:restaurant_id>/menu/new
@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
	return "This page is for making a new menu item for restaurant {}".format(restaurant_id)

# Edit a menu item
# /restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	return "This page is for editing menu item {}".format(menu_id)

# Delete a menu item
# /restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	return "This page is for editing menu item {}".format(menu_id)

if __name__ == '__main__':
	app.debug == True
	app.run(host = '0.0.0.0', port = 5000)