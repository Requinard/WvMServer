from django.db import models

# Create your models here


class TimeStamp(models.Model):
    stamp = models.DateTimeField()

    def __str__(self):
        return str(self.stamp)


class SensorDescription(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    dui = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class SensorData(models.Model):
    relatedStamp = models.ForeignKey(TimeStamp)
    relatedSensor = models.ForeignKey(SensorDescription)
    data = models.CharField(max_length=10)

    def __str__(self):
        return str(self.relatedSensor.name + " " + str(self.relatedSensor.id) + " op " + str(self.relatedStamp.stamp))
