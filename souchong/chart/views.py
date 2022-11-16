from django.shortcuts import render
from account.models import Account
from urllib import parse
from django.conf import settings
from pyspark.sql.functions import explode
from pyspark.sql.functions import desc
from pyspark.sql.functions import count
# Create your views here.

def top100Skills(request):
    temp = settings.DF.select(explode(settings.DF.skill_stacks)).groupBy("col").agg(count("col").alias("skillCount"))
    temp = temp.filter(temp.col != "").sort(desc('skillCount')).take(100)
    skills = []
    for i in temp:
        skills.append({i.col:i.skillCount})
    return render(request, 'charts/top100Skills.html', {"skills":skills})
    
def skillDetail(request):
    skill = "test"
    return render(request, 'charts/skillDetail.html', {"skill":skill})

# class ChartView(TemplateView):
#     template_name = 'chart/chart.html'
    
#     def __init__(self) -> None:
#         conf = pyspark.SparkConf().set('spark.jars.packages','org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')
#         sc = SparkContext(conf=conf).getOrCreate()
#         sqlContext = SQLContext(sc)
#         my_spark = SparkSession \
#             .builder \
#             .master('local')\
#             .appName("myApp") \
#             .config("spark.mongodb.input.uri", "mongodb://thwhd1:thwhd1@165.132.172.93/wanted.wanted?readPreference=primaryPreferred") \
#             .config("spark.mongodb.output.uri", "mongodb://thwhd1:thwhd1@165.132.172.93/test.wanted") \
#             .getOrCreate()
#         self.df  = my_spark.read.format("mongo").option("uri","mongodb://165.132.172.93/wanted.wanted").load()
#         # test = self.df.filter("UPPER(job_title) LIKE UPPER('%JAVA%')")
#         test = self.df.filter(sql_fun.lower(self.df.job_title).contains("java"))
#         print(test.count())

#     def get_context_data(self, **kwargs):
#         # print(self.df.printSchema())
#         context = super().get_context_data(**kwargs)
#         context["qs"] = Editors.objects.all()
#         context = dict(context)
#         for c in context:
#             print(type(c))
#         return context
    

# class Mongo_DB:
#     def __init__(self, mongo_uri, account, passwd):
#         self.mongo_uri = mongo_uri
#         self.account = account
#         self.passwd= passwd
#         url = 'mongodb://%s:%s@%s:27017/?authSource=admin' % (self.account, parse.quote_plus(self.passwd), self.mongo_uri)
#         client = pymongo.MongoClient(url)
#         self.db = client['wanted']

# def test(request):
#     conn = Mongo_DB('165.132.172.93','thwhd1','thwhd1')
#     cursor = conn.db['wanted'].find({})
#     df = pd.DataFrame(list(cursor))
#     print(df)