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
    path("get-all-listed-internships", get_listed_internships, name="get-all-listed-internships"),
    path("get-job/<str:id>", get_job, name="get-job"),
    path("submit-application/<str:id>", submit_application, name="submit-application"),
    
    
    # Admin APIs
    
    path("dashboard", admin_get_dashboard_params, name="dashboard"),
    path("jobs", admin_create_job, name="create-job"),
    path("get-job-applications", admin_get_job_applications, name="get-all-applications"),
    path("get-internship-applications", admin_get_internship_applications, name="get-all-applications"),
    path("get-applicant/<str:id>", admin_get_applicant, name="get-applicant"),
    path("edit-application/<str:id>", admin_edit_application, name="edit-application"),
    path("edit-job/<str:id>", admin_edit_job, name="edit-job"),
    path("delete-job/<str:id>", admin_delete_job, name="delete-job"),
]
urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]