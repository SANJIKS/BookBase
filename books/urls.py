from django.urls import path
from .views import AvailableBooksView, BookPagesListView, BookViewSet, PageDetailView, ReceiptViewSet

urlpatterns = [
    path('books/', BookViewSet.as_view({'get': 'list'}), name='book-list'),
    path('available-books/', AvailableBooksView.as_view(), name='available-books'),
    path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve'}), name='book-detail'),
    path('books/<int:book_id>/pages/', PageDetailView.as_view({'get': 'retrieve'}), name='page-detail'),
    path('books/<int:book_id>/pages/<int:page_number>/', PageDetailView.as_view({'get': 'retrieve'}), name='page-number-detail'),
    path('receipts/', ReceiptViewSet.as_view({'post': 'create'}), name='create-receipt'),
    path('receipts/confirm/<int:pk>/', ReceiptViewSet.as_view({'post': 'confirm_receipt'}, name='confirm-receipt')),
    path('books/<int:book_id>/pages/download/', BookPagesListView.as_view(), name='book-pages-list'),
]