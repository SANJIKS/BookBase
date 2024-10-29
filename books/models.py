from django.db import models

from users.models import CustomUser

class Book(models.Model):
    title = models.CharField(max_length=120, null=True, blank=True)
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)
    author = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}" if self.title else "Untitled Book"

class Page(models.Model):
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL, related_name='pages')
    content = models.FileField(upload_to='books/content/', null=True, blank=True)
    number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Page {self.number} of {self.book.title if self.book else 'Unknown Book'}"

class UserBookAccess(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} has access to {self.book}"

    
class Receipt(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='receipts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Receipt from {self.user} uploaded at {self.uploaded_at}"
