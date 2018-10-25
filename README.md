[![Build Status](https://travis-ci.com/jeanjoe/fast-food-fast.svg?branch=ft-challenge-four)](https://travis-ci.com/jeanjoe/fast-food-fast)
[![Coverage Status](https://coveralls.io/repos/github/jeanjoe/fast-food-fast/badge.svg?branch=ft-challenge-three)](https://coveralls.io/github/jeanjoe/fast-food-fast?branch=ft-challenge-four)
[![Maintainability](https://api.codeclimate.com/v1/badges/128fba01502d5f70e484/maintainability)](https://codeclimate.com/github/jeanjoe/fast-food-fast/maintainability)

### Fast-Food-Fast - Restaurant.

Fast-Food-Fast is the fastest food delivery service app for restaurants.

### Demo UI

The Demo is hosted on [gh-pages](https://jeanjoe.github.io/fast-food-fast/UI/index.html)

### Heroku Link to Datastructure API

https://manzede-fast-food-fast.herokuapp.com/api/v1/orders

### Link to Database API Documentation
https://manzede-fast-food-fast-3.herokuapp.com/apidocs/

### Link to Database API
https://manzede-fast-food-fast-3.herokuapp.com/api/v1/users/signup/

### Link to INTERGRATED USER INRERFACE WITH API
https://manzede-fast-food-fast-3.herokuapp.com/

### Prerequisites
-  Install `Python v3+`
- Install `PosgreSQL9.2`
- Any text editor preferably `Visual studio code`

 ### Built With / Tools Used
 - [Python Flask](http://flask.pocoo.org/) - The Python framework
 - [Github](https://github.com) - For version control
 - [Code climate](https://codeclimate.com) - For code maintainability and quality
 - [Coveralls](http://coveralls.io/) - For test coverage
 - [Travis](https://travis-ci.com/) - For running tests online
 - [Heroku](https://data.heroku.com/) - For Deploying the applicatio
 - [Vanilla Js](http://vanilla-js.com/) - Native JavaScript
 - [Real Favicon Generator](https://realfavicongenerator.net/) - For generating Favicon icons

### How to run the app

To run the application, you need to have Python 3 and above installed on your machine and follow these procedures:

- Clone the code `git clone https://github.com/jeanjoe/fast-food-fast.git`
- cd to the `fast-food-fast` directory
- Create a virtualenv for the app depending on the OS you are using
- activate your virtualenv
- run `pip install -r requirements.txt`
- run `python run.py`

### User / Customer Endpoints
|  Task         | URL | METHOD      | PARAMETERS | AUTH REQUIRED
| --- | --- | --- | --- | --- |
|  Register User   |  api/v1/users/register  |   POST  |  first_name, last_name, email, password (> 5 characters) | NO |
|  User Login   |  api/v1/users/login     |  POST           |    email, password  | NO |
|  Add New Order |  api/v1/users/orders |  POST | location, Quantity | YES |
|  Get order History | api/v1/users/orders | PUT | --------- | YES |
|  Get specific order | api/v1/users/orders/<int:order_id> | GET | ------- | YES |


### Admin Endpoints
|  Task         | URL | METHOD      | PARAMETERS | AUTH REQUIRED
| --- | --- | --- | --- | --- |
|  Register Admin   |  api/v1/admins/register  |   POST  |  first_name, last_name, email, password (> 5 characters) | NO |
|  Admin Login   |  api/v1/admins/login     |  POST           |    email, password  | NO |
|  Add New Menu |  api/v1/admins/menus |  POST | title, description, price | YES |
|  Get all Menus | api/v1/admins/menus/<int:order_id> | PUT | status | YES |
|  Update Order Status | api/v1/admins/orders/<int:order_id>/update | PUT | status ('COMPLETED', 'ACCEPTED', 'PROTECTED') | YES |
|  Get all orders | api/v1/admins/orders | GET | -------- | YES |
|  Get specific order | /api/v1/admins/orders/<int:order_id> | GET | -------- | YES |


### USER INTERFACE PAGES
| Tasks| URL|
|------|----------|
|Admin Login|https://manzede-fast-food-fast-3.herokuapp.com/admin/login|
|Admin register| https://manzede-fast-food-fast-3.herokuapp.com/admin/register|
|Admin View Order| https://manzede-fast-food-fast-3.herokuapp.com/admin/orders |
|Admin View order History | https://manzede-fast-food-fast-3.herokuapp.com/admin/orders/history|
|Admin View Menu Items| https://manzede-fast-food-fast-3.herokuapp.com/admin/menus|
|Admin Post Menu Item| https://manzede-fast-food-fast-3.herokuapp.com/admin/menus/create|
|USER PAGE|
|----------|-------------------|
|User Login| https://manzede-fast-food-fast-3.herokuapp.com/user/login|
|User Register| https://manzede-fast-food-fast-3.herokuapp.com/user/register|
|User View Menu Items| https://manzede-fast-food-fast-3.herokuapp.com/|
|User View Order History| https://manzede-fast-food-fast-3.herokuapp.com/user/orders/history|


### How to Run the Tests

To run the tests

1. Run using `pytest` open the terminal and enter `pytest`
2. To run with `coverage` type `pytest -v --cov app --cov-report term-missing`

### Deployment:

- Create an account with [Heroku](https://data.heroku.com/)
- Create a New project
- install Heroku CLI or integrate your Github account and deploy your branch
- On Heroku, go to overview and create a new postgreSQL database and update the congig details with the database 
### Contributing
@jeanjoe

### Version
 
 v1.0
 
 ### Acknowledgments
 
 - Andela Kampala
