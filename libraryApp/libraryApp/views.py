from ast import And
from datetime import datetime,timedelta
from django.http import JsonResponse
from .models import Book, Loan, Fine
from .serializers import BookSerializer,SignUpSerializer,LoanSerializer,FineSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsAuthenticatedOrCreate
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,login,logout)
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.views import APIView

class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

class getBooks(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        search_by_author=request.GET.get('author')
        search_by_title=request.GET.get('title')
        search_by_availability=request.GET.get('isAvailable')
        books = Book.objects.all()
        if search_by_author is not None:
            books = books.filter(author_name=search_by_author.strip())
        if search_by_title is not None:
            books = books.filter(title=search_by_title.strip())
        if search_by_availability == 'True':
            books = books.filter(in_place=True)
        serializer = BookSerializer(books,many=True)
        return JsonResponse({"Books":serializer.data})

class getLoanedBooks(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        if request.user.is_staff:
            loans = Loan.objects.filter(isLoaned=True)
            serializer = LoanSerializer(loans,many=True)
        else:
            loans = Loan.objects.filter(isLoaned=True,user=request.user)
            serializer = LoanSerializer(loans,many=True)
        return JsonResponse({"LoanedBooks":serializer.data})

class AddBook(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,IsAdminUser)

class DeleteBook(APIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    def delete(self,request):
        _barcode=request.POST.get('barcode')
        if _barcode is None or _barcode == '':
            return JsonResponse({"message":"The barcode is not valid!"},status=404)
        try:
            book=Book.objects.get(barcode=_barcode.strip())
        except Book.DoesNotExist:
            return JsonResponse({"message":"The book couldnt be found!"},status=404)
        book.delete()
        return JsonResponse({"message":"The book was deleted successfully!"})
        

class loanBooks(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        items_on_loan = Loan.objects.filter(isLoaned=True,user=request.user)
        if items_on_loan.count() >= 10:
            return JsonResponse({"message":"Maximum of allowed loans exceeded!"},status=405)
        _barcode=request.POST.get('barcode')
        if _barcode is None:
            return JsonResponse({"message":"The barcode is not valid!"},status=404)
        is_item_loanable = Book.objects.filter(barcode=_barcode.strip(),in_place=True).first()
        if is_item_loanable is None:
            return JsonResponse({"message":"Item not available for loan"},status=405)
        new_loan = Loan.objects.create(book=is_item_loanable,isLoaned=True,loan_date=datetime.now(),
            due_date=datetime.now()+timedelta(days=14),user=request.user)
        is_item_loanable.in_place = False
        is_item_loanable.save()
        return JsonResponse({"message":"Item was loaned successfully!"})

class returnBooks(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        _barcode=request.POST.get('barcode')
        if _barcode is None:
            return JsonResponse({"message":"The barcode is not valid!"},status=404)
        book = Book.objects.filter(barcode=_barcode.strip(),in_place=False).first()
        loan = Loan.objects.filter(book=book,isLoaned=True,user=request.user).first()
        if book is None or loan is None:
            return JsonResponse({"message":"Item not returnable"},status=405)
        book.in_place = True
        book.save()
        loan.return_date=datetime.now()
        loan.isLoaned=False
        loan.save()
        if loan.return_date.date() > loan.due_date:
            Fine.objects.create(loan=loan)
            return JsonResponse({"message":"Item was returned successfully. Fine was created!"})
        return JsonResponse({"message":"Item was returned successfully!"})

class getFines(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        data={}
        loans = Loan.objects.filter(user=request.user)
        i=0
        for _loan in loans:
            try:
                fine = Fine.objects.get(loan=_loan,isFinePayed=False)
            except Fine.DoesNotExist:
                continue
            serializer = FineSerializer(fine,many=False)
            augmented_serializer_data = list(serializer.data)
            augmented_serializer_data.append({'amount': round((_loan.return_date - _loan.due_date).days*0.1,2)})
            data[i]=augmented_serializer_data
            i+=1
        return JsonResponse({"Fines":data})

