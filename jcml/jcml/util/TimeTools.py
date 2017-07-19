



DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
         'ENGINE'   : 'mongodb',
         'DBNAME'   : 'jcml',
         'USERNAME' : 'baoer',
         'PASSWORD' : '123456',
         'HOST'     : '127.0.0.1',
         'PORT'     : '27017'
    }
}