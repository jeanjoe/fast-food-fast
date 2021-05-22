### UNIPAY-URA GATEWAY

UNIPAY-URA GATEWAY is a bridge between URA Payment API and UNITEERP Systems, It integrates all Public university Payments with URA

### Link to Database API Documentation

https://manzede-fast-food-fast-3.herokuapp.com/apidocs/

### Link to Database API

https://manzede-fast-food-fast-3.herokuapp.com/api/v1/users/signup/

### Prerequisites

- Install `Python v3+`
- Install `PosgreSQL9.2`
- Any text editor preferably `Visual studio code`

### Built With / Tools Used

- [Python Flask](http://flask.pocoo.org/) - The Python framework
- [Github](https://github.com) - For version control
- [Code climate](https://codeclimate.com) - For code maintainability and quality
- [Coveralls](http://coveralls.io/) - For test coverage
- [Travis](https://travis-ci.com/) - For running tests online
- [Heroku](https://data.heroku.com/) - For Deploying the applicatio

### How to run the app

To run the application, you need to have Python 3 and above installed on your machine and follow these procedures:

- Clone the code `git clone https://github.com/jeanjoe/fast-food-fast.git`
- cd to the `fast-food-fast` directory
- Create a virtualenv for the app depending on the OS you are using
- activate your virtualenv
- run `pip install -r requirements.txt`
- run `python run.py`

### User / Customer Endpoints

| Task               | URL                                | METHOD | PARAMETERS                                              | AUTH REQUIRED |
| ------------------ | ---------------------------------- | ------ | ------------------------------------------------------- | ------------- |
| Register User      | api/v1/users/register              | POST   | first_name, last_name, email, password (> 5 characters) | NO            |
| User Login         | api/v1/users/login                 | POST   | email, password                                         | NO            |
| Add New Order      | api/v1/users/orders                | POST   | location, Quantity                                      | YES           |
| Get order History  | api/v1/users/orders                | PUT    | ---------                                               | YES           |
| Get specific order | api/v1/users/orders/<int:order_id> | GET    | -------                                                 | YES           |

| API ENDPOINT                  | URL                        | METHOD | PARAMETERS |
| ----------------------------- | -------------------------- | ------ | ---------- |
| GET Payment PRN an order      | api/v1/payments-prn/create | POST   | N/A        |
| Check Payment PRN status      | api/v1/payments-prn/check  | POST   | N/A        |
| Cancel Payment PRN            | api/v1/payments-prn/cancel | DELETE | N/A        |
| Receive Payment notifications | api/v1/payments/notify     | GET    | N/A        |

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
