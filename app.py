from flask import Flask, request
import sqlite3
from urllib.parse import unquote
from database import SQLiteDB
app = Flask(__name__)
current_user = None


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
    if current_user:
        return f"""
        Hello {current_user['First_name']}
        <form method="POST" action="/user/logout">
        <input value="Logout" type="submit">
        </form>
        """

    return app.redirect("user/login", code=302)


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        with SQLiteDB('dish.db') as db:
            data = request.form.to_dict()
            db.insert_into_db('Users', data)

    html_form = f"""
    <form method="POST">
    <h1>Registration form </h1>
    <input type="text" name="Email" placeholder="Enter your email address">
    <input type="text" name="Password" placeholder="Create your password">
    <input type="text" name="Phone" placeholder="Phone number">
    <input type="text" name="First_name" placeholder="First name">
    <input type="text" name="Second_name" placeholder="Second name">
    <input type="text" name="Tg" placeholder="Telegram">
    <input type="submit">
    </form>
    """
    return html_form

@app.route('/user/login', methods=['POST', 'GET'])
def user_login():
    global current_user
    html_form = f"""
    <form method="POST">
    <h1>Registration form </h1>
    <input type="text" name="Email" placeholder="Enter your email address">
    <input type="text" name="Password" placeholder="Enter your password">
    <input type="submit">
    </form>
    """

    if current_user:
        return app.redirect("/user", code=302)

    if request.method == 'POST':
        with SQLiteDB('dish.db') as db:
            data = request.form.to_dict()
            user = db.select_from_db("Users", ['*'], {'Email':data['Email']}, one=True)
            if user['Password']==data['Password']:
                current_user = user
                return app.redirect("/user", code=302)
            else:
                return f" Incorrect credentials/n{html_form}"

    return html_form
@app.route('/user/logout', methods=['POST'])
def user_sign_out():
    global current_user
    current_user = None
    return app.redirect("/user/login", code=302)

@app.route('/user/restore', methods=['POST'])
def user_reset_password():
    return '.'

@app.route('/user/orders', methods=['GET'])
def get_orders_history():
    if current_user:
        with SQLiteDB('dish.db') as db:
            orders =db.select_from_db('Orders', ['*'], {'User':current_user['ID']})
            return str(orders)
    return app.redirect("/user/login", code=302)

@app.route('/user/orders/<id>', methods=['GET'])
def get_order_from_history(id):
    if current_user:
        with SQLiteDB('dish.db') as db:
            orders =db.select_from_db('Orders', ['*'], {'User':current_user['ID']})
            order = None
            for item in orders:
                if item["User"] == current_user["ID"] and item["ID"] == int(id):
                        order = item
                else:
                    return 'not found'
            return str(order)
    return app.redirect("/user/login", code=302)

@app.route('/user/address', methods=['GET', 'POST'])
def get_address():
    if current_user:
        with SQLiteDB('dish.db') as db:
            addresses =db.select_from_db('Addresses', ['*'], {'User':current_user['ID']})
            return str(addresses)
    return app.redirect("/user/login", code=302)



@app.route('/user/address/<id>', methods=['GET', 'PUT',  'POST'])
def get_user_address_by_id(id):
    if current_user:
        with SQLiteDB('dish.db') as db:
            addresses =db.select_from_db('Orders', ['*'], {'User':current_user['ID']})
            address = None
            for item in addresses:
                if item["User"] == current_user["ID"] and item["ID"] == int(id):
                        address = item
                else:
                    return 'not found'
            return str(address)
    return app.redirect("/user/login", code=302)

@app.route('/menu', methods=['GET', 'POST'])
def get_menu():
    with SQLiteDB('dish.db') as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            db.insert_into_db('Dishes', data)

        dishes = db.select_from_db('Dishes', ['*'])

    html_form = f"""
    <form method="POST">
    <input type="text" name="Dish_name" placeholder="name">
    <input type="text" name="Price" placeholder="price">
    <input type="text" name="Description" placeholder="description">
    <input type="text" name="Available" placeholder="availability">
    <input type="text" name="Category" placeholder="category">
    <input type="text" name="Photo" placeholder="photo">
    <input type="text" name="Ccal" placeholder="ccal">
    <input type="text" name="Protein" placeholder="protein">
    <input type="text" name="Fat" placeholder="fat">
    <input type="text" name="Carbs" placeholder="carbs">
    <input type="text" name="Average_rate" placeholder="rate">
    
    <input type="submit">
    </form>
    
    <br />
    {str(dishes)}
    """
    return html_form


@app.route('/menu/<category_name>', methods=['GET'])
def get_category(category_name):
    with SQLiteDB('dish.db') as db:
        category_id = db.select_from_db('Categories', ['id'], {'slug':category_name}, one=True)
        print(category_id)
        result = db.select_from_db('Dishes', ['*'], {'Category':category_id['id']})
        return str(result)


@app.route('/menu/<category_name>/<dish_id>', methods=['GET'])
def get_dish_from_category(category_name, dish_id):
    html_form = f"""
    <form method='POST' action="/menu/{category_name}/{dish_id}/review">
    <input type="number" name="Rate" placeholder="rate">
    <input type="submit">
    </form>
    
    <br />
    """
    with SQLiteDB('dish.db') as db:
        print(dish_id)
        result = db.select_from_db('Dishes', ['*'], {'id':dish_id}, one=True)
        return str(result) + html_form


@app.route('/menu/<category_name>/<dish_id>/review', methods=['POST'])
def create_dish_review_(category_name, dish_id):

    with SQLiteDB('dish.db') as db:
        data = request.form.to_dict()
        data['Dish_id'] = dish_id
        db.insert_into_db('Dish_rates', data)
        return app.redirect(f'/menu/{category_name}/{dish_id}', code=302)

@app.route('/menu/search', methods=['POST'])
def menu_search():
    return '.'


#Endpoints for Admin
@app.route('/admin/', methods=['GET'])
def get_admin_page():
    return '.'

@app.route('/admin/dishes', methods=['GET', 'POST'])
# def get_all_dishes():
    # if request.method == 'GET':
    #     result = query_db("SELECT * FROM dishes")
    #     return unquote(str(result))
    # else:
    #     return '.'

@app.route('/admin/dishes/<dish_id>', methods=['GET', 'PUT', 'DELETE'])
# def get_dish(dish_id):
#     if request.method == 'GET':
#         result = query_db("SELECT * FROM dishes WHERE id = ?", [dish_id], one=True)
#         return unquote(str(result))
#     else:
#         return '.'

@app.route('/admin/orders', methods=['GET'])
def get_all_orders():
    return '.'

@app.route('/admin/orders/<order>', methods=['GET', 'PUT'])
def get_order():
    return '.'

@app.route('/admin/categories', methods=['GET', 'POST'])
# def get_all_categories():
#     result = query_db("SELECT * FROM categories")
#     return unquote(str(result))

@app.route('/admin/categories/<category_slug>', methods=['GET', 'PUT', 'DELETE'])
# def admin_get_category(category_slug):
    # if request.method == 'GET':
    #     result = query_db("SELECT * FROM categories WHERE slug = ?", [category_slug], one=True)
    #     return unquote(str(result))
    # else:
    #     return '.'


@app.route('/admin/search', methods=['GET'])
def search():
    return '.'


if __name__ == '__main__':
    app.run()

