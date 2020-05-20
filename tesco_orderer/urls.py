from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login/', view_login, name="loginpage"),
    path('signup/', view_signup),
    path('logout/', view_logout),
    path("changeaccount/", change_account)
]
