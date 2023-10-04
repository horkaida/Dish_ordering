from flask import Flask, request, session, render_template
import database
import models
import uuid

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8zfdvdhbfvjdvdf]/'
print('hello dicker')


@app.route('/')
def main_page():
    return render_template('main.html', user=session)


@app.route('/cart', methods=['GET', 'POST'])
def get_cart():
    if session.get('id'):
        if request.method == 'GET':
            order = database.db_session.query(models.Order).where((models.Order.user == session['id']) &
                                                                  (models.Order.status == 0)).one_or_none()
            if order:
                dishes = database.db_session.query(models.Ordered_dish).filter(
                    models.Ordered_dish.order_id == order.id).join(models.Dish,
                                                                   models.Dish.id == models.Ordered_dish.dish).join(
                    models.Category, models.Category.id == models.Dish.category).all()
                order_info = {'price': 0, 'ccal': 0, 'protein': 0, 'fat': 0, 'carbs': 0, 'order_id': order.id}
                for dish in dishes:
                    order_info['price'] += dish.dish_info.price * dish.quantity
                    order_info['ccal'] += dish.dish_info.ccal * dish.quantity
                    order_info['protein'] += dish.dish_info.protein * dish.quantity
                    order_info['fat'] += dish.dish_info.fat * dish.quantity
                    order_info['carbs'] += dish.dish_info.carbs * dish.quantity
            else:
                order_info = {'price': 0, 'ccal': 0, 'protein': 0, 'fat': 0, '': 0}
                dishes = []
            return render_template('cart.html', dishes=dishes, user=session, order_info=order_info)
    if request.method == 'POST':
        data = request.form.to_dict()
        ordered_dish = database.db_session.query(models.Ordered_dish).where(models.Ordered_dish.id == data['id']).one()
        ordered_dish.quantity = data['quantity']
        database.db_session.commit()
        return app.redirect('/cart')
    return '.'


@app.route('/cart/remove/<ordered_dish_id>', methods=['POST'])
def remove_from_cart(ordered_dish_id):
    if session.get('id'):
        ordered_dish = database.db_session.query(models.Ordered_dish).where(
            models.Ordered_dish.id == ordered_dish_id).one()
        database.db_session.delete(ordered_dish)
        database.db_session.commit()
        return app.redirect('/cart')


@app.route('/cart/order', methods=['POST'])
def create_order():
    if session.get('id'):
        data = request.form.to_dict()
        order = database.db_session.query(models.Order).where(models.Order.id == data['id']).one()
        order.price = data['price']
        order.ccal = data['ccal']
        order.protein = data['protein']
        order.fat = data['fat']
        order.carbs = data['carbs']
        order.status = 1
        database.db_session.commit()
        return render_template('thankYouPage.html')


@app.route('/cart/add', methods=['POST'])
def cart_add():
    if session.get('id'):
        data = request.form.to_dict()  # dish_id
        order = database.db_session.query(models.Order).where(
            (models.Order.user == session['id']) & (models.Order.status == 0)).one_or_none()
        if order:
            ordered_dish = models.Ordered_dish(dish=data['dish_id'],
                                               quantity=data['quantity'],
                                               order_id=order.id)
            database.db_session.add(ordered_dish)
            database.db_session.commit()
        else:
            address = database.db_session.query(models.Address).where(models.Address.user == session['id']).first()
            new_order = models.Order(user=session['id'],
                                     address=address.id,
                                     price=data['price'],
                                     protein=data['protein'],
                                     fat=data['fat'],
                                     carbs=data['carbs'],
                                     ccal=data['ccal'],
                                     status=0,
                                     created_at=1)
            database.db_session.add(new_order)
            database.db_session.commit()

            order = database.db_session.query(models.Order).where(
                (models.Order.user == session['id']) & (models.Order.status == 0)).one()
            ordered_dish = models.Ordered_dish(dish=data['dish_id'],
                                               quantity=data['quantity'],
                                               order_id=order.id)
            database.db_session.add(ordered_dish)
            database.db_session.commit()
    return app.redirect('/menu')


@app.route('/user', methods=['GET', 'POST', 'DELETE  '])
def user():
    if session.get('id'):
        return render_template('user.html', user=session)

    return app.redirect("user/login", code=302)


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        data = request.form.to_dict()
        user = models.User(email=data['email'],
                           phone=data['phone'],
                           password=data['password'],
                           first_name=data['first_name'],
                           second_name=data['second_name'])
        database.db_session.add(user)
        database.db_session.commit()
        created_user = database.db_session.query(models.User).where(models.User.email == user.email).one()
        verification = models.Email_Verification(user_id=created_user.id,
                                                 verification_code=str(uuid.uuid4()))
        database.db_session.add(verification)
        database.db_session.commit()
        return app.redirect(f'/user/register/verification/{verification.verification_code}', code=302)
    return render_template('registration.html')


@app.route('/user/register/verification/<verification_code>', methods=['GET', 'POST'])
def email_verification(verification_code):
    if request.method == 'GET':
        return render_template('verification.html')
    if request.method == 'POST':
        code = database.db_session.query(models.Email_Verification).where(models.Email_Verification.verification_code == verification_code).one_or_none()
        if code:
            user = database.db_session.query(models.User).where(models.User.id == code.user_id).one()
            user.verified = True
            database.db_session.commit()
            return app.redirect('/user/login', code=302)
        else:
            return render_template('verification.html', error='Incorrect code')


@app.route('/user/login', methods=['POST', 'GET'])
def user_login():
    if session.get('id'):
        return app.redirect("/user", code=302)

    if request.method == 'POST':
        data = request.form.to_dict()
        user = database.db_session.query(models.User).where(models.User.email == data['email']).one()
        if user.password == data['password']:
            session['id'] = user.id
            session['first_name'] = user.first_name
            session['second_name'] = user.second_name
            session['type'] = user.type
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
        orders = database.db_session.query(models.Order).where(models.Order.user == session['id'])
        return render_template('orders.html', orders=orders, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/user/orders/<id>', methods=['GET'])
def get_order_from_history(id):
    if session.get('id'):
        order = database.db_session.query(models.Order).where((models.User.id == session['id'])
                                                              & (models.Order.id == id)).one_or_none()
        return render_template('order.html', order=order, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/user/address', methods=['GET', 'POST'])
def get_address():
    if session.get('id'):
        addresses = database.db_session.query(models.Address).where(models.Address.user == session['id']).all()
        return render_template('addresses.html', addresses=addresses, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/user/address/<id>', methods=['GET', 'PUT', 'POST'])
def get_user_address_by_id(id):
    if session.get('id'):
        address = database.db_session.query(models.Address).where((models.Address.user == session['id'])
                                                                  & (models.Address.id == id)).one_or_none()
        if request.method == 'POST':
            data = request.form.to_dict()
            address.city = data['city']
            address.street = data['street']
            address.building = data['building']
            address.entrance = data['entrance']
            address.floor = data['floor']
            address.apt = data['apt']
            database.db_session.commit()
        return render_template('address.html', address=address, user=session)
    return app.redirect("/user/login", code=302)


@app.route('/menu', methods=['GET'])
def get_menu():
    dishes = database.db_session.query(models.Dish).join(models.Category,
                                                         models.Category.id == models.Dish.category).all()
    return render_template("menu.html", dishes=dishes, user=session)


@app.route('/menu/<category_name>', methods=['GET'])
def get_category(category_name):
    category = database.db_session.query(models.Category).where(models.Category.slug == category_name).one()
    dishes = database.db_session.query(models.Dish).join(models.Category,
                                                         models.Category.id == models.Dish.category).filter(
        models.Dish.category == category.id).all()
    return render_template('menu.html', dishes=dishes, user=session)


@app.route('/menu/<category_name>/<dish_id>', methods=['GET'])
def get_dish_from_category(category_name, dish_id):
    dish = database.db_session.query(models.Dish).where(models.Dish.id == dish_id).join(models.Category,
                                                                                        models.Category.id == models.Dish.category).one()
    return render_template('dish.html', dish=dish, user=session)


@app.route('/menu/<category_name>/<dish_id>/review', methods=['POST'])
def dish_review(category_name, dish_id):
    data = request.form.to_dict()
    dish_rate = models.Dish_rate(dish_id=dish_id, rate=data['rate'])
    database.db_session.add(dish_rate)
    database.db_session.commit()
    return app.redirect(f'/menu/{category_name}/{dish_id}', code=302)


@app.route('/menu/search', methods=['POST'])
def menu_search():
    return '.'


# Endpoints for Admin
@app.route('/admin/', methods=['GET'])
def get_admin_page():
    return render_template('admin/admin.html', user=session)


@app.route('/admin/dishes', methods=['GET'])
def get_all_dishes():
    if session.get('id') and session['type'] == int(1):
        dishes = database.db_session.query(models.Dish).join(models.Category,
                                                             models.Dish.category == models.Category.id).all()
        return render_template('admin/dishes.html', dishes=dishes, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/dishes/create', methods=['GET', 'POST'])
def admin_dish_create():
    if session.get('id') and session['type'] == int(1):
        if request.method == 'GET':
            dish = {'dish_name': '', 'price': '', 'description': '', 'available': '', 'category': 1, 'Photo': '',
                    'ccal': '', 'protein': '', 'fat': '', 'carbs': '', 'average_rate': ''}
            categories = database.db_session.query(models.Category).all()
            return render_template("admin/dish.html", dish=dish, categories=categories, user=session)
        if request.method == 'POST':
            data = request.form.to_dict()
            dish = models.Dish(dish_name=data['dish_name'],
                               price=data['price'],
                               description=data['description'],
                               available=data['available'],
                               category=data['category'],
                               photo=data['photo'],
                               ccal=data['ccal'],
                               protein=data['protein'],
                               fat=data['fat'],
                               carbs=data['carbs']
                               )
            database.db_session.add(dish)
            database.db_session.commit()
            return app.redirect('/admin/dishes')
    else:
        return app.redirect('/')


@app.route('/admin/dishes/<dish_id>', methods=['GET', 'POST'])
def get_dish_admin(dish_id):
    if session.get('id') and session['type'] == int(1):
        dish = database.db_session.query(models.Dish).where(models.Dish.id == dish_id).one()
        if request.method == 'GET':
            categories = database.db_session.query(models.Category).all()
            return render_template("admin/dish.html", dish=dish, categories=categories, user=session)
        if request.method == 'POST':
            data = request.form.to_dict()
            dish.dish_name = data['dish_name']
            dish.category = data['category']
            dish.fat = data['fat']
            dish.ccal = data['ccal']
            dish.carbs = data['carbs']
            dish.protein = data['protein']
            dish.price = data['price']
            dish.description = data['description']
            dish.available = data['available']
            dish.photo = data['photo']
            database.db_session.commit()
            return app.redirect('/admin/dishes')
    else:
        return app.redirect('/')


@app.route('/admin/dishes/<dish_id>/remove', methods=['POST'])
def admin_dish_delete(dish_id):
    if session.get('id') and session['type'] == int(1):
        if request.method == 'POST':
            database.db_session.query(models.Dish).where(models.Dish.id == dish_id).delete()
            database.db_session.commit()
            return app.redirect('/admin/dishes')
    else:
        return app.redirect('/', code=302)


@app.route('/admin/orders', methods=['GET'])
def get_all_orders():
    if session.get('id') and session['type'] == int(1):
        orders = database.db_session.query(models.Order).all()
        return render_template('admin/orders.html', orders=orders, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/orders/<id>', methods=['GET', 'PUT'])
def get_admin_order(id):
    if session.get('id') and session['type'] == int(1):
        order = database.db_session.query(models.Order).where(models.Order.id == id).one_or_none()
        return render_template('admin/order.html', order=order, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/categories', methods=['GET'])
def get_all_categories():
    if session.get('id') and session['type'] == int(1):
        categories = database.db_session.query(models.Category).all()
        return render_template('admin/categories.html', categories=categories, user=session)
    else:
        return app.redirect('/')


@app.route('/admin/categories/<category_slug>', methods=['GET', 'POST'])
def admin_get_category(category_slug):
    if session.get('id') and session['type'] == int(1):
        category = database.db_session.query(models.Category).where(models.Category.slug == category_slug).one_or_none()
        if request.method == 'GET':
            return render_template('admin/category.html', category=category, user=session)
        if request.method == 'POST':
            data = request.form.to_dict()
            category.name = data['name']
            category.slug = data['slug']
            database.db_session.commit()
            return app.redirect('/admin/categories')
    else:
        return app.redirect('/')



@app.route('/admin/search', methods=['GET'])
def search():
    return '.'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
