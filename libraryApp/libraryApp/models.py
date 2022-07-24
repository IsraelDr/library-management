from pyexpat import model
from tkinter.messagebox import NO
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    barcode = models.CharField(max_length=30,default=None)
    author_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20,default='')
    in_place = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Loan(models.Model):
    isLoaned = models.BooleanField(default=False)
    loan_date = models.DateField()
    due_date = models.DateField()
    barcode = models.ForeignKey(Book,models.SET_NULL,db_column='barcode',default=None,null=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid',default=None)
    return_date = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.barcode.barcode

class Fine(models.Model):
    isFinePayed = models.BooleanField(default=False)
    payed_date = models.DateField(null=True)
    loan = models.ForeignKey(Loan,models.SET_NULL,db_column='loan',default=None,null=True)

    def __str__(self):
        return self.loan.barcode.barcode