from xml.etree.ElementInclude import include
from django.urls import path
# from .views import ChartView
from . import views
app_name = "chart"
urlpatterns = [
    # path('doughnut/',ChartView.as_view(), name='index'),
    path('doughnut/',views.test, name='doughnut'),
    
]
