from django.urls import re_path,path
from . import views




urlpatterns = [
    re_path("custom_user/",views.CreateCustomUserView,name="custom"),
    re_path("login/$",views.LoginView,name="loginView"),
    re_path("logout/$",views.logoutUser,name="logout"),
    re_path("upload/$",views.imageUpload,name="image_upload"),
    re_path("download/$",views.downloadCSV,name="download"),
    re_path("managerView/$",views.managerView,name="managerView"),
    re_path("salesmanView/$",views.salesmanView,name="salesmanView"),

]


