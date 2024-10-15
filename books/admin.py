from django.contrib import admin
from .models import Book, Page, Receipt, UserBookAccess

admin.site.register([Book, Page, Receipt, UserBookAccess])