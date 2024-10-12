from django.db import models

from users.models import CustomUser

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

class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} purchased {self.book} on {self.purchased_at}"

    def check_free_books(self):
        if self.is_verified:
            all_books = Book.objects.all().order_by('id')

            purchased_index = list(all_books).index(self.book)

            free_books = all_books[purchased_index + 1:purchased_index + 3]

            for free_book in free_books:
                Purchase.objects.create(user=self.user, book=free_book, is_verified=True)