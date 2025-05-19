from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import *
# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    return Response("Hello World!")

@api_view(['GET'])
@permission_classes([AllowAny])
def careers(request):
    return Response("Careers Response!")

@api_view(['GET'])
@permission_classes([AllowAny])
def get_listed_jobs(request):
    job_listings = JobListing.objects.all()
    serializer = JobListingSerializer(job_listings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_job(request, id):
    job = JobListing.objects.get(id=id)
    serializer = JobListingSerializer(job)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_application(request, id):
    # Access the flat structure directly from request.data
    application_data = request.data
    print(application_data)

    # Get the role/job listing
    role = JobListing.objects.get(id=id)

    # Extract the fields directly from the request data
    fullName = application_data.get("fullName")
    email = application_data.get("email")
    mobile = application_data.get("mobile")
    whatsapp = application_data.get("whatsapp")
    dob = f"{application_data.get('dayOfBirth')}/{application_data.get('monthOfBirth')}/{application_data.get('yearOfBirth')}"
    location = application_data.get("location")
    
    # Convert 'willingToRelocate' from string to boolean
    willingToRelocate = application_data.get("willingToRelocate").lower() == 'true'
    
    education = application_data.get("education")
    institution = application_data.get("institution")
    hobbies = application_data.get("hobbies")
    futurePlan = application_data.get("futurePlan")
    fatherOccupation = application_data.get("fatherOccupation")

    # Default fresher status
    isFresher = application_data.get("experience") == "fresher"

    # Experience-related fields (only if not fresher)
    experience_status = None
    experience_description = None
    experience_brief = None
    currentCTC = None
    expectedCTC = None
    if not isFresher:
        experience_status = application_data.get("currentStatus")
        experience_description = application_data.get("jobDescription")
        experience_brief = application_data.get("responsibilities")
        currentCTC = application_data.get("ctc")
        expectedCTC = application_data.get("expectedSalary")

    # Get the resume file (if any)
    resume = request.FILES.get("resume")

    # Create the job application
    if isFresher:
        JobApplication.objects.create(
            fullName=fullName,
            email=email,
            mobile=mobile,
            whatsapp=whatsapp,
            dob=dob,
            location=location,
            willingToRelocate=willingToRelocate,
            education=education,
            institution=institution,
            hobbies=hobbies,
            futurePlan=futurePlan,
            fatherOccupation=fatherOccupation,
            isFresher=isFresher,
            role=role,
            resume=resume
        )
    else:
        JobApplication.objects.create(
            fullName=fullName,
            email=email,
            mobile=mobile,
            whatsapp=whatsapp,
            dob=dob,
            location=location,
            willingToRelocate=willingToRelocate,
            education=education,
            institution=institution,
            hobbies=hobbies,
            futurePlan=futurePlan,
            fatherOccupation=fatherOccupation,
            isFresher=isFresher,
            experience_status=experience_status,
            experience_description=experience_description,
            experience_brief=experience_brief,
            currentCTC=currentCTC,
            expectedCTC=expectedCTC,
            role=role,
            resume=resume
        )

    return Response({"message": "Job Application successfully submitted."}, status=201)


@api_view(["GET"])
@permission_classes([AllowAny])
def admin_get_listed_jobs(request):
    job_listings = JobListing.objects.all()
    serializer = JobListingSerializer(job_listings, many=True)
    return Response(serializer.data)

