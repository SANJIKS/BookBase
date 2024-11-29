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
        for i in range(0, total_pages, chunk_size):
            images = convert_from_path(pdf_path, first_page=i + 1, last_page=min(i + chunk_size, total_pages))

            for j, image in enumerate(images):
                image_path = f'book_pages/{book.id}_page_{i + j + 1}.png'
                image.save(image_path)

                page = Page.objects.create(
                    book=book,
                    number=i + j + 1,
                    content=default_storage.save(image_path, ContentFile(open(image_path, 'rb').read()))
                )

                os.remove(image_path)


admin.site.register([Page, Receipt, UserBookAccess, BonusBook])
