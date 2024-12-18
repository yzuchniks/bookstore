from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('last_name',)
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name'],
                                    name='unique_author')
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books',
                               on_delete=models.CASCADE)
    count = models.IntegerField()

    class Meta:
        ordering = ('title',)
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_book_author')
        ]

    def __str__(self):
        return self.title
