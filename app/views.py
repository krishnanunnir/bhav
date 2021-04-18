from django.shortcuts import render
from .serializers import ImportDateSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import ImportDate
from django.http import HttpResponse, JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def stock_list(request):
    """
    Returns an API with content of all the stocks
    since there is only one method, I don't think there is need for abstracts and such like viewsets
    """
    if request.method=="GET":
        paginator = PageNumberPagination()
        paginator.page_size = 50
        importDateObj = ImportDate.objects.all()
        result_page = paginator.paginate_queryset(importDateObj, request)
        serializer = ImportDateSerializer(result_page,many= True)
        return JsonResponse(serializer.data,safe= False)

@api_view(['GET'])
def stock_list_by_name(request, stockname):
    """
    Returns an API with content of the stock with name stockname
    Search is basic query with sql 'like', so not as accurate
    """
    if request.method=="GET":
        paginator = PageNumberPagination()
        paginator.page_size = 50
        importDateObj = ImportDate.objects.filter(name__icontains=stockname)
        result_page = paginator.paginate_queryset(importDateObj, request)
        serializer = ImportDateSerializer(result_page,many= True)
        return JsonResponse(serializer.data,safe= False)