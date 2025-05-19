from django.shortcuts import render
from .serializers import BookSerializer
from bookapp.models import Book
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def books(request):
    if request.method == 'GET':
        books=Book.objects.all()
        serializer=BookSerializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method == 'POST':
        data=JSONParser().parse(request)
        serializer=BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=200)
        else:
            return JsonResponse(serializer.errors,status=404)
   

@csrf_exempt
def book_detail(request,id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if request.method == "GET":
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data, status=200, safe=False)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = BookSerializer(instance=book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)
        

def maxProfit(prices):
    min_price=float('inf')
    max_profit=0

    for price in prices:
        if price<min_price:
            min_price=price
        else:
            max_profit=max(max_profit,price-min_price)
    return max_profit




