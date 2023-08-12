from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION, ALL_SUGGESTERS
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, SuggesterFilterBackend, \
    CompoundSearchFilterBackend, FilteringFilterBackend
from django_elasticsearch_dsl_drf.pagination import QueryFriendlyPageNumberPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework.permissions import AllowAny

from elastic_search.documents import CourseDocument
from elastic_search.serializers import CourseDocumentSerializer


class CourseDocumentViewSet(DocumentViewSet):
    document = CourseDocument
    serializer_class = CourseDocumentSerializer
    pagination_class = QueryFriendlyPageNumberPagination
    permission_classes = [AllowAny]
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        SuggesterFilterBackend
    ]
    search_fields = (
        'name',
    )
    filter_fields = {
        'category': 'category'
    }
    suggester_fields = {
        'name': {
            'field': 'name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }
