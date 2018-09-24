[![Build Status](https://travis-ci.com/jeanjoe/fast-food-fast.svg?branch=api%2Fv1)](https://travis-ci.com/jeanjoe/fast-food-fast)
[![Coverage Status](https://coveralls.io/repos/github/jeanjoe/fast-food-fast/badge.svg?branch=api%2Fv1)](https://coveralls.io/github/jeanjoe/fast-food-fast?branch=api%2Fv1)
[![Maintainability](https://api.codeclimate.com/v1/badges/128fba01502d5f70e484/maintainability)](https://codeclimate.com/github/jeanjoe/fast-food-fast/maintainability)

# Fast-Food-Fast - Restaurant.

Fast-Food-Fast is the fastest food delivery service app for restaurants.

##### Demo

The Demo is hosted on [gh-pages](https://jeanjoe.github.io/fast-food-fast/UI/index.html)

##### Heroku Link

https://manzede-fast-food-fast.herokuapp.com/api/v1/orders

##### How to run the app

To run the application, you need to have Python 3 and above installed on your machine and follow these procedures:

- Clone the code
- cd to the directory
- Create a virtualenv for the app depending on the OS you are using
- activate your virtualenv
- run `pip install -r requirements.txt`
- run `python app.py`

##### Get list of all Orders

Route to `api/v1/orders`

Method = `GET`

##### Post an Order

Route  `api/v1/orders`

Method `POST`

Requirements `client_id, menu_id, location, quantity`

##### Get a specific order

Route  `api/v1/orders/order_id`

Method `GET`

Requirements `N/A`

##### Update a specific order status

Route  `api/v1/orders/order_id`

Method `PUT`

Requirements `status`
