from flask import Flask, request, session, render_template
from database import SQLiteDB

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8zfdvdhbfvjdvdf]/'


@app.route('/')
def main_page():
    return render_template('main.html', user=session)


@app.route('/cart', methods=['GET', 'DELETE'])
def get_cart():
    if session.get('ID'):
        if request.method == 'GET':
            with SQLiteDB('dish.db') as db:
                orders = db.select_from_db('Orders', ['*'], {'User': session['ID']}) #TODO Implement with AND using ORM
                order = next((x for x in orders if x['Status'] == 0), None)
                if order:
                    dishes = db.query_db(
                        f"Select * from Orders join Ordered_dishes on Orders.ID = Ordered_dishes.Order_id join Dishes on Dishes.ID=Ordered_dishes.Dish JOIN Categories on Categories.id=Dishes.Category where Ordered_dishes.Order_id == {order['ID']} AND Orders.Status==0")
                else:
                    dishes=[]
                order_info={'price':0, 'ccal':0, 'protein':0, 'fat':0, 'carb':0, 'order_id':order['ID']}
                for dish in dishes:
                    order_info['price'] += dish['Price'] * dish['Quantity']
                    order_info['ccal'] += dish['Ccal'] * dish['Quantity']
                    order_info['protein'] += dish['Protein'] * dish['Quantity']
                    order_info['fat'] += dish['Fat'] * dish['Quantity']
                    order_info['carb'] += dish['Carbs'] * dish['Quantity']
                print(dishes)
                return render_template('cart.html', dishes=dishes, user=session, order_info=order_info)
        if request.method=='POST':
            with SQLiteDB('dish.db') as db:
                data = request.form.to_dict()
                order = db.select_from_db('Orders', ['ID'], {'User': session['ID']}, one=True)
                dish = db.query_db(f"Select * from Orders join Ordered_dishes on Orders.ID = Ordered_dishes.Order_id join Dishes on Dishes.ID=Ordered_dishes.Dish JOIN Categories on Categories.id=Dishes.Category where Ordered_dishes.Order_id == {order['ID']} AND Orders.Status==0")
            db.delete_from_db('Ordered_dishes', {})

    return '.'


@app.route('/cart/order', methods=['POST'])
def create_order():
    with SQLiteDB('dish.db') as db:
        if session.get('ID'):
            data = request.form.to_dict()
            data['Status'] = 1
            order_id = data['ID']
            del data['ID']
            db.update_db('Orders', data, {'ID':order_id})

    return render_template('thankYouPage.html')


@app.route('/cart/add', methods=['POST'])
def cart_add():
    with SQLiteDB('dish.db') as db:
        if session.get('ID'):
            data = request.form.to_dict()  # dish_id
            orders = db.select_from_db('Orders', ['*'], {'User': session['ID']})
            order = next((x for x in orders if x['Status'] == 0), None)
            if order:
                print('WE ARE HERE')
                db.insert_into_db('Ordered_dishes',
                                  {'Dish': data['dish_id'], 'Quantity': data['quantity'], 'Order_id': order['ID']})
            else:
                address = db.select_from_db('Addresses', ['ID'], {'User': session['ID']}, one=True)
                db.insert_into_db('Orders', {'User': session['ID'], 'Address': address['ID'], 'Price': data['price'],
                                             'Protein': data['protein'], 'Fat': data['fat'], 'Carb': data['carbs'], 'Ccal': data['ccal'], 'Created_at':1})
                orders = db.select_from_db('Orders', ['*'], {'User': session['ID']})
                order = next(x for x in orders if x['Status'] == 0)
                db.insert_into_db('Ordered_dishes',
                                  {'Dish': data['dish_id'], 'Quantity': data['quantity'], 'Order_id': order['ID']})

            return app.redirect('/menu')


@app.route('/user', methods=['GET', 'POST', 'DELETE  '])
def user():
    if session.get('ID'):
        return render_template('user.html', user=session)

    return app.redirect("user/login", code=302)


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        with SQLiteDB('dish.db') as db:
            data = request.form.to_dict()
            db.insert_into_db('Users', data)

    return render_template('registration.html')


@app.route('/user/login', methods=['POST', 'GET'])
def user_login():
    if session.get('ID'):
        return app.redirect("/user", code=302)

    if request.method == 'POST':
        with SQLiteDB('dish.db') as db:
            data = request.form.to_dict()
            user = db.select_from_db("Users", ['*'], {'Email': data['Email']}, one=True)
            if user['Password'] == data['Password']:
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
    if session.get('ID'):
        with SQLiteDB('dish.db') as db:
            orders = db.select_from_db('Orders', ['*'], {'User': session['ID']})
            return render_template('orders.html', orders=orders, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/user/orders/<id>', methods=['GET'])
def get_order_from_history(id):
    if session.get('ID'):
        with SQLiteDB('dish.db') as db:
            orders = db.select_from_db('Orders', ['*'], {'User': session['ID']})
            order = None
            for item in orders:
                if item["ID"] == int(id):
                    order = item
            return render_template('order.html', order=order, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/user/address', methods=['GET', 'POST'])
def get_address():
    if session.get('ID'):
        with SQLiteDB('dish.db') as db:
            addresses = db.select_from_db('Addresses', ['*'], {'User': session['ID']})
            return render_template('addresses.html', addresses=addresses, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/user/address/<id>', methods=['GET', 'PUT', 'POST'])
def get_user_address_by_id(id):
    if session.get('ID'):
        with SQLiteDB('dish.db') as db:
            addresses = db.select_from_db('Addresses', ['*'], {'User': session['ID']})
            address = None
            for item in addresses:
                if item["ID"] == int(id):
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
            dish['category_info'] = next(x for x in categories if x['id'] == dish['Category'])
        return render_template("menu.html", dishes=dishes, user=session)


@app.route('/menu/<category_name>', methods=['GET'])
def get_category(category_name):
    with SQLiteDB('dish.db') as db:
        category = db.select_from_db('Categories', ["*"], {'slug': category_name}, one=True)
        dishes = db.select_from_db('Dishes', ['*'], {'Category': category['id']})
        for dish in dishes:
            dish['category_info'] = category
        return render_template('menu.html', dishes=dishes, user=session)


@app.route('/menu/<category_name>/<dish_id>', methods=['GET'])
def get_dish_from_category(category_name, dish_id):
    with SQLiteDB('dish.db') as db:
        dish = db.select_from_db('Dishes', ['*'], {'id': dish_id}, one=True)
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
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                dishes = db.select_from_db('Dishes', ['*'])
                categories = db.select_from_db('Categories', ['*'])
                for dish in dishes:
                    dish['category_info'] = next(x for x in categories if x['id'] == dish['Category'])
                return render_template('admin/dishes.html', dishes=dishes, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/dishes/<dish_id>', methods=['GET', 'PUT', 'DELETE'])
def get_dish_admin(dish_id):
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                dish = db.select_from_db('Dishes', ['*'], {'id': dish_id}, one=True)
                categories = db.select_from_db('Categories', ['*'])
                return render_template("admin/dish.html", dish=dish, categories=categories, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/orders', methods=['GET'])
def get_all_orders():
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                orders = db.select_from_db('Orders', ['*'])
                return render_template('admin/orders.html', orders=orders, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/orders/<id>', methods=['GET', 'PUT'])
def get_admin_order(id):
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                order = db.select_from_db('Orders', ['*'], {'id': id}, one=True)
                return render_template('admin/order.html', order=order, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/categories', methods=['GET', 'POST'])
def get_all_categories():
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                categories = db.select_from_db('Categories', ['*'])
                return render_template('admin/categories.html', categories=categories, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/categories/<category_slug>', methods=['GET', 'PUT', 'DELETE'])
def admin_get_category(category_slug):
    if session.get('ID') and session['Type'] == int(1):
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
