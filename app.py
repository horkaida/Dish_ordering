from flask import Flask, request, session, render_template
from database import SQLiteDB
app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8zfdvdhbfvjdvdf]/'


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
    if session.get('ID'):
        return render_template('base.html', user=session)

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
            user = db.select_from_db("Users", ['*'], {'Email':data['Email']}, one=True)
            if user['Password']==data['Password']:
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
            orders =db.select_from_db('Orders', ['*'], {'User':session['ID']})
            return str(orders)
    return app.redirect("/user/login", code=302)

@app.route('/user/orders/<id>', methods=['GET'])
def get_order_from_history(id):
    if session.get('ID'):
        with SQLiteDB('dish.db') as db:
            orders =db.select_from_db('Orders', ['*'], {'User':session['ID']})
            order = None
            for item in orders:
                if item["User"] == session["ID"] and item["ID"] == int(id):
                        order = item
                else:
                    return 'not found'
            return str(order)
    return app.redirect("/user/login", code=302)

@app.route('/user/address', methods=['GET', 'POST'])
def get_address():
    if session.get('ID'):
        with SQLiteDB('dish.db') as db:
            addresses =db.select_from_db('Addresses', ['*'], {'User':session['ID']})
            return str(addresses)
    return app.redirect("/user/login", code=302)



@app.route('/user/address/<id>', methods=['GET', 'PUT',  'POST'])
def get_user_address_by_id(id):
    if session.get('ID'):
        with SQLiteDB('dish.db') as db:
            addresses =db.select_from_db('Orders', ['*'], {'User':session['ID']})
            address = None
            for item in addresses:
                if item["User"] == session["ID"] and item["ID"] == int(id):
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
def get_all_dishes():
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                dishes = db.select_from_db('Dishes', ['*'])
                return str(dishes)
    else:
        return app.redirect('/')


@app.route('/admin/dishes/<dish_id>', methods=['GET', 'PUT', 'DELETE'])
def get_dish(dish_id):
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                dish = db.select_from_db('Dishes', ['*'], {'id':dish_id}, one=True)
                return str(dish)
    else:
        return app.redirect('/')


@app.route('/admin/orders', methods=['GET'])
def get_all_orders():
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                orders = db.select_from_db('Orders', ['*'])
                return str(orders)
    else:
        return app.redirect('/')

@app.route('/admin/orders/<order_id>', methods=['GET', 'PUT'])
def get_order(order_id):
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                order = db.select_from_db('Orders', ['*'], {'id':order_id}, one=True)
                return str(order)
    else:
        return app.redirect('/')

@app.route('/admin/categories', methods=['GET', 'POST'])
def get_all_categories():
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                categories = db.select_from_db('Categories', ['*'])
                return str(categories)
    else:
        return app.redirect('/')

@app.route('/admin/categories/<category_slug>', methods=['GET', 'PUT', 'DELETE'])
def admin_get_category(category_slug):
    if session.get('ID') and session['Type'] == int(1):
        with SQLiteDB('dish.db') as db:
            if request.method == 'GET':
                category= db.select_from_db('Categories', ['*'], {'slug':category_slug}, one=True)
                return str(category)
    else:
        return app.redirect('/')



@app.route('/admin/search', methods=['GET'])
def search():
    return '.'


if __name__ == '__main__':
    app.run()

