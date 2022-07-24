from django.contrib import admin
from .models import Book,Loan,Fine

admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Fine)