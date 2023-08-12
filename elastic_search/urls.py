from django.urls import path, include
from rest_framework.routers import DefaultRouter
from elastic_search.views import CourseDocumentViewSet

router = DefaultRouter()
router.register(r'course', CourseDocumentViewSet, 'course')

urlpatterns = [
    path('', include(router.urls)),
]
