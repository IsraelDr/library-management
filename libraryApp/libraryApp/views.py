from ast import And
from datetime import datetime,timedelta
from django.http import JsonResponse
from .models import Book, Loan, Fine
from .serializers import BookSerializer,SignUpSerializer,LoanSerializer,FineSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedOrCreate
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,login,logout)
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.views import APIView

class SignUp(generics.CreateAPIView):
   queryset = User.objects.all()
   serializer_class = SignUpSerializer
   permission_classes = (IsAuthenticatedOrCreate,)



class getBooks(APIView):#add filter todo
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        search_by_author=request.GET.get('author')
        search_by_title=request.GET.get('title')
        search_by_availability=request.GET.get('isAvailable')
        books = Book.objects.all()
        if search_by_author is not None:
            books = books.filter(author_name=search_by_author)
        if search_by_title is not None:
            books = books.filter(title=search_by_title)
        if search_by_availability is not None:
            books = books.filter(in_place=search_by_availability)
        serializer = BookSerializer(books,many=True)
        return JsonResponse({"Books":serializer.data})

class getLoanedBooks(APIView):#add filter todo
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        if request.user.is_staff:
            loans = Loan.objects.filter(isLoaned=True)
            serializer = LoanSerializer(loans,many=True)
        else:
            loans = Loan.objects.filter(isLoaned=True,userid=request.user.id)
            serializer = LoanSerializer(loans,many=True)
        return JsonResponse({"LoanedBooks":serializer.data})

class AddBook(APIView):# todo
    permission_classes = (IsAuthenticated,)
    def put(self,request):
        _barcode=request.POST['barcode']
        _author_name=request.POST['author']
        _title=request.POST['title']
        _isbn=request.POST['isbn']
        _in_place = True
        newbook=Book.objects.create(barcode=_barcode,author_name=_author_name,title=_title,isbn=_isbn,in_place=_in_place)
        serializer = BookSerializer(newbook,many=False)
        return JsonResponse({"Created Book":serializer.data})

class DeleteBook(APIView):# todo
    permission_classes = (IsAuthenticated,)
    def delete(self,request):
        _id=request.POST['id']
        book=Book.objects.get(id=_id)
        book.delete()
        return JsonResponse({"errormessage":"The book was deleted successfully!"})

class loanBooks(APIView):# todo
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        items_on_loan = Loan.objects.filter(isLoaned=True,userid=request.user.id)
        if items_on_loan.count() >= 10:
            return JsonResponse({"errormessage":"Maximum of allowed loans exceeded!"})
        _barcode=request.POST['barcode']
        is_item_loanable = Book.objects.filter(barcode=_barcode,in_place=True).first()
        if is_item_loanable is None:
            return JsonResponse({"errormessage":"Item not available for loan"})
        new_loan = Loan.objects.create(barcode=is_item_loanable,isLoaned=True,loan_date=datetime.now(),
            due_date=datetime.now()+timedelta(days=14),userid=request.user)
        is_item_loanable.in_place = False
        is_item_loanable.save()
        return JsonResponse({"successmessage":"Item was loaned successfully!"})

class returnBooks(APIView):# todo
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        _barcode=request.POST['barcode']
        book = Book.objects.filter(barcode=_barcode,in_place=False).first()
        loan = Loan.objects.filter(barcode=book,isLoaned=True,userid=request.user).first()
        if book is None or loan is None:
            return JsonResponse({"errormessage":"Item not returnable"})
        book.in_place = True
        book.save()
        loan.return_date=datetime.now()
        loan.isLoaned=False
        loan.save()
        if loan.return_date.date() > loan.due_date:
            Fine.objects.create(loan=loan)
        return JsonResponse({"successmessage":"Item was returned successfully!"})

class getFines(APIView):# todo
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        data={}
        loans = Loan.objects.filter(userid=request.user)
        i=0
        for _loan in loans:
            try:
                fine = Fine.objects.get(loan=_loan,isFinePayed=False)
            except Fine.DoesNotExist:
                continue
            serializer = FineSerializer(fine,many=False)
            augmented_serializer_data = list(serializer.data)
            augmented_serializer_data.append({'amount': (_loan.return_date - _loan.due_date).days*0.1})
            data[i]=augmented_serializer_data
            i+=1
        return JsonResponse({"Fines":data})

