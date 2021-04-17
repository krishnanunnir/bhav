from django.shortcuts import render
from .serializers import ImportDateSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import ImportDate
from django.http import HttpResponse, JsonResponse
# Create your views here.

@csrf_exempt
def stock_list(request):
    if request.method=="GET":
        importDateObj = ImportDate.objects.all()
        serializer = ImportDateSerializer(importDateObj,many= True)
        return JsonResponse(serializer.data,safe= False)