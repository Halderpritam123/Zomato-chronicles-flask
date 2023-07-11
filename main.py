from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data
users = []
menu = [
    {'dish_name': 'Pizza', 'dish_price': 10.99, 'availability': 'available'},
    {'dish_name': 'Burger', 'dish_price': 5.99, 'availability': 'available'},
    # Add more dishes here
]
orders = []

@app.route('/')
def index():
    return jsonify({"msg": "Welcome to home page 🚅"})

# Register route
@app.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = next((user for user in users if user['email'] == email), None)
    if user:
        return jsonify({'error': 'User with this email already exists'}), 409

    new_user = {'name': name, 'email': email, 'password': password}
    users.append(new_user)

    return jsonify({'message': 'Registration successful'}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = next((user for user in users if user['email'] == email and user['password'] == password), None)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    # Perform any necessary logout functionality
    return jsonify({'message': 'Logout successful'}), 200

# Menu route
@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(menu), 200

# Menu availability update route (admin only)
@app.route('/menu/<int:dish_id>/availability', methods=['PUT'])
def update_menu_availability(dish_id):
    # Implement authorization logic here to check if user is an admin
    # ...

    dish = next((dish for dish in menu if dish['id'] == dish_id), None)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404

    availability = request.json.get('availability')
    if not availability:
        return jsonify({'error': 'Missing availability field'}), 400

    dish['availability'] = availability
    return jsonify({'message': 'Menu availability updated'}), 200

# Menu dish addition route (admin only)
@app.route('/menu', methods=['POST'])
def add_dish_to_menu():
    # Implement authorization logic here to check if user is an admin
    # ...

    dish_name = request.json.get('dish_name')
    dish_price = request.json.get('dish_price')
    availability = request.json.get('availability')

    if not dish_name or not dish_price or not availability:
        return jsonify({'error': 'Missing required fields'}), 400

    new_dish = {'dish_name': dish_name, 'dish_price': dish_price, 'availability': availability}
    menu.append(new_dish)

    return jsonify({'message': 'Dish added to menu'}), 201

# Menu dish deletion route (admin only)
@app.route('/menu/<int:dish_id>', methods=['DELETE'])
def delete_dish_from_menu(dish_id):
    # Implement authorization logic here to check if user is an admin
    # ...

    dish = next((dish for dish in menu if dish['id'] == dish_id), None)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404

    menu.remove(dish)
    return jsonify({'message': 'Dish deleted from menu'}), 200

# Menu dish update route (admin only)
@app.route('/menu/<int:dish_id>', methods=['PUT'])
def update_dish_on_menu(dish_id):
    # Implement authorization logic here to check if user is an admin
    # ...

    dish = next((dish for dish in menu if dish['id'] == dish_id), None)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404

    dish_name = request.json.get('dish_name')
    dish_price = request.json.get('dish_price')

    if dish_name:
        dish['dish_name'] = dish_name
    if dish_price:
        dish['dish_price'] = dish_price

    return jsonify({'message': 'Dish updated'}), 200

# Order route
@app.route('/order', methods=['GET'])
def get_orders():
    # Implement authorization logic here if needed
    # ...

    return jsonify(orders), 200

# Order creation route
@app.route('/order', methods=['POST'])
def create_order():
    # Implement authorization logic here if needed
    # ...

    dish_name = request.json.get('dish_name')
    dish_price = request.json.get('dish_price')

    if not dish_name or not dish_price:
        return jsonify({'error': 'Missing required fields'}), 400

    new_order = {'dish_name': dish_name, 'dish_price': dish_price}
    orders.append(new_order)

    return jsonify({'message': 'Order created'}), 201

# Order deletion route
@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Implement authorization logic here if needed
    # ...

    order = next((order for order in orders if order['id'] == order_id), None)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    orders.remove(order)
    return jsonify({'message': 'Order deleted'}), 200

# Order status update route (admin only)
@app.route('/order/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    # Implement authorization logic here to check if user is an admin
    # ...

    order = next((order for order in orders if order['id'] == order_id), None)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order_status = request.json.get('order_status')
    if not order_status:
        return jsonify({'error': 'Missing order_status field'}), 400

    order['order_status'] = order_status
    return jsonify({'message': 'Order status updated'}), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
