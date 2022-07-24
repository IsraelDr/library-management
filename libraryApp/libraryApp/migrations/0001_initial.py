# Generated by Django 4.0.6 on 2022-07-24 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.CharField(default=None, max_length=30)),
                ('author_name', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('isbn', models.CharField(default='', max_length=20)),
                ('in_place', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isLoaned', models.BooleanField(default=False)),
                ('loan_date', models.DateField()),
                ('due_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('barcode', models.ForeignKey(db_column='barcode', default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='libraryApp.book')),
                ('userid', models.ForeignKey(db_column='userid', default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
