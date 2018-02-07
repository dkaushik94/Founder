



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dev_grappus',
        'USER':'root',
        'PASSWORD':'grappus',
        'HOST':'localhost',
        'PORT':3306
    }
}


startup_images_file_path = '/home/ubuntu/startupportal/portal/media/startup_pics/'

user_images_file_path = '/home/ubuntu/startupportal/portal/media/profile_pic/'

posts_images_file_path = '/home/ubuntu/startupportal/portal/media/postimages/'

events_images_file_path = '/home/ubuntu/startupportal/portal/media/event_pics/'


# Logging Settings.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/home/ubuntu/startupportal_dev/startupportal/dev-debug.log'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
    },
}

RSA_KEY_PATH = '/home/ubuntu/startupportal_dev/startupportal/portal/portal/rsa_key.pem'
