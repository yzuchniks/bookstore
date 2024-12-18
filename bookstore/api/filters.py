import django_filters

from books.models import Book


class BookFilter(django_filters.FilterSet):

    author_first_name = django_filters.CharFilter(
        field_name='author__first_name', lookup_expr='icontains'
    )
    author_last_name = django_filters.CharFilter(
        field_name='author__last_name', lookup_expr='icontains'
    )

    class Meta:
        model = Book
        fields = ['author_first_name', 'author_last_name']
