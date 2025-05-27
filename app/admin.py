from django.contrib import admin
from .models import Gallery, JobListing, JobApplication
# Register your models here.
admin.site.register(JobListing)
admin.site.register(JobApplication)
admin.site.register(Gallery)