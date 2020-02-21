from django.db import models
from django.utils.translation import ugettext_lazy as _
from .statics import ICON_LIST


class Document(models.Model):
    title = models.CharField(
        verbose_name=_('Titel'),
        max_length=100,
        blank=True,
        null=True,
    )
    document_type = models.ForeignKey(
        to='DocumentType',
        verbose_name='Type document',
        related_name='type_to_document',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    uploaded_file = models.FileField(
        verbose_name=_('Bestand'),
        upload_to='uploads'
    )
    uploaded = models.DateTimeField(
        verbose_name=_('Upload datum/tijd'),
        auto_now_add=True,
    )
    saved = models.DateTimeField(
        verbose_name=_('Opgeslagen datum/tijd'),
        auto_now=True,
    )

    def __str__(self):
        if self.document_type:
            return self.document_type.type_name
        return self.uploaded

    class Meta:
        verbose_name = _('Bestand')
        verbose_name_plural = _('Bestanden')
        ordering = ('-uploaded', )


class DocumentType(models.Model):
    type_name = models.CharField(
        verbose_name=_('Type naam'),
        max_length=100,
    )
    icon = models.CharField(
        verbose_name=_('Icon'),
        max_length=50,
        choices=ICON_LIST,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Bestands type')
        verbose_name_plural = _('Bestands types')
        ordering = ('type_name', )

    @property
    def icon_path(self):
        return 'images/%s.svg' % self.icon

    def __str__(self):
        return self.type_name