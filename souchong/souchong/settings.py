"""
Django settings for souchong project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"BASE_DIR={BASE_DIR}")
# APPS_DIR = os.path.join(BASE_DIR, 'souchong')
# TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-21ct7f5zzqvtrutju1@ne2fvh(%c^2v#hh^x5o-32bt-gf_f4$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # During development only
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chart.apps.ChartConfig',
    'account.apps.AccountConfig',
    'mathfilters',
    # 'crispy_forms',
    # 'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS='bootstrap5'
CRISPY_TEMPLATE_PACKS='bootstrap5'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'souchong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'souchong.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
    # 'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
    #     'ENGINE': 'djongo',
    #     'ENFORCE_SCHEMA': True,
    #     'LOGGING':{
    #         'version':1,
    #         'loggers':{
    #             'djongo':{
    #                 'level': 'DEBUG',
    #                 'propogate': False,
    #             }
    #         },
    #     },
    #     'NAME':'wanted',
    #     'CLIENT':{
    #         'host':'165.132.172.93',
    #         'port':27017,
    #         'username':'thwhd1',
    #         'password':'thwhd1',
    #         'authSource':'admin',
    #         'authMechanism':'SCRAM-SHA-1'
    #     }
    # }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_URL = '/static/'

STATICFILES_DIRS = [                        #Debuging 용도로만 사용 됨.
    os.path.join(BASE_DIR,'static'),
    os.path.join(BASE_DIR,'media'),
]
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')   #(실서버용 static root)cdn 은 aws와 같은 클라우드에 배포했을 경우를 시뮬레이팅하기 위한 용도
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')     #cdn -> content delivery network

TEMP = os.path.join(BASE_DIR, 'media_cdn/temp')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

AUTH_USER_MODEL = 'account.Account'
# ATUHENTICATION_BACKENDS= (
#     'django.contrib.auth.backends',
#     'account.backends.CaseInsensitiveModelBackend'
# )

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# LOGIN_REDIRECT_URL = '/home'
# LOGOUT_REDIRECT_URL = '/login'

# SESSION_COOKIE_SECURE  = False
BASE_URL = "http://165.132.172.93:8000"
DATA_UPLOAD_MAX_MEMORY_SIZE = 10*1024*1024  #10 MB (max media size)


# ===================SparkSession===================
import pyspark
from pyspark.sql import SparkSession, SQLContext
from pyspark.context import SparkContext
import pyspark.sql.functions as sql_fun

conf = pyspark.SparkConf().set('spark.jars.packages','org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')
sc = SparkContext(conf=conf).getOrCreate()
sqlContext = SQLContext(sc)
my_spark = SparkSession \
    .builder \
    .master('local')\
    .appName("myApp") \
    .config("spark.mongodb.input.uri", "mongodb://thwhd1:thwhd1@165.132.172.93/wanted.wanted?readPreference=primaryPreferred") \
    .config("spark.mongodb.output.uri", "mongodb://thwhd1:thwhd1@165.132.172.93/test.wanted") \
    .getOrCreate()
DF  = my_spark.read.format("mongo").option("uri","mongodb://165.132.172.93/wanted.wanted").load()


from pyspark.sql.functions import explode, count, desc, countDistinct, lower, monotonically_increasing_id
temp = DF.select(explode(DF.skill_stacks).alias("skill"), "company_name")
skillCount = temp.groupBy("skill")\
                .agg(count("skill").alias("skillCount"))\
                .filter(temp.skill != "")\
                .sort(desc("skillCount"))
skillCount.collect()

companyCount = temp.groupBy("skill")\
            .agg(countDistinct("company_name").alias("companyCount"))\
            .filter(temp.skill != "")\
            .sort(desc("companyCount"))
companyCount.collect()                
JOINED_DF = skillCount.join(companyCount, ['skill'], 'outer')
JOINED_DF = JOINED_DF\
                    .filter(JOINED_DF.skill!="")\
                    .sort(desc("skillCount"))
JOINED_DF = JOINED_DF.withColumn("index", monotonically_increasing_id()+1)