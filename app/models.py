from django.db import models

# Create your models here.
class JobListing(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="job_role/")
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    responsibilities = models.CharField(max_length=5000)
    requirements = models.CharField(max_length=5000)
    status = models.CharField(max_length=100, default='active')
    is_internship = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    custom_fields = models.JSONField(blank=True, null=True)

    
    def get_responsibilities(self):
        return self.responsibilities.split(',')
    
    def get_requiurements(self):
        return self.requirements.split(',')
    
    def __str__(self):
        return self.title


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Screened', 'Screened'),
        ('Short listed', 'Short listed'),
        ('Addressed', 'Addressed'),
        ('Task Assigned', 'Task Assigned'),
        ('Task Completed', 'Task Completed'),
        ('Internship Started', 'Internship Started'),
        ('Internship Completed', 'Internship Completed'),
        ('Onboarded', 'Onboarded'),
        ('Rejected', 'Rejected'),
        ('Held for Review', 'Held for Review'),
        ('Terminated', 'Terminated'),
        ('Relieved', 'Relieved'),
        ('RNR', 'RNR'),
        ('NR', 'NR'),
        ('CBL', 'CBL'),
    ]
    fullName = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    whatsapp = models.CharField(max_length=10)
    dob = models.CharField(max_length=10)
    location = models.CharField(max_length=20)
    willingToRelocate = models.BooleanField()
    education = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    hobbies = models.CharField(max_length=100)
    futurePlan = models.CharField(max_length=100)
    fatherOccupation = models.CharField(max_length=100)
    isFresher = models.BooleanField()
    
    experience_status = models.CharField(max_length=100, blank=True, null=True)
    experience_description = models.CharField(max_length=1000, blank=True, null=True)
    experience_brief = models.CharField(max_length=500, blank=True, null=True)
    currentCTC = models.CharField(max_length=30, blank=True, null=True)
    expectedCTC = models.CharField(max_length=30, blank=True, null=True)
    role = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='job_application')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Pending")
    resume = models.FileField(upload_to="resume/")
    notes = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    
    def get_responsibilities(self):
        return self.responsibilities.split(',')
    
    def get_requiurements(self):
        return self.requirements.split(',')
    
    def __str__(self):
        return f"{self.fullName} - {self.role.title}"