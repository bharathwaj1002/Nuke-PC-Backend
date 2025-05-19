from django.contrib import admin
from django.urls import path, re_path
from .views import *
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path("", index, name="index"),
    path("careers", careers, name="careers"),
    path("get-all-listed-jobs", get_listed_jobs, name="get-all-listed-jobs"),
    path("get-job/<str:id>", get_job, name="get-job"),
    path("submit-application/<str:id>", submit_application, name="submit-application"),
]
urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]