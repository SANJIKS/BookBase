from django.contrib import admin
from .models import Book, Page, Receipt, UserBookAccess, BonusBook

admin.site.register([Book, Page, Receipt, UserBookAccess, BonusBook])