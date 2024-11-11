from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import Http404

from books.permissions import IsPurchased
from .models import Book, Page, Receipt, UserBookAccess
from .serializers import BookSerializer, PageDetailSerializer, ReceiptSerializer
from .utils import send_receipt_to_moderator

class BookViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AvailableBooksView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        user_books = UserBookAccess.objects.filter(user=user).select_related('book')
        books = [access.book for access in user_books]
        
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class PageDetailView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    permission_classes = [IsAuthenticated, IsPurchased]

    def get_object(self):
        book_id = self.kwargs['book_id']
        page_number = self.kwargs.get('page_number', 1)
 
        page = Page.objects.filter(book_id=book_id, number=page_number).first()
        if not page:
            page = Page.objects.filter(book_id=book_id, number=1).first()
            if not page:
                raise Http404("Нет страниц для этой книги.")
        
        return page

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receipt = serializer.save(user=request.user)

        send_receipt_to_moderator(receipt)

        return Response({"message": "Чек загружен, ожидайте подтверждения."}, status=status.HTTP_201_CREATED)
    

# class ConfirmPayment(APIView):
#     def post

class BookPagesListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        user = request.user
        if not UserBookAccess.objects.filter(user=user, book_id=book_id).exists():
            return Response({"detail": "Access denied"}, status=403)

        pages = Page.objects.filter(book_id=book_id).order_by('number')

        page_links = {
            page.number: page.content.url if page.content else None
            for page in pages
        }

        return Response(page_links)