from .models import Book, Loan, Fine
from rest_framework import serializers
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','barcode','author_name','title','isbn','in_place']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class LoanSerializer(serializers.ModelSerializer):
    barcode = BookSerializer(many = False)
    userid = UserSerializer(many=False)
    class Meta:
        model = Loan
        fields = ['id','barcode','userid']

class FineSerializer(serializers.ModelSerializer):
    #loan = LoanSerializer(many=False)
    class Meta:
        model = Fine
        fields = ['id','payed_date']

class SignUpSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ('username', 'password','email','is_staff')
       write_only_fields = ('password',)