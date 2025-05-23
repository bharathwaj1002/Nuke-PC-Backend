import json
from django.db.models import Count, Q
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
    job_listings = JobListing.objects.filter(is_internship=False)
    serializer = JobListingSerializer(job_listings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_listed_internships(request):
    job_listings = JobListing.objects.filter(is_internship=True)
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
    application_data = request.data

    role = JobListing.objects.get(id=id)

    fullName = application_data.get("fullName")
    email = application_data.get("email")
    mobile = application_data.get("mobile")
    whatsapp = application_data.get("whatsapp")
    dob = f"{application_data.get('dayOfBirth')}/{application_data.get('monthOfBirth')}/{application_data.get('yearOfBirth')}"
    location = application_data.get("location")
    willingToRelocate = application_data.get("willingToRelocate", "").lower() == 'true'
    education = application_data.get("education")
    institution = application_data.get("institution")
    hobbies = application_data.get("hobbies")
    futurePlan = application_data.get("futurePlan")
    fatherOccupation = application_data.get("fatherOccupation")

    isFresher = application_data.get("experience") == "fresher"

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

    resume = request.FILES.get("resume")

    # ✅ Handle custom fields JSON
    custom_fields_json = application_data.get("custom_fields")
    custom_fields = {}
    if custom_fields_json:
        try:
            custom_fields = json.loads(custom_fields_json)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON in custom_fields"}, status=400)

    # Create the job application
    application = JobApplication.objects.create(
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
        resume=resume,
        custom_fields=custom_fields  # ✅ Save parsed JSON here
    )

    return Response({"message": "Job Application successfully submitted."}, status=201)


# Admin Panel APIs
@api_view(["GET"])
@permission_classes([AllowAny])
def admin_get_dashboard_params(request):
    total_jobs = JobListing.objects.count()
    total_applications = JobApplication.objects.count()

    selected_count = JobApplication.objects.filter(status="Short listed").count()
    pending_count = JobApplication.objects.filter(status="Pending").count()

    # Applications grouped by status
    status_counts = JobApplication.objects.values("status").annotate(count=Count("id"))

    # Applications grouped by department
    department_counts = JobApplication.objects.values("role__department").annotate(count=Count("id"))
    department_counts = [{"name": d["role__department"], "count": d["count"]} for d in department_counts]


    # Fresher vs Experienced
    fresher_count = JobApplication.objects.filter(isFresher=True).count()
    exp_count = JobApplication.objects.filter(isFresher=False).count()

    # Short listed vs Rejected
    selected_vs_rejected = JobApplication.objects.values("status").filter(
        Q(status="Short listed") | Q(status="Rejected")
    ).annotate(count=Count("id"))

    return Response({
        "totalJobs": total_jobs,
        "totalApplications": total_applications,
        "applicationsByStatus": list(status_counts),
        "applicationsByDepartment": department_counts,
        "fresherVsExperienced": [
            {"name": "Fresher", "count": fresher_count},
            {"name": "Experienced", "count": exp_count},
        ],
        "selectedVsRejected": list(selected_vs_rejected),
    })



@api_view(["GET"])
@permission_classes([AllowAny])
def admin_get_listed_jobs(request):
    job_listings = JobListing.objects.all()
    serializer = JobListingSerializer(job_listings, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def admin_get_job_applications(request):
    applications = JobApplication.objects.filter(role__is_internship=False)
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def admin_get_internship_applications(request):
    applications = JobApplication.objects.filter(role__is_internship=True)
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def admin_get_applicant(request, id):
    applicant = JobApplication.objects.get(id=id)
    serializer = JobApplicationSerializer(applicant)
    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([AllowAny])
def admin_edit_application(request, id):
    try:
        application = JobApplication.objects.get(id=id)
    except JobApplication.DoesNotExist:
        return Response({"error": "Application not found"}, status=404)

    data = request.data.copy()

    # Clean whitespace
    if 'responsibilities' in data:
        data['responsibilities'] = data['responsibilities'].strip()
    if 'requirements' in data:
        data['requirements'] = data['requirements'].strip()

    serializer = JobApplicationSerializer(application, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def admin_create_job(request):
    print("Incoming data:", request.data)
    print("Incoming files:", request.FILES)

    # Make mutable copy of data
    data = request.data.copy()

    # Clean text fields
    if 'responsibilities' in data:
        data['responsibilities'] = data['responsibilities'].strip()
    if 'requirements' in data:
        data['requirements'] = data['requirements'].strip()

    # Parse custom_fields if it's a JSON string
    custom_fields_raw = data.get('custom_fields')
    try:
        if isinstance(custom_fields_raw, str):
            print("Raw custom_fields string:", custom_fields_raw)
            data['custom_fields'] = json.loads(custom_fields_raw)
    except json.JSONDecodeError as e:
        print("JSON error:", str(e))
        return Response({"custom_fields": "Invalid JSON format"}, status=400)

    # Create a standard Python dict for the serializer
    full_data = dict(data)

    # Convert any single-value lists to raw values
    for key, value in full_data.items():
        if isinstance(value, list) and len(value) == 1:
            full_data[key] = value[0]

    # Add image from request.FILES
    if 'image' in request.FILES:
        full_data['image'] = request.FILES['image']

    print("Prepared data for serializer:", full_data)

    serializer = JobListingSerializer(data=full_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=400)

    


@api_view(["PUT"])
@permission_classes([AllowAny])
def admin_edit_job(request, id):
    try:
        job_listing = JobListing.objects.get(id=id)
    except JobListing.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    data = request.data.copy()

    # Clean whitespace
    if 'responsibilities' in data:
        data['responsibilities'] = data['responsibilities'].strip()
    if 'requirements' in data:
        data['requirements'] = data['requirements'].strip()
    serializer = JobListingSerializer(job_listing, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        return Response(serializer.errors, status=400)
    
    
@api_view(["DELETE"])
@permission_classes([AllowAny])
def admin_delete_job(request, id):
    try:
        job = JobListing.objects.get(id=id)
        job.delete()
        return Response({"message": "Job deleted successfully."}, status=204)
    except JobListing.DoesNotExist:
        return Response({"error": "Job not found."}, status=404)