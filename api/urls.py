import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import patterns, url, include

router = DefaultRouter()
router.register(r'stamp', views.StampViewSet)
router.register(r'description', views.SensorViewSet)
router.register(r'data', views.DataViewSet)


#Define URLs here
urlpatterns = patterns('',
    url(r'^', include(router.urls))
)