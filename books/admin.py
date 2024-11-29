from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pdf2image import convert_from_path
import os
from django.contrib import admin
from .models import Book, Page, Receipt, UserBookAccess, BonusBook

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cover', 'content', 'description')
    search_fields = ('title', 'author')

    def save_pdf_pages(self, request, queryset):
        for book in queryset:
            if book.content:
                self.process_pdf(book)
        self.message_user(request, "PDF обработан и страницы добавлены.")
    
    save_pdf_pages.short_description = "Обработать PDF и добавить страницы"
    actions = [save_pdf_pages]

    def process_pdf(self, book):
        pdf_path = book.content.path
        total_pages = len(convert_from_path(pdf_path, 1))
        chunk_size = 10
        book_pages_dir = 'book_pages'
        book_pages_full_path = os.path.join(default_storage.location, book_pages_dir)
        
        if not os.path.exists(book_pages_full_path):
            os.makedirs(book_pages_full_path)

        for i in range(0, total_pages, chunk_size):
            images = convert_from_path(pdf_path, first_page=i + 1, last_page=min(i + chunk_size, total_pages))

            for j, image in enumerate(images):
                image_filename = f'{book.id}_page_{i + j + 1}.png'
                image_path = os.path.join(book_pages_dir, image_filename)
                image_full_path = os.path.join(book_pages_full_path, image_filename)
                
                image.save(image_full_path)

                with open(image_full_path, 'rb') as img_file:
                    page = Page.objects.create(
                        book=book,
                        number=i + j + 1,
                        content=default_storage.save(image_path, ContentFile(img_file.read()))
                    )

                os.remove(image_full_path)

admin.site.register([Page, Receipt, UserBookAccess, BonusBook])
