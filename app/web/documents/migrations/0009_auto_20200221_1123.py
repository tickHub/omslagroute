# Generated by Django 2.2.9 on 2020-02-21 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_auto_20200221_1058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ('name',), 'verbose_name': 'Document', 'verbose_name_plural': 'Documenten'},
        ),
        migrations.AlterModelOptions(
            name='documentversion',
            options={'ordering': ('-uploaded',), 'verbose_name': 'Document versie', 'verbose_name_plural': 'Document versies'},
        ),
        migrations.RenameField(
            model_name='document',
            old_name='type_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='documentversion',
            name='document_type',
        ),
        migrations.RemoveField(
            model_name='documentversion',
            name='title',
        ),
        migrations.AddField(
            model_name='documentversion',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_to_document_version', to='documents.Document', verbose_name='Document'),
        ),
        migrations.AlterField(
            model_name='document',
            name='icon',
            field=models.CharField(blank=True, choices=[('form', 'Formulier'), ('checklist', 'Checklist')], max_length=50, null=True, verbose_name='Icon'),
        ),
        migrations.AlterField(
            model_name='documentversion',
            name='uploaded',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Initieel opgeslagen datum/tijd'),
        ),
    ]
