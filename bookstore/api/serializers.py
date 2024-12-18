from rest_framework import serializers

from books.models import Author, Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('title', 'author', 'count')

    def validate_count(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'Количество книг не может быть меньше нуля.'
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'books')
