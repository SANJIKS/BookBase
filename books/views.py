from rest_framework import viewsets, mixins
from django.http import Http404
from .models import Book, Page
from .serializers import BookSerializer, PageDetailSerializer

class BookViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class PageDetailView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer

    def get_object(self):
        book_id = self.kwargs['book_id']
        page_number = self.kwargs.get('page_number', 1)

        page = Page.objects.filter(book_id=book_id, number=page_number).first()
        if not page:
            page = Page.objects.filter(book_id=book_id, number=1).first()
            if not page:
                raise Http404("Нет страниц для этой книги.")
        
        return page
