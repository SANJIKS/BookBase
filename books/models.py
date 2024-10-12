from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=120, null=True, blank=True)
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)
    author = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}" if self.title else "Untitled Book"

class Page(models.Model):
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, related_name='pages')
    content = models.ImageField(upload_to='books/content/', null=True, blank=True)
    number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Page {self.number} of {self.book.title if self.book else 'Unknown Book'}"
