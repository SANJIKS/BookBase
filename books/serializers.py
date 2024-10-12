from rest_framework import serializers
from .models import Book, Page

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class PageDetailSerializer(serializers.ModelSerializer):
    previous_page = serializers.SerializerMethodField()
    next_page = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'book', 'content', 'number', 'previous_page', 'next_page']

    def get_previous_page(self, obj):
        previous_page = Page.objects.filter(book=obj.book, number=obj.number - 1).first()
        return previous_page.number if previous_page else None

    def get_next_page(self, obj):
        next_page = Page.objects.filter(book=obj.book, number=obj.number + 1).first()
        return next_page.number if next_page else None
