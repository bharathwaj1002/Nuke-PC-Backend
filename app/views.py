from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    return Response("Hello World!")

@api_view(['GET'])
@permission_classes([AllowAny])
def careers(request):
    return Response("Careers Response!")