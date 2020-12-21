import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# psycopg2
POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'appventa',
        'USER': 'postgres',
        'PASSWORD': '3008',
        'HOST': 'localhost',
        'POST': '5432'
    }
}

# mysqlclient
MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

# heroku
HEROKU = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd43oldbfc54pj',
        'USER': 'rnwyloeuircqlh',
        'PASSWORD': 'e06b24ee24353b9f1c8a81a19f30d7ffccc2ceabe0c14ab25f853b09dc5ce31c',
        'HOST': 'ec2-75-101-212-64.compute-1.amazonaws.com',
        'POST': '5432'
    }
}
