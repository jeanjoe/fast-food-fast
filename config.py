class Config():
    DEBUG = False
    SECRET_KEY="whsdyuhgshji90woiryh3ikwgrdn9w7eui3kgwbnidjhnsmufycneh"

class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME= "fast_foods_fast"
    DB_USER= "postgres"
    DB_PASS= "manben"
    DB_HOST= "localhost"
    DB_PORT= "5432"

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

    DB_NAME= "fast_foods_fast_test"
    DB_USER= "postgres"
    DB_PASS= "manben"
    DB_HOST= "localhost"
    DB_PORT= "5432"
    