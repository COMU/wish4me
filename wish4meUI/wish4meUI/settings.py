import os

# Django settings for wish4meUI project.

PROJECT_NAME = 'Wish4Me'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'http://127.0.0.1:8000'

ADMINS = (
    ('Oguz Yarimtepe', 'oguzyarimtepe@gmail.com'),
    ('Mesutcan Kurt', 'mesutcank@gmail.com'),
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
MEDIA_URL = BASE_URL+'/site_media/'

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

    # Use one of the following to switch design

    # 960.gs design
    #os.path.join(PROJECT_PATH, 'templates'),

    # Bootstrap design
    os.path.join(PROJECT_PATH, 'templates', 'v2'),
    #os.path.join(PROJECT_PATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "userprofile.context_processors.default_profile_image",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.comments',
    'foursq',
    'twitter_app',
    'userprofile',
    'django_openid_auth',
    'wish4meUI.google',
    'facebook',
    'wish',
    'wishlist',
    'friend',
    'ajax_select',
    'contact_importer',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
#for web development
FACEBOOK_APP_ID = "255768354473895"
FACEBOOK_APP_SECRET = "b8f0ef66e6e88951311ea2e70dccf4fa"
FACEBOOK_SCOPE = 'email,publish_stream,friends_about_me'

#for android app testing:
#FACEBOOK_APP_ID = "408993659121861"
#FACEBOOK_APP_SECRET = "36f0be90d364e91d732438b816daace4"
#FACEBOOK_SCOPE = 'email,publish_stream,friends_about_me'

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'

AUTHENTICATION_BACKENDS = (
    'facebook.auth.FacebookBackend',
    'wish4meUI.google.auth.GoogleAuthBackend',
    'wish4meUI.twitter_app.auth.TwitterAuthBackend',
    'wish4meUI.foursq.auth.FoursqAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

#required client id and secret
FOURSQ_CLIENT_ID = '1OVOPIR5HS5XEXJYNB4B1QNCPLFLIVULYCGHT3BFSNCG5HMR'
FOURSQ_CLIENT_SECRET = 'JKYYZB5FIDQEHIE3MB4VZARVWWTEZTN1ICOAK1IPFBCHSSQH'

#there must be a password and e-mail for user registration, so these are used by default
DEFAULT_PASSWORD = 'b90f83f387b20a704b65d1dbf94736a9b8864507'
DEFAULT_EMAIL = 'default@wish4me.com'

#Google OpenID login settings
LOGIN_URL = '/?redirect=true'
LOGIN_REDIRECT_URL = '/user/loginSuccess'
LOGOUT_URL = '/'
OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

FIXTURE_DIRS = (PROJECT_PATH+'/',)
DEFAULT_PROFILE_PICTURE = ("images/defaultProfile.jpg")

#Ajax Selects Options
AJAX_LOOKUP_CHANNELS = {
    #   pass a dict with the model and the field to search against
    'user-channel'  : {'model':'auth.user', 'search_field':'username'}
}
# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'

#Session settings:
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "sessionid"

#location search oauth token
#username: wish4meinfo@gmail.com
#password: wish4me1nfo
LOCATION_SEARCH_OAUTH_TOKEN = "15L2WG3D34CCX3FZNJZRQMZUAXHFFL2HCP1LT3LJSOQR0BDB"