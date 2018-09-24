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

## How to use the API endpoints

|  Task         | URL | METHOD      | PARAMETERS |
| --- | --- | --- | --- |
|  Post an  order   |  api/v1/orders     |   POST         |  menu_id, client_id, location, quantity |
|  Get all orders    |  api/v1/orders     |  GET           |    N/A                |
|  Get a specific order  |  api/v1/orders/order_id |  GET |  N/A |
|  Update status of specifc order | api/v1/orders/order_id | PUT | status |
