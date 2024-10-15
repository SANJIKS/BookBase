from django.urls import path
from .views import BookViewSet, PageDetailView, ReceiptViewSet

urlpatterns = [
    path('books/', BookViewSet.as_view({'get': 'list'}), name='book-list'),
    path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve'}), name='book-detail'),
    path('books/<int:book_id>/pages/', PageDetailView.as_view({'get': 'retrieve'}), name='page-detail'),
    path('books/<int:book_id>/pages/<int:page_number>/', PageDetailView.as_view({'get': 'retrieve'}), name='page-number-detail'),
    path('receipts/', ReceiptViewSet.as_view({'post': 'create'}), name='create-receipt')
]