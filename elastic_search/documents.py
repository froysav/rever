from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from reste.models import Product


@registry.register_document
class CourseDocument(Document):
    name = fields.TextField(
        attr='name',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )

    class Index:
        name = 'course'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Product
