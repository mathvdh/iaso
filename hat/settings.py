"""
Django settings for iaso project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sentry_sdk
from datetime import timedelta


TESTING = os.environ.get("TESTING", "").lower() == "true"
PLUGIN_POLIO_ENABLED = os.environ.get("PLUGIN_POLIO_ENABLED", "").lower() == "true"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "").lower() == "true"
USE_S3 = os.getenv("USE_S3") == "true"

DEV_SERVER = os.environ.get("DEV_SERVER", "").lower() == "true"
ENVIRONMENT = os.environ.get("IASO_ENVIRONMENT", "development").lower()
SENTRY_URL = os.environ.get("SENTRY_URL", "")

ALLOWED_HOSTS = ["*"]

# Tell django to view requests as secure(ssl) that have this header set
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")

# Default site for django contrib site framework
SITE_ID = 1


# Logging

LOGGING_LEVEL = os.getenv("DJANGO_LOGGING_LEVEL", "INFO")
if TESTING:
    # We don't want to see log output when running tests
    LOGGING_LEVEL = "CRITICAL"


ENKETO = {
    "ENKETO_DEV": os.getenv("ENKETO_DEV"),
    "ENKETO_API_TOKEN": os.getenv("ENKETO_API_TOKEN"),
    "ENKETO_URL": os.getenv("ENKETO_URL"),
    "ENKETO_API_SURVEY_PATH": "/api_v2/survey",
    "ENKETO_API_INSTANCE_PATH": "/api_v2/instance",
}

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"default": {"format": "%(levelname)-8s %(asctime)s %(name)s -- %(message)s"}},
    "filters": {"no_static": {"()": "hat.common.log_filter.StaticUrlFilter"}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            # Don't pollute the log output with lots of static url request in development
            "filters": ["no_static"] if DEBUG else None,
        }
    },
    "loggers": {
        "django": {"level": LOGGING_LEVEL},
        "rq": {"level": LOGGING_LEVEL},
        "hat": {"level": LOGGING_LEVEL},
        "iaso": {"level": LOGGING_LEVEL},
        "beanstalk_worker": {"level": LOGGING_LEVEL},
        #  Uncomment to print all sql query
        # 'django.db.backends': {'level': 'DEBUG'},
        "": {"handlers": ["console"]},
    },
}

# AWS expects python logs to be stored in this folder
AWS_LOG_FOLDER = "/opt/python/log"
if os.path.isdir(AWS_LOG_FOLDER):
    if os.access(AWS_LOG_FOLDER, os.W_OK):
        print("Logging to django log")
        LOGGING["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": os.path.join(AWS_LOG_FOLDER, "django.log"),
        }
        LOGGING["loggers"][""]["handlers"].append("file")
        LOGGING["loggers"]["hat"]["level"] = "DEBUG"
    else:
        print(f"WARNING: we seem to be running on AWS but {AWS_LOG_FOLDER} is not writable, check ebextensions")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.postgres",
    "django.contrib.sites",  # needed by contrib-comments
    "storages",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "webpack_loader",
    "django_ltree",
    "hat.sync",
    "hat.vector_control",
    "hat.audit",
    "hat.menupermissions",
    "iaso",
    "django_extensions",
    "beanstalk_worker",
    "django_comments",
]

# needed because we customize the comment model
# see https://django-contrib-comments.readthedocs.io/en/latest/custom.htm
COMMENTS_APP = "iaso"

if PLUGIN_POLIO_ENABLED:
    INSTALLED_APPS.append("plugins.polio")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hat.urls"


# Allow cors for all origins but only for the sync endpoint
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
# CORS_URLS_REGEX = r"^/sync/.*$"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["./hat/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.contrib.messages.context_processors.messages",
                "hat.common.context_processors.appversions",
                "hat.common.context_processors.environment",
            ]
        },
    }
]

WSGI_APPLICATION = "hat.wsgi.application"


# Database

DB_NAME = os.environ.get("RDS_DB_NAME", "iaso")
DB_USERNAME = os.environ.get("RDS_USERNAME", "postgres")
DB_PASSWORD = os.environ.get("RDS_PASSWORD", None)
DB_HOST = os.environ.get("RDS_HOSTNAME", "db")
DB_PORT = os.environ.get("RDS_PORT", 5432)
SNS_NOTIFICATION_TOPIC = os.environ.get("SNS_NOTIFICATION_TOPIC", None)

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": DB_NAME,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}


def is_superuser(u):
    return u.is_superuser


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization

LANGUAGE_CODE = "en"

LOCALE_PATHS = ["/opt/app/hat/locale/", "hat/locale/"]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"


AUTH_CLASSES = [
    "iaso.api.auth.authentication.CsrfExemptSessionAuthentication",
    "rest_framework_simplejwt.authentication.JWTAuthentication",
]


# Needed for PowerBI, used for the Polio project, which only support support BasicAuth.
if PLUGIN_POLIO_ENABLED:
    AUTH_CLASSES.append(
        "rest_framework.authentication.BasicAuthentication",
    )

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": AUTH_CLASSES,
    "DEFAULT_PERMISSION_CLASSES": ("hat.api.authentication.UserAccessPermission",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": None,
    "DEFAULT_THROTTLE_RATES": {"anon": "200/day"},
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_csv.renderers.CSVRenderer",
    ),
}

SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(days=3650), "REFRESH_TOKEN_LIFETIME": timedelta(days=3651)}

AWS_S3_REGION_NAME = "eu-central-1"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

if USE_S3:
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_IS_GZIPPED = True
    AWS_S3_FILE_OVERWRITE = False
    S3_USE_SIGV4 = True
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_HOST = "s3.eu-central-1.amazonaws.com"
    AWS_DEFAULT_ACL = None

    # s3 static settings
    STATIC_LOCATION = "iasostatics"
    STATICFILES_STORAGE = "iaso.storage.StaticStorage"
    STATIC_URL = "https://%s.s3.amazonaws.com/%s/" % (AWS_STORAGE_BUCKET_NAME, STATIC_LOCATION)
    MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME  # subdirectories will depend on field
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    MEDIA_URL = "/media/"
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "iaso/static"),
    os.path.join(BASE_DIR, "plugins/polio/static/polio"),
    os.path.join(BASE_DIR, "hat/assets/webpack"),
)

# Javascript/CSS Files:
WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "",  # used in prod
        "STATS_FILE": os.path.join(
            PROJECT_ROOT,
            "assets/webpack",
            "webpack-stats.json"
            if (DEBUG and not os.environ.get("TEST_PROD", None) and not USE_S3)
            else "webpack-stats-prod.json",
        ),
    }
}


AUTH_PROFILE_MODULE = "hat.users.Profile"

if SENTRY_URL:
    sentry_sdk.init(SENTRY_URL, traces_sample_rate=1.0)

# Workers configuration

BEANSTALK_WORKER = bool(os.environ.get("WORKER", False))
BEANSTALK_SQS_URL = os.environ.get(
    "BEANSTALK_SQS_URL", "https://sqs.eu-central-1.amazonaws.com/198293380284/iaso-staging-queue"
)
BEANSTALK_SQS_REGION = os.environ.get("BEANSTALK_SQS_REGION", "eu-central-1")

if DEBUG:
    BEANSTALK_TASK_SERVICE = "beanstalk_worker.services.FakeTaskService"
else:
    BEANSTALK_TASK_SERVICE = "beanstalk_worker.services.TaskService"

# BEANSTALK_TASK_SERVICE = "beanstalk_worker.services.TaskService"

SSL_ON = (not DEBUG) and (not BEANSTALK_WORKER)
if SSL_ON:
    SECURE_HSTS_SECONDS = 31_536_000  # 1 year
SECURE_SSL_REDIRECT = SSL_ON

# Email configuration

DEFAULT_FROM_EMAIL = "Iaso Team <iaso@bluesquare.org>"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "mail.smtpbucket.com")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "8025")
