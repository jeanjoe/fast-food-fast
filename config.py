class Config():
    DEBUG = False
    SECRET_KEY = "whsdyuhgshji90woiryh3ikwgrdn9w7eui3kgwbnidjhnsmufycneh"
    DB_NAME = "d4554bh5hlg666"
    DB_USER = "biizsdnusllfom"
    DB_PASS = "a849805a16d39043891cb68791f88dee03bbd75fc78eb27873751749e7bf669e"
    DB_HOST = "ec2-54-221-225-11.compute-1.amazonaws.com"
    DB_PORT = "5432"


class DevelopmentConfig(Config):
    DEBUG = False
    DB_NAME = "fast_foods_fast"
    DB_USER = "postgres"
    DB_PASS = "manben"
    DB_HOST = "localhost"
    DB_PORT = "5432"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

    DB_NAME = "fast_foods_fast_test"
    DB_USER = "postgres"
    DB_PASS = "manben"
    DB_HOST = "localhost"
    DB_PORT = "5433"
