from django.contrib import admin
from models import SensorDescription, SensorData, TimeStamp, Interval


# Register your models here.
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'relatedSensor', 'relatedStamp')
    list_filter = ('relatedSensor', 'relatedStamp')

    fieldsets = (
        (
            'Relations' ,
            {
                'fields': ('relatedSensor', 'relatedStamp'),
            }
        ),
        (
            'Data Entry',
            {
                'fields': ('data',),
            }
        ),
    )

class SensorDataInline(admin.TabularInline):
    model = SensorData
    extra = 5
    can_delete = False


class SensorDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'unit')
    list_per_page = 30

    inlines = [
        SensorDataInline,
    ]


class TimeStampAdmin(admin.ModelAdmin):
    list_display = ('id', 'stamp')

    inlines = [
        SensorDataInline,
    ]


class IntervalAdmin(admin.ModelAdmin):
    pass


admin.site.register(SensorData, SensorDataAdmin)
admin.site.register(SensorDescription, SensorDescriptionAdmin)
admin.site.register(TimeStamp, TimeStampAdmin)
admin.site.register(Interval)