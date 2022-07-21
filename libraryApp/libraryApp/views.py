from django.http import JsonResponse
from .models import Book
from .serializers import BookSerializer

def getCatalog(request):
    books = Book.objects.all()
    serializer = BookSerializer(books,many=True)
    return JsonResponse({"Catalog":serializer.data})

