import os

# Django settings for wish4meUI project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'http://127.0.0.1:8000'

ADMINS = (
    ('Oguz Yarimtepe', 'oguzyarimtepe@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'wish4me.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8000/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@5kmamo0c@@%ngat%bk(l$4a_-2$*2*pd!co893k1h+$dmt24h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'wish4meUI.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
    os.path.join(PROJECT_PATH, 'templates', 'v1'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'foursq',
    'twitter_app',
    'userprofile',
    'django_openid_auth',
    'google',
    'facebook',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

FACEBOOK_APP_ID = "255768354473895"
FACEBOOK_APP_SECRET = "b8f0ef66e6e88951311ea2e70dccf4fa"
FACEBOOK_SCOPE = 'email,publish_stream'

AUTH_PROFILE_MODULE = 'facebook.FacebookProfile'

AUTHENTICATION_BACKENDS = (
    'facebook.backend.FacebookBackend',
    'google.auth.GoogleBackend',
    'django.contrib.auth.backends.ModelBackend',
)

#required client id and secret
FOURSQ_CLIENT_ID = '1OVOPIR5HS5XEXJYNB4B1QNCPLFLIVULYCGHT3BFSNCG5HMR'
FOURSQ_CLIENT_SECRET = 'JKYYZB5FIDQEHIE3MB4VZARVWWTEZTN1ICOAK1IPFBCHSSQH'

#there must be a password and e-mail for user registration, so these are used by default
DEFAULT_PASSWORD = 'b90f83f387b20a704b65d1dbf94736a9b8864507'
DEFAULT_EMAIL = 'default@wish4me.com'

#Google OpenID login settings
LOGIN_URL = '/google/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/google/logout/'
OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'
