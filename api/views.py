from survey.models import *
from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import viewsets

class StampViewSet(viewsets.ModelViewSet):
    queryset = TimeStamp.objects.all()
    serializer_class = TimeStampSerializer

class DataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = DataSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = SensorDescription.objects.all()
    serializer_class = DescriptionSerializer