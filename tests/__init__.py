import random

REGISTER_USER = {
    "first_name": "Manzede",
    "last_name": "Benard",
    "email": "manzede@gmail.com",
    "phone": "256773969641",
    "password": "manzede",
    "confirm_password": "manzede"
}

REGISTER_USER_RANDOM_EMAIL = {
    "first_name": "Manzede",
    "last_name": "Benard",
    "email":  random.choice("mkahhewu7382h2yw2627hjhgg") +"nzede@gmail.com",
    "phone": "256773969641",
    "password": "manzede",
    "confirm_password": "manzede"
}

USER_LOGIN = {
    "email": "manzede@gmail.com",
    "password": "manzede"
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