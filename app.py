from flask import Flask, request, session, render_template
from database_old import SQLiteDB

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8zfdvdhbfvjdvdf]/'


@app.route('/')
def main_page():
    return render_template('main.html', user=session)


@app.route('/cart', methods=['GET', 'POST'])
def get_cart():
    if session.get('id'):
        if request.method == 'GET':
            with SQLiteDB('dish.db') as db:
                orders = db.select_from_db('Orders', ['*'],
                                           {'user': session['id']})  # TODO Implement with AND using ORM
                order = next((x for x in orders if x['status'] == 0), None)
                if order:
                    dishes = db.query_db(
                        f"Select Ordered_dishes.id, Dishes.price, Dishes.ccal, Dishes.fat, Dishes.protein,"
                        f"Dishes.carbs, Dishes.dish_name, Ordered_dishes.quantity from Orders"
                        f" join Ordered_dishes on Orders.id = Ordered_dishes.order_id"
                        f" join Dishes on Dishes.id=Ordered_dishes.dish"
                        f" join Categories on Categories.id=Dishes.category "
                        f" where Ordered_dishes.order_id == {order['id']} AND Orders.status==0")

                    order_info = {'price': 0, 'ccal': 0, 'protein': 0, 'fat': 0, 'carbs': 0, 'order_id': order['id']}
                    for dish in dishes:
                        order_info['price'] += dish['price'] * dish['quantity']
                        order_info['ccal'] += dish['ccal'] * dish['quantity']
                        order_info['protein'] += dish['protein'] * dish['quantity']
                        order_info['fat'] += dish['fat'] * dish['quantity']
                        order_info['carbs'] += dish['carbs'] * dish['quantity']
                else:
                    order_info = {'price': 0, 'ccal': 0, 'protein': 0, 'fat': 0, '': 0}
                    dishes = []
                return render_template('cart.html', dishes=dishes, user=session, order_info=order_info)
        if request.method == 'POST':
            with SQLiteDB('dish.db') as db:
                data = request.form.to_dict()
                db.update_db('Ordered_dishes', {'quantity': data['quantity']}, {'id': data['id']})
                return app.redirect('/cart')


@app.route('/cart/remove/<ordered_dish_id>', methods=['POST'])  # TODO HTML form does not support DELETE method
def remove_from_cart(ordered_dish_id):
    if session.get('id'):
        with SQLiteDB('dish.db') as db:
            db.delete_from_db('Ordered_dishes', {'id': ordered_dish_id})
            return app.redirect('/cart')


@app.route('/cart/order', methods=['POST'])
def create_order():
    with SQLiteDB('dish.db') as db:
        if session.get('id'):
            data = request.form.to_dict()
            data['status'] = 1
            order_id = data['id']
            del data['id']
            db.update_db('Orders', data, {'id': order_id})

    return render_template('thankYouPage.html')


@app.route('/cart/add', methods=['POST'])
def cart_add():
    with SQLiteDB('dish.db') as db:
        if session.get('id'):
            data = request.form.to_dict()  # dish_id
            orders = db.select_from_db('Orders', ['*'], {'user': session['id']})
            order = next((x for x in orders if x['status'] == 0), None)
            if order:
                db.insert_into_db('Ordered_dishes',
                                  {'dish': data['dish_id'], 'quantity': data['quantity'], 'order_id': order['id']})
            else:
                address = db.select_from_db('Addresses', ['id'], {'user': session['id']}, one=True)
                db.insert_into_db('Orders', {'user': session['id'], 'address': address['id'], 'price': data['price'],
                                             'protein': data['protein'], 'fat': data['fat'], 'carbs': data['carbs'],
                                             'ccal': data['ccal'], 'Created_at': 1})
                orders = db.select_from_db('Orders', ['*'], {'user': session['id']})
                order = next(x for x in orders if x['status'] == 0)
                db.insert_into_db('Ordered_dishes',
                                  {'dish': data['dish_id'], 'quantity': data['quantity'], 'order_id': order['id']})

        return app.redirect('/menu')


@app.route('/user', methods=['GET', 'POST', 'DELETE  '])
def user():
    if session.get('id'):
        return render_template('user.html', user=session)

    return app.redirect("user/login", code=302)


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        with SQLiteDB('dish.db') as db:
            data = request.form.to_dict()
            db.insert_into_db('users', data)

    return render_template('registration.html')


@app.route('/user/login', methods=['POST', 'GET'])
def user_login():
    if session.get('id'):
        return app.redirect("/user", code=302)

    if request.method == 'POST':
        with SQLiteDB('dish.db') as db:
            data = request.form.to_dict()
            user = db.select_from_db("users", ['*'], {'email': data['email']}, one=True)
            if user['password'] == data['password']:
                for key, value in user.items():
                    session[key] = value
                return app.redirect("/user", code=302)
            else:
                return render_template('login.html', error='Incorrect credentials')

    return render_template('login.html')


@app.route('/user/logout', methods=['POST'])
def user_sign_out():
    session.clear()
    return app.redirect("/user/login", code=302)


@app.route('/user/restore', methods=['POST'])
def user_reset_password():
    return '.'


@app.route('/user/orders', methods=['GET'])
def get_orders_history():
    if session.get('id'):
        with SQLiteDB('dish.db') as db:
            orders = db.select_from_db('Orders', ['*'], {'user': session['id']})
            return render_template('orders.html', orders=orders, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/user/orders/<id>', methods=['GET'])
def get_order_from_history(id):
    if session.get('id'):
        with SQLiteDB('dish.db') as db:
            orders = db.select_from_db('Orders', ['*'], {'user': session['id']})
            order = None
            for item in orders:
                if item["id"] == int(id):
                    order = item
            return render_template('order.html', order=order, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/user/address', methods=['GET', 'POST'])
def get_address():
    if session.get('id'):
        with SQLiteDB('dish.db') as db:
            addresses = db.select_from_db('Addresses', ['*'], {'user': session['id']})
            return render_template('addresses.html', addresses=addresses, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/user/address/<id>', methods=['GET', 'PUT', 'POST'])
def get_user_address_by_id(id):
    if session.get('id'):
        with SQLiteDB('dish.db') as db:
            addresses = db.select_from_db('Addresses', ['*'], {'user': session['id']})
            address = None
            for item in addresses:
                if item["id"] == int(id):
                    address = item
            return render_template('address.html', address=address, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/menu', methods=['GET', 'POST'])
def get_menu():
    with SQLiteDB('dish.db') as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            db.insert_into_db('Dishes', data)
        dishes = db.select_from_db('Dishes', ['*'])
        categories = db.select_from_db('Categories', ['*'])
        for dish in dishes:
            dish['category_info'] = next(x for x in categories if x['id'] == dish['category'])
        return render_template("menu.html", dishes=dishes, user=session)


@app.route('/menu/<category_name>', methods=['GET'])
def get_category(category_name):
    with SQLiteDB('dish.db') as db:
        category = db.select_from_db('Categories', ["*"], {'slug': category_name}, one=True)
        dishes = db.select_from_db('Dishes', ['*'], {'category': category['id']})
        for dish in dishes:
            dish['category_info'] = category
        return render_template('menu.html', dishes=dishes, user=session)


@app.route('/menu/<category_name>/<dish_id>', methods=['GET'])
def get_dish_from_category(category_name, dish_id):
    with SQLiteDB('dish.db') as db:
        dish= db.select_from_db('Dishes', ['*'], {'id': dish_id}, one=True)
        dish['category_info'] = db.select_from_db('Categories', ["*"], {'slug': category_name}, one=True)
        return render_template('dish.html', dish=dish, user=session)


@app.route('/menu/<category_name>/<dish_id>/review', methods=['POST'])
def dish_review(category_name, dish_id):
    with SQLiteDB('dish.db') as db:
        data = request.form.to_dict()
        data['Dish_id'] = dish_id
        db.insert_into_db('Dish_rates', data)
        return app.redirect(f'/menu/{category_name}/{dish_id}', code=302)


@app.route('/menu/search', methods=['POST'])
def menu_search():
    return '.'


# Endpoints for Admin
@app.route('/admin/', methods=['GET'])
def get_admin_page():
    return render_template('admin/admin.html', user=session)


@app.route('/admin/dishes', methods=['GET', 'POST'])
def get_all_dishes():
    if session.get('id') and session['type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                dishes = db.select_from_db('Dishes', ['*'])
                categories = db.select_from_db('Categories', ['*'])
                for dish in dishes:
                    dish['category_info'] = next(x for x in categories if x['id'] == dish['category'])
                return render_template('admin/dishes.html', dishes=dishes, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/dishes/create', methods=['GET', 'POST'])
def admin_dish_create():
    if session.get('id') and session['type'] == int(1):
        if request.method == 'GET':
            with SQLiteDB('dish.db') as db:
                dish= {'dish_name':'', 'price':'', 'description':'', 'available':'', 'category':1, 'Photo':'',
                        'ccal':'', 'protein':'', 'fat':'', 'carbs':'', 'average_rate':''}
                categories = db.select_from_db('Categories', ['*'])
                return render_template("admin/dish.html", dish=dish, categories=categories, user=session)
        if request.method == 'POST':
            with SQLiteDB('dish.db') as db:
                data = request.form.to_dict()
                db.insert_into_db('Dishes', data)
                return app.redirect('/admin/dishes')
    else:
        return app.redirect('/')


@app.route('/admin/dishes/<dish_id>', methods=['GET', 'POST'])
def get_dish_admin(dish_id):
    if session.get('id') and session['type'] == int(1):
        if request.method == 'GET':
            with SQLiteDB('dish.db') as db:
                dish= db.select_from_db('Dishes', ['*'], {'id': dish_id}, one=True)
                categories = db.select_from_db('Categories', ['*'])
                return render_template("admin/dish.html", dish=dish, categories=categories, user=session)
        if request.method == 'POST':
            with SQLiteDB('dish.db') as db:
                data = request.form.to_dict()
                db.update_db('Dishes', data, {'id': data['id']})
                return app.redirect('/admin/dishes')
    else:
        return app.redirect('/')


@app.route('/admin/dishes/<dish_id>/remove', methods=['POST'])
def admin_dish_delete(dish_id):
    if session.get('id') and session['type'] == int(1):
        if request.method == 'POST':
            with SQLiteDB('dish.db') as db:
                db.delete_from_db('Dishes', {'id': dish_id})
                return app.redirect('/admin/dishes')


@app.route('/admin/orders', methods=['GET'])
def get_all_orders():
    if session.get('id') and session['type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                orders = db.select_from_db('Orders', ['*'])
                return render_template('admin/orders.html', orders=orders, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/orders/<id>', methods=['GET', 'PUT'])
def get_admin_order(id):
    if session.get('id') and session['type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                order = db.select_from_db('Orders', ['*'], {'id': id}, one=True)
                return render_template('admin/order.html', order=order, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/categories', methods=['GET', 'POST'])
def get_all_categories():
    if session.get('id') and session['type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                categories = db.select_from_db('Categories', ['*'])
                return render_template('admin/categories.html', categories=categories, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/categories/<category_slug>', methods=['GET', 'PUT', 'DELETE'])
def admin_get_category(category_slug):
    if session.get('id') and session['type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                category = db.select_from_db('Categories', ['*'], {'slug': category_slug}, one=True)
                return render_template('admin/category.html', category=category, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/search', methods=['GET'])
def search():
    return '.'


if __name__ == '__main__':
    app.run()
