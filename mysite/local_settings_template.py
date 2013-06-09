# Here's a template for what your local_settings.py should look like

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = '~/webapps/moderndescartes/emails/'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your email address here'
EMAIL_HOST_PASSWORD = 'enter the real password here'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MEDIA_URL = 'http://moderndescartes.com/media/'

ALLOWED_HOSTS = ['.moderndescartes.com', '75.126.113.164',]
