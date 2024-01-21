from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from .admin import admin_site

urlpatterns = [
    # path('', include('courses.urls')),
    path('', views.index, name='index'),
    path('welcome/<str:year>', views.welcome, name='welcome'),
    path('test/', views.TestView.as_view(), name='test'),
    re_path(r'welcome2/(?P<year>[0-9]{4})/$', views.welcome2, name='welcome'),
    path('admin/', admin.site.urls),

]