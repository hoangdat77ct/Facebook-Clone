import datetime
SECRET_KEY = 'thisissecret'
JSON_AS_ASCII = False
DEBUG = True
CORS_HEADERS= 'Content-Type'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)