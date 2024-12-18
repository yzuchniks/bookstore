from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Author, Book
from .filters import BookFilter
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    @action(detail=True, methods=['post'], url_path='buy')
    def buy(self, request, pk=None):
        book = self.get_object()

        if book.count <= 0:
            return Response(
                {'detail': 'Книги нет на складе.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        book.count -= 1
        book.save()

        return Response(
            {'message': 'Книга успешно куплена.'},
            status=status.HTTP_200_OK
        )
