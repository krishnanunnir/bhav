from django.shortcuts import render
from .serializers import ImportDateSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import ImportDate
from django.http import HttpResponse, JsonResponse
# Create your views here.

@csrf_exempt
def stock_list(request):
    """
    Returns an API with content of all the stocks
    since there is only one method, I don't think there is need for abstracts and such like viewsets
    """
    if request.method=="GET":
        importDateObj = ImportDate.objects.all()
        serializer = ImportDateSerializer(importDateObj,many= True)
        return JsonResponse(serializer.data,safe= False)

def stock_list_by_name(request, stockname):
    """
    Returns an API with content of the stock with name stockname
    Search is basic query with sql 'like', so not as accurate
    """
    if request.method=="GET":
        importDateObj = ImportDate.objects.filter(name__icontains=stockname)
        serializer = ImportDateSerializer(importDateObj,many= True)
        return JsonResponse(serializer.data,safe= False)