from rest_framework import serializers
from survey.models import *

class TimeStampSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeStamp

class DescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SensorDescription


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData