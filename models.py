from sqlalchemy import Column, Integer, String, ForeignKey, Float
from database import Base


class User_type(Base):
    __tablename__ = 'User_types'
    id = Column(Integer, primary_key=True)
    type = Column(String(120))
    def __str__(self):
        return f'<User_type {self.id}>'
    def __repr__(self):
        return self.__str__()


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    phone = Column(Integer, unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))
    tg = Column(Integer)
    type = Column(Integer, ForeignKey('User_type.id'))
    first_name = Column(String(50))
    second_name = Column(String(50))

    def __init__(self, phone=None, email=None, password=None, tg=None, first_name=None, second_name=None):
        self.phone = phone
        self.email = email
        self.password = password
        self.tg = tg
        self.first_name = first_name
        self.second_name = second_name
    def __str__(self):
        return f'<User {self.id}>'
    def __repr__(self):
        return self.__str__()


class Address(Base):
    __tablename__ = 'Addresses'
    id = Column(Integer, primary_key=True)
    city = Column(String(120))
    street = Column(String(120))
    building = Column(String(120))
    apt = Column(Integer)
    floor = Column(Integer)
    user = Column(Integer, ForeignKey('User.id'))

    def __init__(self, city=None, street=None, building=None, apt=None, floor=None, user=None):
        self.city = city
        self.street = street
        self.building = building
        self.apt = apt
        self.floor = floor
        self.user = user
    def __str__(self):
        return f'<Address {self.id}>'
    def __repr__(self):
        return self.__str__()


class Category(Base):
    __tablename__ = 'Categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    slug = Column(String(120))

    def __init__(self, name=None, slug=None):
        self.name = name
        self.slug = slug
    def __str__(self):
        return f'<Category {self.id}>'
    def __repr__(self):
        return self.__str__()


class Dish(Base):
    __tablename__ = 'Dishes'
    id = Column(Integer, primary_key=True)
    dish_name = Column(String(120))
    price = Column(Integer)
    description = Column(String(120))
    available = Column(Integer)
    category = Column(Integer, ForeignKey('Category.id'))
    photo = Column(String(120))
    ccal = Column(Integer)
    protein = Column(Integer)
    fat = Column(Integer)
    carbs = Column(Integer)
    average_rate = Column(Integer)

    def __init__(self, dish_name=None, price=None, description=None, available=None, category=None, photo=None, ccal=None, protein=None, fat=None, carbs=None, average_rate=None, slug=None):
        self.dish_name = dish_name
        self.price = price
        self.description = description
        self.available = available
        self.category = category
        self.photo = photo
        self.ccal = ccal
        self.protein = protein
        self.fat = fat
        self.carbs = carbs
        self.average_rate = average_rate
    def __str__(self):
        return f'<Dish {self.id}>'
    def __repr__(self):
        return self.__str__()


class Ordered_dish(Base):
    __tablename__ = 'Ordered_dishes'
    id = Column(Integer, primary_key=True)
    dish = Column(Integer, ForeignKey('Dish.id'))
    order_id = Column(Integer, ForeignKey('Order.id'))
    quantity = Column(Integer)

    def __init__(self, dish=None, order_id=None, quantity=None):
        self.dish = dish
        self.order_id = order_id
        self.quantity = quantity
    def __str__(self):
        return f'<Ordered_dish {self.id}>'
    def __repr__(self):
        return self.__str__()


class Order(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('User.id'))
    address = Column(Integer, ForeignKey('Address.id'))
    price = Column(Integer)
    protein = Column(Integer)
    fat = Column(Integer)
    carbs = Column(Integer)
    ccal = Column(Integer)
    comment = Column(String(350))
    created_at = Column(Integer)
    rate = Column(Integer)
    status = Column(Integer, ForeignKey('Status.id'))

    def __init__(self, user=None, address=None, price=None, protein=None, fat=None, carbs=None, ccal=None, comment=None, created_at=None, rate=None):
        self.user = user
        self.address = address
        self.price = price
        self.protein = protein
        self.fat = fat
        self.carbs = carbs
        self.ccal = ccal
        self.comment = comment
        self.created_at = created_at
        self.rate = rate

    def __str__(self):
        return f'<Order {self.id}>'

    def __repr__(self):
        return self.__str__()


class Status(Base):
    __tablename__ = 'Statuses'
    id = Column(Integer, primary_key=True)
    status = Column(String(50))
    def __str__(self):
        return f'<Status {self.id}>'
    def __repr__(self):
        return self.__str__()

class Dish_rate(Base):
    __tablename__ = 'Dish_rates'
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('Dish.id'))
    rate = Column(Float)

    def __str__(self):
        return f'<Dish_rate {self.id}>'

    def __repr__(self):
        return self.__str__()