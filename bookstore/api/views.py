from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Author, Book
from .filters import BookFilter
from .serializers import AuthorSerializer, BookSerializer
from django.db import transaction
from django.db.models import F


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    @action(detail=True, methods=['post'], url_path='buy')
    def buy(self, request, pk=None):
        try:
            with transaction.atomic():
                updated_count = Book.objects.filter(
                    id=pk, count__gt=0
                ).update(count=F('count') - 1)
                if updated_count == 0:
                    return Response(
                        {'detail': 'Книги нет на складе.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(
                {'message': 'Книга успешно куплена.'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'detail': 'Ошибка при покупке книги: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
