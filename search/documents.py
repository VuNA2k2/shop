from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from book.models import Book, Author, Category, Publisher, PublisherRefBook
from mobile.models import Mobile


@registry.register_document
class AuthorDocument(Document):
    class Index:
        name = 'authors'

    class Django:
        model = Author
        fields = ['id', 'name', 'email', 'phone']


@registry.register_document
class PublisherDocument(Document):
    class Index:
        name = 'publishers'

    class Django:
        model = Publisher
        fields = ['id', 'name', 'email', 'phone']


@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'categories'

    class Django:
        model = Category
        fields = ['id', 'name', 'description']


@registry.register_document
class BookDocument(Document):
    class Index:
        name = 'books'

    class Django:
        model = Book
        fields = ['id', 'title', 'year', 'description', 'language']
        related_models = [Author, Category, Publisher]

    author = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'email': fields.TextField(),
        'phone': fields.TextField()
    })
    publishers = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'email': fields.TextField(),
        'phone': fields.TextField()
    }, attr='publisherrefbook_set')

    category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField()
    })

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Author):
            return related_instance.book_author.all()
        elif isinstance(related_instance, Category):
            return related_instance.book_category.all()
        elif isinstance(related_instance, Publisher):
            return related_instance.publisherrefbook_set.all()

    def prepare(self, instance):
        data = super().prepare(instance)
        data['author'] = {
            'id': instance.author_id.id,
            'name': instance.author_id.name,
            'email': instance.author_id.email,
            'phone': instance.author_id.phone
        }
        data['publishers'] = [{
            'id': publisher.publisher_id.id,
            'name': publisher.publisher_id.name,
            'email': publisher.publisher_id.email,
            'phone': publisher.publisher_id.phone
        } for publisher in instance.publisherrefbook_set.all()]
        data['category'] = {
            'id': instance.category_id.id,
            'name': instance.category_id.name,
            'description': instance.category_id.description
        }
        return data

    def to_dict(self, include_meta=False, skip_empty=True):
        data = {
            'id': self.id,
            'title': self.title,
            'author': {
                'id': self.author.id,
                'name': self.author.name,
                'email': self.author.email,
                'phone': self.author.phone
            },
            'publishers': [{
                'id': publisher.id,
                'name': publisher.name,
                'email': publisher.email,
                'phone': publisher.phone
            } for publisher in self.publishers],
            'year': self.year,
            'description': self.description,
            'language': self.language,
            'category': {
                'id': self.category.id,
                'name': self.category.name,
                'description': self.category.description
            },
        }
        return data


@registry.register_document
class MobileDocument(Document):
    category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField()
    })

    class Index:
        name = 'mobiles'

    class Django:
        model = Mobile
        fields = ['id', 'name', 'description', 'brand', 'model']
        related_models = [Category]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.mobile_category.all()

    def prepare(self, instance):
        data = super().prepare(instance)
        data['category'] = {
            'id': instance.category_id.id,
            'name': instance.category_id.name,
            'description': instance.category_id.description
        }
        return data
