from flask import Flask

app = Flask(__name__)


@app.route('/')
def main_page():
    return 'Main page'

@app.route('/cart', methods=['GET', 'PUT'])
def get_cart():
    return '.'

@app.route('/cart/order', methods=['POST'])
def create_order():
    return '.'

@app.route('/cart/add', methods=['POST'])
def cart_add():
    return '.'

@app.route('/user', methods=['GET', 'POST', 'DELETE  '])
def user():
    return '.'

@app.route('/user/register', methods=['POST'])
def user_register():
    return '.'

@app.route('/user/sign_in', methods=['POST'])
def user_sign_in():
    return '.'

@app.route('/user/sign_out', methods=['POST'])
def user_sign_out():
    return '.'

@app.route('/user/restore', methods=['POST'])
def user_reset_password():
    return '.'

@app.route('/user/orders', methods=['GET'])
def get_orders_history():
    return '.'

@app.route('/user/orders/<id>', methods=['GET'])
def get_order_from_history():
    return '.'

@app.route('/user/address', methods=['GET', 'POST'])
def get_user_address():
    return '.'

@app.route('/user/address/<id>', methods=['GET', 'PUT',  'POST'])
def get_user_address_by_id():
    return '.'

@app.route('/menu', methods=['GET'])
def get_menu():
    return '.'

@app.route('/menu/<category_name>', methods=['GET'])
def get_category():
    return '.'

@app.route('/menu/<category_name>/<dish>', methods=['GET'])
def get_dish_from_category():
    return '.'

@app.route('/menu/<category_name>/<dish>/review', methods=['POST'])
def create_dish_review_():
    return '.'

@app.route('/menu/search', methods=['POST'])
def menu_search():
    return '.'


#Endpoints for Admin
@app.route('/admin/', methods=['Get'])
def get_admin_page():
    return '.'

@app.route('/admin/dishes', methods=['Get', 'POST'])
def get_all_dishes():
    return '.'

@app.route('/admin/dishes/<dish>', methods=['Get', 'PU  T', 'DELETE'])
def get_dish():
    return '.'

@app.route('/admin/orders', methods=['Get'])
def get_all_orders():
    return '.'

@app.route('/admin/orders/<order>', methods=['Get', 'PUT'])
def get_order():
    return '.'

@app.route('/admin/categories', methods=['Get', 'POST'])
def get_all_categories():
    return '.'

@app.route('/admin/categories/<category>', methods=['Get', 'PUT', 'DELETE'])
def admin_get_category():
    return '.'

@app.route('/admin/search', methods=['Get'])
def search():
    return '.'


if __name__ == '__main__':
    app.run()

