from django.urls import path,include
from .views import Text2Html,homepage,converts

urlpatterns = [
    path("converttext/", Text2Html),
    path("", homepage),
    path("all/",converts),
]