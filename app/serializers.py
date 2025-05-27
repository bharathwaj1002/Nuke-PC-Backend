from rest_framework import serializers
from app.models import JobListing, JobApplication, Gallery

class JobListingSerializer(serializers.ModelSerializer):
    application_count = serializers.SerializerMethodField()
    class Meta:
        model = JobListing
        fields = '__all__'
        
    def get_application_count(self, obj):
        return obj.job_application.count()
        
class JobApplicationSerializer(serializers.ModelSerializer):
    role_title = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = '__all__'

    def get_role_title(self, obj):
        return obj.role.title if obj.role else None
    
class GallerySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ['id', 'url', 'alt']  # select fields explicitly

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return ''