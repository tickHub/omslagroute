from django.contrib import admin
from .models import *


@admin.register(DocumentVersion)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('uploaded', 'uploaded_file', 'document',)


@admin.register(Document)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'document_type')
