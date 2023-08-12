from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from elastic_search.documents import CourseDocument


class CourseDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CourseDocument
        fields = ['id', 'name', ]
