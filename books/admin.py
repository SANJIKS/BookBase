from django.contrib import admin
from .models import Book, Page

admin.site.register([Book, Page])