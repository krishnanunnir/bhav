"""
DB equivalent of redis
"""
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
import csv
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from .tasks import writeCSVToCache
from .serializers import EquitySerializer
from .Pagination import PageNumberCountPagination
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def stock_list(request):
    """
    Returns an API with content of all the stocks
    since there is only one method, I don't think there is need for abstracts and such like viewsets
    """
    if request.method=="GET":
        writeCSVToCache(datetime.date(2020,12,7))
        paginator = PageNumberCountPagination()
        paginator.page_size = 200
        all_stocks = []
        # keys are not ideal in very large caches
        # but our db at max contains 3000 records corresponding to equity csv
        stock_list =  cache.keys("*")
        for stock in stock_list:
            all_stocks+=[cache.get(stock)]
        result_page = paginator.paginate_queryset(all_stocks, request)
        serializer = EquitySerializer(result_page,many= True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def stock_list_by_name(request, stockname):
    """
    Returns an API with content of the stock with name stockname
    Search is basic query with sql 'like', so not as accurate
    """
    if request.method=="GET":
        paginator = PageNumberCountPagination()
        paginator.page_size = 200
        search_result = []
        search_key = cache.keys("*"+stockname.lower() +"*")
        for key in search_key:
            search_result+=[cache.get(key)]
        result_page = paginator.paginate_queryset(search_result, request)
        serializer = EquitySerializer(result_page,many= True)
        return paginator.get_paginated_response(serializer.data)

def get_as_csv(request, stockname=""):
    # Create the HttpResponse object with the appropriate CSV header.
    search_result = []
    search_key = cache.keys("*"+stockname.lower()+"*")
    date_of_access_string = datetime.date.today().strftime("%d%m%y")
    if stockname:
        file_name_csv = f'EQ{date_of_access_string}_{stockname}'
    else:
        file_name_csv = f'EQ{date_of_access_string}'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name_csv}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Code', 'Name', 'Open','Close','Low', 'High'])
    for  key in search_key:
        obj = cache.get(key)
        writer.writerow([obj["code"],obj["name"],obj["open_value"],obj["close_value"],obj["low_value"],obj["high_value"]])
    return response
def render_stock(request, template = "index.html"):
    return render(request, template)
