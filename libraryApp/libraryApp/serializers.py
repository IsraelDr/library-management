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
    book = BookSerializer(many = False)
    user = UserSerializer(many=False)
    class Meta:
        model = Loan
        fields = ['id','book','user']

class FineSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(many=False)
    class Meta:
        model = Fine
        fields = ['id','payed_date','loan']

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password','email','is_staff')
        write_only_fields = ('password',)

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)