from xml.etree.ElementInclude import include
from django.urls import path
from . import views
app_name = "chart"
urlpatterns = [
    # path('doughnut/',ChartView.as_view(), name='index'),
    # path('doughnut/',views.top100skills, name='doughnut'),
    path('top100Skills/',views.top100Skills, name='top100Skills'),
    path('skillDetail/',views.skillDetail, name='skillDetail'),
    
    
]
