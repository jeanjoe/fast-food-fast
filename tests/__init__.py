import random

REGISTER_USER = {
    "first_name": "Manzede",
    "last_name": "Benard",
    "email": "manzede@gmail.com",
    "phone": "256773969641",
    "password": "manzede"
}

REGISTER_ADMIN = {
    "first_name": "Admin",
    "last_name": "Admin",
    "email": "admin@admin.com",
    "phone": "256773969641",
    "password": "admin"
}

REGISTER_USER_RANDOM_EMAIL = {
    "first_name": "Manzede",
    "last_name": "Benard",
    "email":  random.choice("mkahhewu7382h2yw2627hjhgg") +"nzede@gmail.com",
    "phone": "256773969641",
    "password": "manzede"
}

REGISTER_EMAIL_EXISTS = {
    "first_name": "Manzede",
    "last_name": "Benard",
    "email": "manzede@gmail.com",
    "phone": "256773969641",
    "password": "manzede"
}

USER_LOGIN = {
    "email": "manzede@gmail.com",
    "password": "manzede"
}

ADMIN_LOGIN = {
    "email": "admin@admin.com",
    "password": "admin"
}

WRONG_USER_LOGIN = {
    "email": "manzede@gmail.com",
    "password": "21324546565"
}

MENU_DATA = {
    "title": "Local food",
    "description": "All food",
    "price": 20000
}