from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Editors
from urllib import parse
import pandas as pd
import pymongo
import findspark
import pyspark
from pyspark.sql import SparkSession, SQLContext
from pyspark.context import SparkContext

# Create your views here.

class ChartView(TemplateView):
    print("test")
    template_name = 'chart/chart.html'
    def get_context_data(self, **kwargs):
        # sc = SparkContext('local')
        # spark = SparkSession(sc)
        conf = pyspark.SparkConf().set('spark.jars.packages','org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')
        sc = SparkContext(conf=conf)
        sqlContext = SQLContext(sc)
        my_spark = SparkSession \
            .builder \
            .master('local')\
            .appName("myApp") \
            .config("spark.mongodb.input.uri", "mongodb://thwhd1:thwhd1@165.132.172.93/wanted.wanted?readPreference=primaryPreferred") \
            .config("spark.mongodb.output.uri", "mongodb://thwhd1:thwhd1@165.132.172.93/test.wanted") \
            .getOrCreate()
        df = my_spark.read.format("mongo").option("uri","mongodb://165.132.172.93/wanted.wanted").load()
        print(df.printSchema())

class Mongo_DB:
    def __init__(self, mongo_uri, account, passwd):
        self.mongo_uri = mongo_uri
        self.account = account
        self.passwd= passwd
        url = 'mongodb://%s:%s@%s:27017/?authSource=admin' % (self.account, parse.quote_plus(self.passwd), self.mongo_uri)
        client = pymongo.MongoClient(url)
        self.db = client['wanted']

def test(request):
    conn = Mongo_DB('165.132.172.93','thwhd1','thwhd1')
    cursor = conn.db['wanted'].find({})
    df = pd.DataFrame(list(cursor))
    print(df)