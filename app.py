from flask import Flask, request
import sqlite3
from urllib.parse import unquote
from database import SQLiteDB
app = Flask(__name__)


# def query_db(query, args=(), one=False):
#     con = sqlite3.connect("dish.db")
#     cur = con.cursor()
#     result = cur.execute(query, args).fetchall()
#     return (result[0] if result else None) if one else result


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
def get_address():
    return '.'

@app.route('/user/address/<id>', methods=['GET', 'PUT',  'POST'])
def get_user_address_by_id():
    return '.'

@app.route('/menu', methods=['GET', 'POST'])
def get_menu():
    with SQLiteDB('dish.db') as db:
        if request.method == 'POST':
            data = request.json
            db.insert_into_db('Dishes', data)

        dishes = db.select_from_db('Dishes', ['*'])
    return str(dishes)


@app.route('/menu/<category_name>', methods=['GET'])
def get_category(category_name):
    with SQLiteDB('dish.db') as db:
        result = db.select_from_db('Categories', ['name'], 'slug'==category_name)
        return str(result)
    # category_id = query_db("SELECT * FROM Categories WHERE slug = ?", [category_name], one=True)[1]
    # result = query_db("SELECT * FROM dishes WHERE Category =?", [category_id])
    # return unquote(str(result))


@app.route('/menu/<category_name>/<dish_id>', methods=['GET'])
# def get_dish_from_category(category_name, dish_id):
#     result = query_db("SELECT * FROM dishes WHERE id =?", [dish_id], one=True)
#     return unquote(str(result))

@app.route('/menu/<category_name>/<dish>/review', methods=['POST'])
def create_dish_review_():
    return '.'

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

