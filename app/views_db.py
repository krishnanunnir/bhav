"""
DB equivalent of redis
"""
from django.shortcuts import render
from .serializers import ImportDateSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import ImportDate
import datetime
import csv
from django.http import HttpResponse, JsonResponse
# Create your views here.

@csrf_exempt
def stock_list(request):
    """
    Returns an API with content of all the stocks
    since there is only one method, I don't think there is need for abstracts and such like viewsets
    """
    if request.method=="GET":
        importDateObj = ImportDate.objects.all().order_by("-id")
        serializer = ImportDateSerializer(importDateObj,many= True)
        return JsonResponse(serializer.data,safe= False)

def stock_list_by_name(request, stockname):
    """
    Returns an API with content of the stock with name stockname
    Search is basic query with sql 'like', so not as accurate
    """
    if request.method=="GET":
        importDateObj = ImportDate.objects.filter(name__icontains=stockname).order_by("-id")
        serializer = ImportDateSerializer(importDateObj,many= True)
        return JsonResponse(serializer.data,safe= False)

def get_as_zip(request, stockname=""):
    # Create the HttpResponse object with the appropriate CSV header.
    importDateObj = ImportDate.objects.filter(name__icontains=stockname).order_by("-id")
    date_of_access_string = datetime.date.today().strftime("%d%m%y")
    if stockname:
        file_name_zip = f'EQ{date_of_access_string}_{stockname}.zip'
    else:
        file_name_zip = f'EQ{date_of_access_string}.zip'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name_zip}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Code', 'Name', 'Open','Close','Low', 'High'])
    for  obj in importDateObj:
        print(obj)
        writer.writerow([obj.code,obj.name,obj.open_value,obj.close_value,obj.low_value,obj.high_value])
    return response
def render_stock(request, template = "index.html"):
    return render(request, template)
