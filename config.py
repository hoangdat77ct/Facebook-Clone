import datetime
SECRET_KEY = 'thisissecret'
JSON_AS_ASCII = False
DEBUG = True
CORS_HEADERS= 'Content-Type'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'datnguyen.mkd@gmail.com'
MAIL_PASSWORD = 'Hoangdat77ct'
MAIL_USE_SSL = True
UPLOAD_FOLDER = '/home/demon/BIWOCO/'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024