import datetime
import random
import csv
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from models import TimeStamp, SensorDescription, SensorData
# Create your views here.
def index(request):
    """
    Lists latest instrument measurements
    """
    latestStamp = TimeStamp.objects.order_by('-pk')[0]
    #Get all timestamps, order them by latest, and pick the first object

    relatedData = SensorData.objects.filter(relatedStamp_id = latestStamp.id)
    #Get all data that has the latest timestamps id as relatedStamp

    context = { 'data': relatedData, 'stampTime' : latestStamp.stamp.time(), "stampDate" : latestStamp.stamp.date()}
    return render(request, 'survey/index.html', context )

def instrument(request, sort=1):
    """
    Lists all instruments
    """

    instruments = SensorDescription.objects.all()
    #Get all sensors in the database

    latestStamp = TimeStamp.objects.order_by('-pk')[0]

    metingen = SensorData.objects.filter(relatedStamp_id=latestStamp.id)

    context = {'instruments' : instruments, 'data': metingen}
    #Set context for template calls

    return render(request, 'survey/instrument.html', context)


def getSpecificPost(get):
    try:
        first = int(get['start'])
    except:
        first = 1
    try:
        last = int(get['end'])
    except:
        last = 50
    try:
        sort = int(get['sorting'])
    except:
        sort = 1

    return first, last, sort


def instrumentDetail(request, id):
    """
    Lists all measurements from a specific instrument
    """

    if request.POST:
        # Handle forms
        get = request.POST

        if get["action"] == 'download':
            first, last, sort = getSpecificPost(get)
            # Als er gedownload moet worden

            relatedData = SensorData.objects.filter(relatedSensor_id = id).order_by('-id')[first:last*sort:sort]

            relatedSensor = get_object_or_404(SensorDescription, pk=id)
            # Ophalen Data

            response = HttpResponse(content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="%s.csv"' % str(datetime.datetime.now())
            # Schrijven resposnie

            writer = csv.writer(response, delimiter=';')
            # CSVschrijver openen

            writer.writerow(["Tijdstip", "%s (%s)" % (relatedSensor.name, relatedSensor.unit)])

            for row in relatedData:
                writer.writerow([row.relatedStamp.stamp, row.data])

            return response

        elif get["action"] == "specify":
        # Specifieke meetgegevens pakken
            first, last, sort = getSpecificPost(get)

            relatedData = SensorData.objects.filter(relatedSensor_id = id).order_by('-id')[first:last * sort:sort]
            #Get all data related to the instrument

            relatedSensor = get_object_or_404(SensorDescription, pk=id)
            #Get the sensor description, or 404 otherwise

            context = {'sensor' : relatedSensor, 'data': relatedData, "first": first, "last" : last,"sort":sort }

            return render(request, 'survey/instrumentDetail.html', context)


    relatedData = SensorData.objects.filter(relatedSensor_id = id).order_by('-id')[:6]
    #Get all data related to the instrument, and latest 6

    relatedSensor = get_object_or_404(SensorDescription, pk=id)
    #Get the sensor description, or 404 otherwise

    context = {'sensor' : relatedSensor, 'data': relatedData}

    return render(request, 'survey/instrumentDetail.html', context)


def timestamp(request):
    """
    Lists latest timestamp, with link to details
    """

    if request.POST:
        post = request.POST

        if post['action'] == "download":
            first, last, sort = getSpecificPost(post)
            # Get POST variables

            timestamps = TimeStamp.objects.all()[first:last*sort:sort]
            #timestamps.order_by("-pk")
            # Get Timestamps

            sensors = SensorDescription.objects.all().order_by("pk")

            response = HttpResponse(content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="%s.csv"' % str(datetime.datetime.now())
            # Schrijven resposnie

            writer = csv.writer(response, delimiter=';')
            # CSVschrijver openen

            sensorRow = ["Timestamp"]

            for sensor in sensors:
                sensorRow.append("%s (%s)" %(sensor.name , sensor.unit))

            writer.writerow(sensorRow)

            for stamp in timestamps:
                dataRow = [stamp]

                data = SensorData.objects.filter(relatedStamp_id=stamp.id)

                for row in data:
                    dataRow.append(row.data)

                writer.writerow(dataRow)

            return response

        elif post['action'] == "specify":
            first, last, sort = getSpecificPost(post)

            stamps = TimeStamp.objects.all().order_by('-pk')[first:last*sort:sort]
            #Get all stamps, order them bij latest, and then sort by interval

            dataRows = []

            for stamp in stamps:
                dataRow = [stamp]
                data = SensorData.objects.filter(relatedStamp_id=stamp.id)

                for row in data:
                    dataRow.append(row.data)

                dataRows.append(dataRow)

            sensors = SensorDescription.objects.all().order_by('pk')
            context = {'stamps' : dataRows, 'sensors':sensors, 'data':dataRows }
            #Sets the context for template calls


            return render(request, 'survey/stamp.html', context)
            #Renders webpage




    stamps = TimeStamp.objects.all().order_by('-pk')[::1]
    stamps = stamps[:100]
    #Get all stamps, order them bij latest, and then sort by interval

    dataRows = []

    for stamp in stamps:
        dataRow = [stamp]
        data = SensorData.objects.filter(relatedStamp_id=stamp.id)

        for row in data:
            dataRow.append(row.data)

        dataRows.append(dataRow)

    sensors = SensorDescription.objects.all().order_by('pk')
    context = {'stamps' : dataRows, 'sensors':sensors, 'data':dataRows }
    #Sets the context for template calls


    return render(request, 'survey/stamp.html', context)
    #Renders webpage


def timestampDetail(request,id):
    """
    Lists all measurements from a specific timestamp
    """
    relatedData = SensorData.objects.filter(relatedStamp_id = id)
    #Get all data with the related timestamp

    relatedStamp = get_object_or_404(TimeStamp, pk=id)
    #Get timestamp to display

    context = {'stampTime': relatedStamp.stamp.time(), 'stampDate':relatedStamp.stamp.date(),  'data' : relatedData}
    return render(request, 'survey/stampDetailed.html', context)


def generate(request):
    """
    Generate fake data, and redirect back to index

    A lot of data
    """
    current  = TimeStamp.objects.order_by('-pk')[0].stamp
    if current == 0:
        current = datetime.datetime.now()
    delta = datetime.timedelta(minutes=10)
    for x in range(0, 4000):
        # get a timestamp

        timestampf = TimeStamp(stamp=current)
        timestampf.save()
        #Add timestamp to database

        sensors = SensorDescription.objects.all()
        #Get all available sensors

        random.seed(current)
        for sensor in sensors:
            fakeData = random.randint(1, 2000)

            newEntry = SensorData(relatedStamp=timestampf, relatedSensor=sensor, data=fakeData)

            newEntry.save()

        current += delta

    return index(request)


def download(request, amount = 0, interval = 0):
    """
    Either generates a .csv file, or
    """
    if request.GET:
        #Generate download data
        now = datetime.datetime.now()
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % str(now)

        writer = csv.writer(response, delimiter=';')

        dataRow = ['timestamp']

        stamps = TimeStamp.objects.all()[::int(request.GET['interval'])]
        stamps = stamps[:int(request.GET['amount'])]

        sensors = SensorDescription.objects.all()

        for sensor in sensors:
            dataRow.append(str(sensor) + (" (%s)" % sensor.unit))

        writer.writerow(dataRow)

        for stamp in stamps:
            dataRow = [str(stamp.stamp)]
            data = SensorData.objects.filter(relatedStamp=stamp).order_by("relatedSensor")

            for row in data:
                dataRow.append(row.data)


            writer.writerow(dataRow)
        return response
    else:
        stampCount = TimeStamp.objects.count()

        context = {'stampcount' : stampCount}

        return render(request, "survey/download.html", context)


def find(request):
    """
    Attempts to find a specific timestamp
    """
    return HttpResponse("In construction")