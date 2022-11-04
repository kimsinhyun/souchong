from xml.etree.ElementInclude import include
from django.urls import path
# from .views import ChartView
from . import views
urlpatterns = [
    # path('doughnut/',ChartView.as_view(), name='index'),
    path('doughnut/',views.test, name='doughnut'),
    path('home/',views.home, name='home'),
]
